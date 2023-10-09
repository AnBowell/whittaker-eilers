use sprs::FillInReduction::ReverseCuthillMcKee;
use sprs::SymmetryCheck::CheckSymmetry;
use sprs::{CsMat, CsMatView};
use sprs_ldl::{Ldl, LdlNumeric};

use crate::errors::WhittakerError;

/// When using vals_x, the Whittaker smoother will divide by the differences of adjacent vals_x. This can result by division by 0 and therefore NaNs
/// Checking for this behavior in vals_x beforehand prevents this.
pub const WHITTAKER_X_EPSILON: f64 = 1e-6;

/// Whitaker-Eilers Smoothing and Interpolation
///
/// A discrete-time version of spline smoothing for equally or unequally spaced data.
///
/// The idea behind this struct is for it to be reusable. For any given time-series you may have a single sampling frequency, but
/// many measurements you which to be smoothed.
///
pub struct WhittakerSmoother {
    ///  Smoothing constant. The larger lambda is, the smoother the output.
    pub lambda: f64,
    /// The order of the filter.
    pub order: usize,
    /// The length of the data to be smoothed.
    pub data_length: usize,
    vals_x: Option<Vec<f64>>,
    e_mat: CsMat<f64>,
    d_mat: CsMat<f64>,
    weights_mat: Option<CsMat<f64>>,
    to_solve: CsMat<f64>,
    ldl: LdlNumeric<f64, usize>,
}

impl WhittakerSmoother {
    /// Creates a new Whittaker smoother.
    ///
    /// This function should be used to create a new instance of the Whittaker smoother. A smoothing value, order, and length of d
    /// data should always be provided. If you wish to smooth non equally spaced data a `vals_x` must also be provided. If you wish to
    /// smooth data, applying different weights to your measurements, provide a `weights`. The Whittaker smoother can also be used to interpolate data
    /// by setting the measurement's weight to 0.
    ///
    /// The smoother can later have it's weights, lambda, and order changed without creating a new struct. However, if you wish to change the length of data to be smoothed,
    /// a new [WhittakerSmoother] should be constructed.
    ///
    /// # Arguments:
    /// * `lambda`: Controls the smoothing strength, the larger, the smoother.
    /// * `order`: The order of the filter.
    /// * `data_length`: The length of the data which is to be smoothed.
    /// * `vals_x`: The time/position at which the y measurement was taken. Used to smooth unequally spaced data. Must be monotonically increasing.
    /// * `weights`: The weight of each y measurement.
    ///
    /// # Returns
    ///
    /// Result with a new WhittakerSmoother if creation was successful.
    ///
    pub fn new(
        lambda: f64,
        order: usize,
        data_length: usize,
        vals_x: Option<&Vec<f64>>,
        weights: Option<&Vec<f64>>,
    ) -> Result<WhittakerSmoother, WhittakerError> {
        let e_mat: CsMat<f64> = CsMat::eye(data_length);

        if data_length < order {
            return Err(WhittakerError::DataTooShort(data_length, order));
        }

        let (d_mat, cloned_vals_x) = match vals_x {
            Some(x_vec) => {
                if data_length != x_vec.len() {
                    return Err(WhittakerError::LengthMismatch(data_length, x_vec.len()));
                }
                let mut cloned_x_vals = Vec::with_capacity(data_length);
                for i in 0..data_length - 1 {
                    if x_vec[i] >= x_vec[i + 1] {
                        return Err(WhittakerError::NotMonotonicallyIncreasing(i));
                    }
                    if (x_vec[i] - x_vec[i + 1]).abs() < WHITTAKER_X_EPSILON {
                        return Err(WhittakerError::SampleRateError(i));
                    }
                    cloned_x_vals.push(x_vec[i]);
                }
                cloned_x_vals.push(x_vec[data_length - 1]);

                (ddmat(x_vec, x_vec.len(), order), Some(cloned_x_vals))
            }
            None => (diff_no_ddmat(&e_mat, order), None),
        };

        let weights_mat: Option<CsMat<f64>> = match weights {
            Some(weights) => {
                if data_length != weights.len() {
                    return Err(WhittakerError::LengthMismatch(data_length, weights.len()));
                }

                let diags = (0..weights.len() + 1).collect::<Vec<usize>>();

                Some(CsMat::new_csc(
                    (weights.len(), weights.len()),
                    diags[..].to_vec(),
                    diags[..weights.len()].to_vec(),
                    weights.to_vec(),
                ))
            }
            None => None,
        };

        let to_solve: CsMat<f64> = match weights_mat.as_ref() {
            Some(weights) => weights + &(&(&d_mat.transpose_view() * &d_mat) * lambda),
            None => &e_mat + &(&(&d_mat.transpose_view() * &d_mat) * lambda),
        };

        let ldl = Ldl::new()
            .fill_in_reduction(sprs::FillInReduction::ReverseCuthillMcKee)
            .check_symmetry(CheckSymmetry)
            .check_perm(sprs::CheckPerm)
            .numeric(to_solve.view())
            .map_err(|x| WhittakerError::SolverError(x))?;

        return Ok(WhittakerSmoother {
            lambda,
            order,
            data_length,
            vals_x: cloned_vals_x,
            e_mat,
            d_mat,
            weights_mat,
            to_solve,
            ldl,
        });
    }

    /// Updates the weights of the data to be smoothed.
    ///
    /// The number of weights added should be equal to that of the data you are to smooth. They should ideally fall between 0 and 1.
    ///
    /// # Arguments:
    /// * `weights`: The weights of the measurements to be smoothed. The smaller the weight the more the measurement will be ignored. Setting a weight to 0 results in interpolation.
    ///
    /// # Returns
    /// `Result<(),WhittakerError>`: Updates the struct successfully, or returns an error.
    pub fn update_weights(&mut self, weights: &Vec<f64>) -> Result<(), WhittakerError> {
        if self.data_length != weights.len() {
            return Err(WhittakerError::LengthMismatch(
                self.data_length,
                weights.len(),
            ));
        }

        self.data_length = weights.len();

        let diags = (0..weights.len() + 1).collect::<Vec<usize>>();

        self.weights_mat = Some(CsMat::new_csc(
            (weights.len(), weights.len()),
            diags[..].to_vec(),
            diags[..weights.len()].to_vec(),
            weights.clone(),
        ));

        self.update_lambda(self.lambda)?;
        Ok(())
    }

    /// Updates the order of the Whittaker smoother.
    ///
    /// Efficiently updates the order at which the Whittaker will use to smooth the data.
    ///
    /// # Arguments:
    /// * `order`: The order to smooth.
    ///
    /// # Returns
    /// `Result<(),WhittakerError>`: Updates the struct successfully, or returns an error.
    pub fn update_order(&mut self, order: usize) -> Result<(), WhittakerError> {
        if self.data_length < order {
            return Err(WhittakerError::DataTooShort(self.data_length, order));
        }

        self.order = order;

        self.d_mat = match &self.vals_x {
            Some(x) => ddmat(x, x.len(), order),
            None => diff_no_ddmat(&self.e_mat, order),
        };

        self.update_lambda(self.lambda)?;
        Ok(())
    }

    /// Updates the smoothing constant
    ///
    /// Efficiently update the target smoothness of the Whittaker smoother. The larger the `lambda`, the smoother the data.
    ///
    /// # Arguments:
    /// * `lambda`: The smoothing constant of the Whittaker smoother.
    ///
    /// # Returns
    /// `Result<(),WhittakerError>`: Updates the struct successfully, or returns an error.
    pub fn update_lambda(&mut self, lambda: f64) -> Result<(), WhittakerError> {
        self.lambda = lambda;

        self.to_solve = match self.weights_mat.as_ref() {
            Some(weights) => weights + &(&(&self.d_mat.transpose_view() * &self.d_mat) * lambda),
            None => &self.e_mat + &(&(&self.d_mat.transpose_view() * &self.d_mat) * lambda),
        };

        self.ldl = Ldl::new()
            .fill_in_reduction(ReverseCuthillMcKee)
            .check_symmetry(CheckSymmetry)
            .numeric(self.to_solve.view())
            .map_err(|x| WhittakerError::SolverError(x))?;

        Ok(())
    }

    /// Run Whittaker smoothing on values.
    ///
    /// This function actually runs the solver which results in the smoothed data. If you just wish to continuously smooth
    /// data of different y values with the sample rate remaining the same, simply call this function with different data. Remaking the `WhittakerSmoother` struct
    /// will result in a lot of overhead.
    ///
    /// # Arguments
    /// * `vals_y`: The values which are to be smoothed by the Whittaker smoother.
    ///
    /// # Returns
    /// `Result<Vec<f64>, WhittakerError>`: Returns the smoothed/interpolated data or an error.
    ///
    pub fn smooth(&self, vals_y: &[f64]) -> Result<Vec<f64>, WhittakerError> {
        if vals_y.len() != self.data_length {
            return Err(WhittakerError::LengthMismatch(
                self.data_length,
                vals_y.len(),
            ));
        }
        return if self.weights_mat.is_some() {
            Ok(self.ldl.solve(
                self.weights_mat
                    .as_ref()
                    .unwrap()
                    .data()
                    .iter()
                    .zip(vals_y)
                    .map(|(a, b)| a * b)
                    .collect::<Vec<f64>>(),
            ))
        } else {
            Ok(self.ldl.solve(vals_y))
        };
    }
}

/// Dividing differencing matrix of order d
///
/// # Arguments
/// * `x`: Sampling positions.
/// * `size`: Length og the data.
/// * `d`: order of differences.
///
/// # Returns
/// A sparse matrix containing the divided differences of order d.
fn ddmat(x: &[f64], size: usize, d: usize) -> CsMat<f64> {
    if d == 0 {
        return CsMat::eye(size);
    } else {
        let dx: Vec<f64> = x.windows(d + 1).map(|t| 1_f64 / (t[d] - t[0])).collect();

        let ind: Vec<usize> = (0..(size - d) + 1).collect();

        let v = CsMatView::new((size - d, size - d), &ind, &ind[..(size - d)], &dx);

        let d = &v * &diff(&ddmat(x, size, d - 1));

        return d;
    }
}

// Finds the difference between adjacent elements of a sparse matrix
fn diff(e: &CsMat<f64>) -> CsMat<f64> {
    let e1 = e.slice_outer(0..e.rows() - 1);
    let e2 = e.slice_outer(1..e.rows());
    return &e2 - &e1;
}
// Dividing difference matrix for equally spaced data.
fn diff_no_ddmat(e: &CsMat<f64>, d: usize) -> CsMat<f64> {
    if d == 0 {
        return e.clone();
    } else {
        return diff_no_ddmat(&diff(e), d - 1);
    }
}
