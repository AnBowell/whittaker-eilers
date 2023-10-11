use pyo3::prelude::*;

use whittaker_eilers_rs::WhittakerError as WhittakerErrorRs;
use whittaker_eilers_rs::WhittakerSmoother as WhittakerSmootherRs;

use crate::errors::WhittakerError;
#[pyclass]
#[repr(transparent)]
pub struct WhittakerSmoother(WhittakerSmootherRs);

#[pymethods]
impl WhittakerSmoother {
    #[new]
    // #[pyo3(signature = (lmbda, order, data_length, x_input, weights), text_signature = "(lmbda, order, data_length, x_input, weights)")]
    pub fn __init__(
        lmbda: f64, // Lambda is a key word in python
        order: usize,
        data_length: usize,
        x_input: Option<Vec<f64>>,
        weights: Option<Vec<f64>>,
    ) -> PyResult<Self> {
        Ok(WhittakerSmoother(
            WhittakerSmootherRs::new(
                lmbda,
                order,
                data_length,
                x_input.as_ref(),
                weights.as_ref(),
            )
            .map_err(map_err_to_py)?,
        ))
    }

    pub fn get_order(&self) -> usize {
        self.0.get_order()
    }
    pub fn get_lambda(&self) -> f64 {
        self.0.get_lambda()
    }
    pub fn get_data_length(&self) -> usize {
        self.0.get_data_length()
    }

    pub fn update_weights(&mut self, weights: Vec<f64>) -> PyResult<()> {
        self.0.update_weights(&weights).map_err(map_err_to_py)
    }

    pub fn update_order(&mut self, order: usize) -> PyResult<()> {
        self.0.update_order(order).map_err(map_err_to_py)
    }

    pub fn update_lambda(&mut self, lambda: f64) -> PyResult<()> {
        self.0.update_lambda(lambda).map_err(map_err_to_py)
    }

    pub fn smooth(&self, y_vals: Vec<f64>) -> PyResult<Vec<f64>> {
        self.0.smooth(&y_vals).map_err(map_err_to_py)
    }
}

fn map_err_to_py(err: WhittakerErrorRs) -> PyErr {
    PyErr::from(WhittakerError(err))
}
