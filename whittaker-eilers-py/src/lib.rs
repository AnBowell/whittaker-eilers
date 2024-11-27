mod cross_validation;
mod errors;
mod whittaker_smoother;

use pyo3::{
    pymodule,
    types::{PyModule, PyModuleMethods},
    Bound, PyResult,
};
use whittaker_smoother::WhittakerSmoother;

#[pymodule]
fn whittaker_eilers(m: &Bound<'_, PyModule>) -> PyResult<()> {
    #![doc = include_str!("../README.md")]
    m.add_class::<WhittakerSmoother>()?;
    Ok(())
}
