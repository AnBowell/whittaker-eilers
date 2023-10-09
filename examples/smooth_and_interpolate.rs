use plotly::{common::Mode, Layout, Plot, Scatter};
use rand::thread_rng;
use rand_distr::{Distribution, Uniform};
use whittaker_eilers::WhittakerSmoother;

fn basic_smooth(x_input: &Vec<f64>, y_input: &Vec<f64>, lambda: f64, order: usize) {
    let smoothed_y_only = WhittakerSmoother::new(lambda, order, y_input.len(), None, None)
        .unwrap()
        .smooth(&y_input)
        .unwrap();

    let raw_points = Scatter::new(x_input.clone(), y_input.to_vec())
        .mode(Mode::Markers)
        .name("Raw Wood Data");
    let smoothed_points = Scatter::new(x_input.clone(), smoothed_y_only)
        .mode(Mode::Lines)
        .name("Whittaker Smoothed");

    let mut plot = Plot::new();
    plot.add_trace(raw_points);
    plot.add_trace(smoothed_points);

    let layout = Layout::new().title("Basic smoothing of equally spaced Y".into());
    plot.set_layout(layout);

    plot.show();
}

fn smooth_with_x(x_input_with_noise: &Vec<f64>, y_input: &Vec<f64>, lambda: f64, order: usize) {
    let smoothed_y_only = WhittakerSmoother::new(
        lambda,
        order,
        y_input.len(),
        Some(&x_input_with_noise),
        None,
    )
    .unwrap()
    .smooth(&y_input)
    .unwrap();

    let raw_points = Scatter::new(x_input_with_noise.clone(), y_input.to_vec())
        .mode(Mode::Markers)
        .name("Raw Wood Data");
    let smoothed_points = Scatter::new(x_input_with_noise.clone(), smoothed_y_only)
        .mode(Mode::Lines)
        .name("Whittaker Smoothed");

    let mut plot = Plot::new();
    plot.add_trace(raw_points);
    plot.add_trace(smoothed_points);

    let layout = Layout::new().title("Basic smoothing of Y with arbitrary X".into());
    plot.set_layout(layout);
    plot.show();
}

fn smooth_with_weights(
    x_input_with_noise: &Vec<f64>,
    y_input: &Vec<f64>,
    weights: &Vec<f64>,
    lambda: f64,
    order: usize,
) {
    let smoothed_y_only = WhittakerSmoother::new(
        lambda,
        order,
        y_input.len(),
        Some(&x_input_with_noise),
        Some(&weights),
    )
    .unwrap()
    .smooth(&y_input)
    .unwrap();

    let raw_points = Scatter::new(x_input_with_noise.clone(), y_input.to_vec())
        .mode(Mode::Markers)
        .name("Raw Wood Data");
    let smoothed_points = Scatter::new(x_input_with_noise.clone(), smoothed_y_only)
        .mode(Mode::Lines)
        .name("Whittaker Smoothed With Weights");

    let mut plot = Plot::new();
    plot.add_trace(raw_points);
    plot.add_trace(smoothed_points);

    let layout = Layout::new().title("Basic smoothing of Y with arbitrary X and weights".into());
    plot.set_layout(layout);
    plot.show();
}
fn smooth_and_interpolate(
    x_input: &Vec<f64>,
    y_input: &Vec<f64>,
    weights: &Vec<f64>,
    lambda: f64,
    order: usize,
) {
    let smoothed_y_only =
        WhittakerSmoother::new(lambda, order, y_input.len(), Some(&x_input), Some(&weights))
            .unwrap()
            .smooth(&y_input)
            .unwrap();

    let raw_points = Scatter::new(x_input.clone(), y_input.to_vec())
        .mode(Mode::Markers)
        .name("Raw Wood Data");
    let smoothed_points = Scatter::new(x_input.clone(), smoothed_y_only)
        .mode(Mode::Lines)
        .name("Whittaker Smoothed With Weights");

    let mut plot = Plot::new();
    plot.add_trace(raw_points);
    plot.add_trace(smoothed_points);

    let layout = Layout::new().title("Smoothing and Interpolation using weights".into());
    plot.set_layout(layout);
    plot.show();
}

fn main() {
    let mut y_input = WOOD_DATASET.to_vec();
    let x_input = (0..y_input.len()).map(|x| x as f64).collect::<Vec<f64>>();

    let mut rng = thread_rng();

    let x_noise_distribution = Uniform::new(0.0, 0.7);
    let weights_distribution = Uniform::new(0.0, 1.0);

    let x_input_with_noise = (0..y_input.len())
        .map(|x| (x as f64) + x_noise_distribution.sample(&mut rng)) //TODO! Check this is sampling each time
        .collect::<Vec<f64>>();

    let mut weights = weights_distribution
        .sample_iter(&mut rng)
        .take(y_input.len())
        .collect::<Vec<f64>>();

    let lambda = 2e4;
    let order = 2;

    basic_smooth(&x_input, &y_input, lambda, order);

    smooth_with_x(&x_input_with_noise, &y_input, lambda, order);

    smooth_with_weights(&x_input_with_noise, &y_input, &weights, lambda, order);

    for i in 30..60 {
        y_input[i] = 0.0; // Set y to some arbitrary value we want to interpolate.
        weights[i] = 0.0; // Set weights to 0 for data we want to interpolate.
    }

    smooth_and_interpolate(&x_input, &y_input, &weights, lambda, order);
}

/// Data from this repo:
/// <https://github.com/mhvwerts/whittaker-eilers-smoother>
pub const WOOD_DATASET: &[f64] = &[
    106.0, 111.0, 111.0, 107.0, 105.0, 107.0, 110.0, 108.0, 111.0, 119.0, 117.0, 107.0, 105.0,
    107.0, 109.0, 105.0, 104.0, 102.0, 108.0, 113.0, 113.0, 107.0, 103.0, 103.0, 98.0, 102.0,
    103.0, 104.0, 105.0, 105.0, 105.0, 101.0, 103.0, 107.0, 109.0, 104.0, 100.0, 103.0, 100.0,
    105.0, 102.0, 105.0, 106.0, 107.0, 104.0, 107.0, 109.0, 108.0, 111.0, 107.0, 107.0, 106.0,
    107.0, 102.0, 102.0, 101.0, 103.0, 103.0, 103.0, 100.0, 101.0, 101.0, 100.0, 102.0, 101.0,
    96.0, 96.0, 98.0, 104.0, 107.0, 107.0, 102.0, 105.0, 101.0, 105.0, 110.0, 111.0, 111.0, 100.0,
    102.0, 102.0, 107.0, 112.0, 114.0, 113.0, 108.0, 106.0, 103.0, 103.0, 101.0, 103.0, 106.0,
    107.0, 106.0, 107.0, 107.0, 104.0, 111.0, 117.0, 118.0, 115.0, 107.0, 110.0, 117.0, 121.0,
    122.0, 123.0, 119.0, 117.0, 118.0, 115.0, 111.0, 108.0, 107.0, 105.0, 105.0, 105.0, 103.0,
    105.0, 107.0, 109.0, 110.0, 111.0, 108.0, 107.0, 106.0, 108.0, 107.0, 105.0, 102.0, 101.0,
    102.0, 101.0, 97.0, 100.0, 105.0, 108.0, 108.0, 105.0, 103.0, 103.0, 100.0, 103.0, 106.0,
    107.0, 97.0, 98.0, 100.0, 101.0, 97.0, 99.0, 101.0, 104.0, 107.0, 109.0, 111.0, 109.0, 103.0,
    105.0, 102.0, 108.0, 113.0, 113.0, 108.0, 107.0, 102.0, 106.0, 106.0, 106.0, 103.0, 97.0,
    103.0, 107.0, 102.0, 107.0, 111.0, 110.0, 107.0, 103.0, 99.0, 97.0, 99.0, 100.0, 99.0, 100.0,
    99.0, 100.0, 99.0, 99.0, 98.0, 100.0, 102.0, 102.0, 106.0, 112.0, 113.0, 109.0, 107.0, 105.0,
    97.0, 105.0, 110.0, 113.0, 108.0, 101.0, 95.0, 99.0, 100.0, 97.0, 92.0, 98.0, 101.0, 103.0,
    101.0, 92.0, 95.0, 91.0, 86.0, 86.0, 87.0, 93.0, 97.0, 95.0, 91.0, 86.0, 87.0, 88.0, 88.0,
    89.0, 87.0, 90.0, 88.0, 87.0, 89.0, 90.0, 90.0, 87.0, 86.0, 88.0, 83.0, 85.0, 85.0, 87.0, 91.0,
    93.0, 96.0, 95.0, 89.0, 89.0, 85.0, 88.0, 89.0, 92.0, 95.0, 91.0, 87.0, 83.0, 83.0, 82.0, 81.0,
    81.0, 80.0, 81.0, 82.0, 80.0, 76.0, 72.0, 73.0, 75.0, 77.0, 75.0, 80.0, 81.0, 81.0, 81.0, 81.0,
    81.0, 84.0, 86.0, 87.0, 88.0, 86.0, 84.0, 82.0, 80.0, 79.0, 82.0, 82.0, 76.0, 81.0, 83.0, 82.0,
    81.0, 75.0, 78.0, 78.0, 78.0, 79.0, 82.0, 82.0, 84.0, 82.0, 77.0, 77.0, 77.0, 75.0, 77.0, 73.0,
    75.0, 76.0, 80.0, 77.0, 68.0, 71.0, 71.0, 68.0, 67.0, 69.0, 72.0, 82.0,
];
