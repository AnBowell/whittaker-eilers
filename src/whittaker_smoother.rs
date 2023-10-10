use sprs::FillInReduction::ReverseCuthillMcKee;
use sprs::SymmetryCheck::CheckSymmetry;
use sprs::{CsMat, CsMatView};
use sprs_ldl::{Ldl, LdlNumeric};

use crate::errors::WhittakerError;
use crate::WHITTAKER_X_EPSILON;

/// Whitaker-Eilers Smoother and Interpolator
///
/// The smoother must be created via [WhittakerSmoother::new()] and once created, can be reused to smooth multiple sets of data as
/// efficiently as possible. You can update `lambda`, the smoothness; the order of the smoother `order`; the measurement `weights`; or the sample
/// times/positions `x_input` through the provided functions. They enable you to control the smoother without remaking costly matrices.
///
pub struct WhittakerSmoother {
    lambda: f64,
    order: usize,
    data_length: usize,
    x_input: Option<Vec<f64>>,
    e_mat: CsMat<f64>,
    d_mat: CsMat<f64>,
    weights_mat: Option<CsMat<f64>>,
    to_solve: CsMat<f64>,
    ldl: LdlNumeric<f64, usize>,
}

impl WhittakerSmoother {
    /// Create a new Whittaker-Eilers smoother and interpolator.
    ///
    /// The smoother is configured through it's `lambda` and it's `order`. `Lambda` controls the smoothness of the data and `order` controls
    /// the order of which the penalities are applied (generally 2 - 4). The smoother can then be configured to weight measurements between 0 and 1
    /// to interpolate (0 weight) or to complete trust (1 weight) the measurement. The smoother can handle equally spaced measurements by simply not passing
    /// an `x_input` or unequally spaced data by providing the sampling times/positions as `x_input`.
    ///
    /// The smoother parameters can be updated using the provided functions to avoid remaking this costly struct. The only time the [WhittakerSmoother] should be
    /// remade is when the data length has changed, or a different sampling rate has been provided.
    ///
    /// # Arguments:
    /// * `lambda`: Controls the smoothing strength, the larger, the smoother.
    /// * `order`: The order of the filter.
    /// * `data_length`: The length of the data which is to be smoothed.
    /// * `x_input`: The time/position at which the y measurement was taken. Used to smooth unequally spaced data. Must be monotonically increasing.
    /// * `weights`: The weight of each y measurement.
    pub fn new(
        lambda: f64,
        order: usize,
        data_length: usize,
        x_input: Option<&Vec<f64>>,
        weights: Option<&Vec<f64>>,
    ) -> Result<WhittakerSmoother, WhittakerError> {
        let e_mat: CsMat<f64> = CsMat::eye(data_length);

        if data_length < order {
            return Err(WhittakerError::DataTooShort(data_length, order));
        }

        let (d_mat, cloned_vals_x) = match x_input {
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
            x_input: cloned_vals_x,
            e_mat,
            d_mat,
            weights_mat,
            to_solve,
            ldl,
        });
    }

    /// Retrieve the smoother's current lambda.
    pub fn get_lambda(&self) -> f64 {
        self.lambda
    }

    /// Retrieve the smoother's current order.
    pub fn get_order(&self) -> usize {
        self.order
    }

    /// Retrieve the length of the smoother's data.
    pub fn get_data_length(&self) -> usize {
        self.data_length
    }

    /// Updates the weights of the data to be smoothed.
    ///
    /// The length of weights should be equal to that of the data you are to smooth. The values of the weights should fall between 0 and 1.
    ///
    /// # Arguments:
    /// * `weights`: The weights of the measurements to be smoothed. The smaller the weight the more the measurement will be ignored. Setting a weight to 0 results in interpolation.
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

    /// Updates the order of the Whittaker-Eilers smoother.
    ///
    /// Efficiently updates the order at which the Whittaker will use to smooth the data.
    ///
    /// # Arguments:
    /// * `order`: The order to smooth.
    pub fn update_order(&mut self, order: usize) -> Result<(), WhittakerError> {
        if self.data_length < order {
            return Err(WhittakerError::DataTooShort(self.data_length, order));
        }

        self.order = order;

        self.d_mat = match &self.x_input {
            Some(x) => ddmat(x, x.len(), order),
            None => diff_no_ddmat(&self.e_mat, order),
        };

        self.update_lambda(self.lambda)?;
        Ok(())
    }

    /// Updates the smoothing constant `lambda` of the Whittaker-Eilers smoother.
    ///
    /// Efficiently update the target smoothness of the Whittaker smoother. The larger the `lambda`, the smoother the data.
    ///
    /// # Arguments:
    /// * `lambda`: The smoothing constant of the Whittaker-Eilers smoother.
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

    /// Run Whittaker-Eilers smoothing and interpolation.
    ///
    /// This function actually runs the solver which results in the smoothed data. If you just wish to continuously smooth
    /// data of different y values with the sample rate remaining the same, simply call this function with different data. Remaking the `WhittakerSmoother` struct
    /// will result in a lot of overhead.
    ///
    /// # Arguments
    /// * `vals_y`: The values which are to be smoothed and interpolated by the Whittaker-Eilers smoother.
    ///
    /// # Returns:
    /// The smoothed and interpolated data.
    pub fn smooth(&self, y_input: &[f64]) -> Result<Vec<f64>, WhittakerError> {
        if y_input.len() != self.data_length {
            return Err(WhittakerError::LengthMismatch(
                self.data_length,
                y_input.len(),
            ));
        }
        return if self.weights_mat.is_some() {
            Ok(self.ldl.solve(
                self.weights_mat
                    .as_ref()
                    .unwrap()
                    .data()
                    .iter()
                    .zip(y_input)
                    .map(|(a, b)| a * b)
                    .collect::<Vec<f64>>(),
            ))
        } else {
            Ok(self.ldl.solve(y_input))
        };
    }
}

/// Dividing differencing matrix of order d
///
/// # Arguments
/// * `x`: Sampling positions.
/// * `size`: Length og the data.
/// * `d`: order of differences.
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
