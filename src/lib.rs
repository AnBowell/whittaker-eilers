#![doc = include_str!("../README.md")]
#![deny(missing_docs, unused_imports)]

mod cross_validation;
mod errors;
mod whittaker_smoother;

pub use cross_validation::{CrossValidationResult, OptimisedSmoothResult};
pub use errors::WhittakerError;
pub use errors::WHITTAKER_X_EPSILON;
pub use whittaker_smoother::WhittakerSmoother;
