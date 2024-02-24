mod cross_validation;
mod errors;
mod whittaker_smoother;

use pyo3::{pymodule, types::PyModule, PyResult, Python};
use whittaker_smoother::WhittakerSmoother;

#[pymodule]
fn whittaker_eilers(_py: Python, m: &PyModule) -> PyResult<()> {
    #![doc = include_str!("../README.md")]
    m.add_class::<WhittakerSmoother>()?;
    Ok(())
}
