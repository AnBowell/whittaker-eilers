use sprs::errors::LinalgError;

/// The smallest difference allowed between elements of x inputs.
/// 
/// When using an x input in the Whittaker, the difference between consecutive inputs is calculated
/// and used as a divisor. If this gets too small you'll end up with NaNs everywhere. Easier to prevent it!
pub const WHITTAKER_X_EPSILON: f64 = 1e-6;


#[derive(PartialEq, Eq, Debug, Clone)]
/// Common errors that occur within the Whittaker-Eilers smoother.
pub enum WhittakerError {
    /// Occurs when two inputs provided (x, y, or weights) do not have the same length. Contains the two lengths.
    LengthMismatch(usize, usize),
    /// Occurs when input length is smaller than the order of the smoother. Contains the length and order.
    DataTooShort(usize, usize),
    /// Occurs when the LDLT decomposition fails to solve. Passes through error from [sprs]. Contains the [LinalgError] from [sprs].
    SolverError(LinalgError),
    /// Occurs when the x input is more closely spaced than [WHITTAKER_X_EPSILON]. This error prevents NaNs. Contains the offending data index.
    SampleRateError(usize),
    /// Occurs when the x input is not increasing Monotonically. It should be always increasing; never remaining constant or decreasing. Contains the offending data index.
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
