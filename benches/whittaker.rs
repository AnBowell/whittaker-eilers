use criterion::{black_box, criterion_group, criterion_main, Criterion};
use whittaker_eilers::WhittakerSmoother;

fn new_y_whittaker(y: &Vec<f64>) -> Vec<f64> {
    WhittakerSmoother::new(2e4, 2, y.len(), None, None)
        .unwrap()
        .smooth(y)
        .unwrap()
}

fn new_x_y_whittaker(x: &Vec<f64>, y: &Vec<f64>) -> Vec<f64> {
    WhittakerSmoother::new(2e4, 2, y.len(), Some(x), None)
        .unwrap()
        .smooth(y)
        .unwrap()
}

fn new_x_y_weights_whittaker(x: &Vec<f64>, y: &Vec<f64>, weights: &Vec<f64>) -> Vec<f64> {
    WhittakerSmoother::new(2e4, 2, y.len(), Some(x), Some(weights))
        .unwrap()
        .smooth(y)
        .unwrap()
}

fn criterion_benchmark(c: &mut Criterion) {
    let wood_data_vec: Vec<f64> = WOOD_DATASET.to_vec();
    let wood_x_vec: Vec<f64> = (0..wood_data_vec.len()).map(|x| x as f64).collect();
    let weights = vec![1.0; wood_data_vec.len()];

    let reusable_smoother = WhittakerSmoother::new(
        2e4,
        2,
        wood_data_vec.len(),
        Some(&wood_x_vec),
        Some(&weights),
    )
    .unwrap();
    c.bench_function("Whittaker Wood Y Only", |b| {
        b.iter(|| new_y_whittaker(black_box(&wood_data_vec)))
    });
    c.bench_function("Whittaker Wood X and Y", |b| {
        b.iter(|| new_x_y_whittaker(black_box(&wood_x_vec), black_box(&wood_data_vec)))
    });
    c.bench_function("Whittaker Wood X, Y, and weights", |b| {
        b.iter(|| {
            new_x_y_weights_whittaker(
                black_box(&wood_x_vec),
                black_box(&wood_data_vec),
                black_box(&weights),
            )
        })
    });
    c.bench_function("Whittaker Wood X, Y, and weights reused", |b| {
        b.iter(|| reusable_smoother.smooth(&wood_data_vec).unwrap())
    });
}
criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);

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
