mod errors;
mod whittaker_smoother;
use pyo3::{pymodule, types::PyModule, PyResult, Python};
use whittaker_smoother::WhittakerSmoother;

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn whittaker_eilers(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<WhittakerSmoother>()?;
    Ok(())
}
