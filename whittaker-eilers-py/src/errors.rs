use pyo3::create_exception;
use pyo3::exceptions::PyException;
use pyo3::PyErr;

use whittaker_eilers_rs::WhittakerError as WhittakerErrorRs;

pub struct WhittakerError(pub WhittakerErrorRs);

impl std::convert::From<WhittakerError> for PyErr {
    fn from(err: WhittakerError) -> PyErr {
        match &err.0 {
            WhittakerErrorRs::LengthMismatch(_, _) => LengthMismatch::new_err(err.0.to_string()),
            WhittakerErrorRs::DataTooShort(_, _) => DataTooShort::new_err(err.0.to_string()),
            WhittakerErrorRs::SolverError(_) => SolverError::new_err(err.0.to_string()),
            WhittakerErrorRs::SampleRateError(_) => SolverError::new_err(err.0.to_string()),
            WhittakerErrorRs::NotMonotonicallyIncreasing(_) => {
                NotMonotonicallyIncreasing::new_err(err.0.to_string())
            }
        }
    }
}

create_exception!(whittaker_eilers, LengthMismatch, PyException);
create_exception!(whittaker_eilers, DataTooShort, PyException);
create_exception!(whittaker_eilers, SolverError, PyException);
create_exception!(whittaker_eilers, SampleRateError, PyException);
create_exception!(whittaker_eilers, NotMonotonicallyIncreasing, PyException);
