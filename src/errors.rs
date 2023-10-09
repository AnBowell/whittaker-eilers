use sprs::errors::LinalgError;

use crate::WHITTAKER_X_EPSILON;

#[derive(PartialEq, Eq, Debug, Clone)]
/// Common errors that occur within the Whittaker-Eilers smoother.
pub enum WhittakerError {
    /// Occurs when two inputs provided (x, y, or weights) do not have the same length.
    LengthMismatch(usize, usize),
    /// Occurs when input length is smaller than the order of the smoother.
    DataTooShort(usize, usize),
    /// Occurs when the LDLT decomposition fails to solve. Passes through error from [sprs].
    SolverError(LinalgError),
    /// Occurs when the x input is more closely spaced than [WHITTAKER_X_EPSILON]. This error prevents NaNs.
    SampleRateError(usize),
    /// Occurs when the x input is not increasing Monotonically. It should be always increasing; never remaining constant or decreasing.
    NotMonotonicallyIncreasing(usize),
}

impl std::fmt::Display for WhittakerError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            WhittakerError::LengthMismatch(expected, actual) => {
                write!(
                    f,
                    "Length mismatch: expected {}, got {}.",
                    expected, actual,
                )
            }
            WhittakerError::DataTooShort(length, order) => write!(
                f,
                "Input too short. Data must be longer than the order of the smoother. Data length: {}, smoother order: {}.",
                length, order
            ),
            WhittakerError::SolverError(linalg_error) => write!(
                f,
                "Error attempting to create solver for system: {}",
                linalg_error
            ),
            WhittakerError::SampleRateError(position) => write!(
                f, 
                "vals_x input data needs to be spaced a minimum of {} apart. If this is not the case, try scaling up your vals_x. Offending index: {}.",
                WHITTAKER_X_EPSILON, position
            ),
            WhittakerError::NotMonotonicallyIncreasing(position) => write!(
                f,
                "vals_x input data needs to be monotonically increasing. Offending index: {}", position
            )
        }
    }
}
impl std::error::Error for WhittakerError {}
