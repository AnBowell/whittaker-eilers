use pyo3::prelude::*;

use whittaker_eilers_rs::WhittakerSmoother as WhittakerSmootherRs;

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
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn whittaker_eilers(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<WhittakerSmoother>()?;
    Ok(())
}
