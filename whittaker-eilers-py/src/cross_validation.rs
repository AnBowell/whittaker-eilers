use pyo3::prelude::*;

use whittaker_eilers_rs::CrossValidationResult as CrossValidationResultRs;
use whittaker_eilers_rs::OptimisedSmoothResult as OptimisedSmoothResultRs;

/// Contains the results of cross validation for a variety of lambdas
///
/// This class contains the results of finding the optimal lambda. A vec
/// contains all of the lambdas, smoothed series, and errors. `get_optimal` then
/// provides the ability to return the optimal one and `get_all` will return the full results.
#[pyclass]
#[repr(transparent)]
pub struct OptimisedSmoothResult(pub(crate) OptimisedSmoothResultRs);

#[pymethods]
impl OptimisedSmoothResult {
    /// Gets the optimally smoothed result.
    pub fn get_optimal(&self) -> CrossValidationResult {
        CrossValidationResult(self.0.get_optimal())
    }
    /// Gets all of the smoothed results.
    pub fn get_all(&self) -> Vec<CrossValidationResult> {
        self.0
            .validation_results
            .iter()
            .map(|x| CrossValidationResult(x.clone()))
            .collect()
    }
}

/// The result of smoothing with cross validation
#[pyclass]
#[repr(transparent)]
pub struct CrossValidationResult(pub(crate) CrossValidationResultRs);

#[pymethods]
impl CrossValidationResult {
    /// The lambda value that was used to smooth the data.
    pub fn get_lambda(&self) -> f64 {
        self.0.lambda
    }
    /// The smoothed data.
    pub fn get_smoothed(&self) -> Vec<f64> {
        self.0.smoothed.clone()
    }
    /// The associated cross validation error for the smoothed data. Technically square-rooted cross validation error.
    pub fn get_cross_validation_error(&self) -> f64 {
        self.0.cross_validation_error
    }
}
