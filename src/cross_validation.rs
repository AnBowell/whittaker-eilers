/// Contains the results of cross validation for a variety of lambdas
///
/// This struct contains the results of finding the optimal lambda. A vec
/// contains all of the lambdas, smoothed series, and errors. A function then
/// provides the ability to return the optimal one.
///
#[derive(Clone, Debug)]
pub struct OptimisedSmoothResult {
    /// The lambda, smoothed series, and errors for each lambda tested.
    pub validation_results: Vec<CrossValidationResult>,
    pub(crate) optimal_index: usize,
}

impl OptimisedSmoothResult {
    /// Returns the optimally smoothed data series, lambda, and error.
    pub fn get_optimal(&self) -> CrossValidationResult {
        self.validation_results[self.optimal_index].to_owned()
    }
}
/// The result of smoothing with cross validation
#[derive(Clone, Debug)]
pub struct CrossValidationResult {
    /// The lambda value that was used to smooth the data.
    pub lambda: f64,
    /// The smoothed data.
    pub smoothed: Vec<f64>,
    /// The associated cross validation error for the smoothed data. Technically square-rooted cross validation error.
    pub cross_validation_error: f64,
}

pub(crate) fn every_fifth_element(data: &[f64]) -> Vec<f64> {
    data.iter()
        .enumerate()
        .filter(|(index, _)| index % 5 == 0)
        .map(|(_, val)| *val)
        .collect::<Vec<f64>>()
}
