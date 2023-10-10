use pyo3::prelude::*;

use whittaker_eilers_rs::WhittakerSmoother as WhittakerSmootherRs;
mod whittaker_smoother;

#[pyclass]
struct WhittakerSmoother(WhittakerSmootherRs);

#[pymethods]
impl WhittakerSmoother {
    // pub(crate) fn new(ws: WhittakerSmootherRs) -> Self {
    //     WhittakerSmoother(ws)
    // }
    #[new]
    pub fn __init__(
        lambda: f64,
        order: usize,
        data_length: usize,
        x_input: Vec<f64>,
        weights: Vec<f64>,
    ) -> PyResult<Self> {
        Ok(WhittakerSmoother(
            WhittakerSmootherRs::new(lambda, order, data_length, Some(&x_input), Some(&weights))
                .unwrap(),
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
}
