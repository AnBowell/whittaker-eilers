/// TODO
pub struct OptimisedSmoothResult {
    /// TODO
    pub validation_results: Vec<CrossValidationResult>,
    pub(crate) optimal_index: usize,
}

impl OptimisedSmoothResult {
    /// TODO
    pub fn get_optimal(&self) -> CrossValidationResult {
        return self.validation_results[self.optimal_index].to_owned();
    }
}
/// TODO
#[derive(Clone, Debug)]
pub struct CrossValidationResult {
    /// TODO
    pub lambda: f64,
    /// TODO
    pub smoothed: Vec<f64>,
    /// TODO
    pub cross_validation_error: f64,
}

pub(crate) fn every_tenth_element(data: &[f64]) -> Vec<f64> {
    data.iter()
        .enumerate()
        .filter(|(index, _)| index % 10 == 0)
        .map(|(_, val)| *val)
        .collect::<Vec<f64>>()
}
