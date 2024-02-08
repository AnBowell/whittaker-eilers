use pyo3::prelude::*;

use whittaker_eilers_rs::CrossValidationResult as CrossValidationResultRs;
use whittaker_eilers_rs::OptimisedSmoothResult as OptimisedSmoothResultRs;

/// Doc string here
#[pyclass]
#[repr(transparent)]
pub struct OptimisedSmoothResult(pub(crate) OptimisedSmoothResultRs);

#[pymethods]
impl OptimisedSmoothResult {
    pub fn get_optimal(&self) -> CrossValidationResult {
        CrossValidationResult(self.0.get_optimal())
    }
}

#[pyclass]
#[repr(transparent)]
pub struct CrossValidationResult(pub(crate) CrossValidationResultRs);

#[pymethods]
impl CrossValidationResult {
    pub fn get_lambda(&self) -> f64 {
        self.0.lambda
    }
    pub fn get_smoothed(&self) -> Vec<f64> {
        self.0.smoothed.clone()
    }
    pub fn get_cross_validation_error(&self) -> f64 {
        self.0.cross_validation_error
    }
}
