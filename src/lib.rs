#![doc = include_str!("../README.md")]
#![deny(missing_docs, unused_imports)]

mod errors;
mod whittaker_smoother;

pub use errors::WhittakerError;
pub use whittaker_smoother::WhittakerSmoother;
pub use whittaker_smoother::WHITTAKER_X_EPSILON;
