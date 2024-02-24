use approx::assert_relative_eq;
use std::{
    fs::File,
    io::{BufRead, BufReader},
};
use whittaker_eilers::WhittakerSmoother;

// TODO: Tests need a refactor to extract common code.

#[test]
fn validate_standard_whittaker() {
    let input_data = read_input_to_vecs();
    let original_result_order_2 = read_output_to_vec("tests/data/output/output_only_y_2e4_2.csv");

    let mut whittaker_smoother =
        WhittakerSmoother::new(2e4, 2, input_data.y.len(), None, None).unwrap();

    let rust_whittaker_out = whittaker_smoother.smooth(&input_data.y).unwrap();

    assert_eq!(original_result_order_2.len(), rust_whittaker_out.len());
    for i in 0..original_result_order_2.len() {
        assert_relative_eq!(
            original_result_order_2[i],
            rust_whittaker_out[i],
            epsilon = 1e-8
        )
    }

    let original_result_order_3 = read_output_to_vec("tests/data/output/output_only_y_2e4_3.csv");

    whittaker_smoother.update_order(3).unwrap();

    let rust_whittaker_out = whittaker_smoother.smooth(&input_data.y).unwrap();

    assert_eq!(original_result_order_3.len(), rust_whittaker_out.len());
    for i in 0..original_result_order_3.len() {
        assert_relative_eq!(
            original_result_order_3[i],
            rust_whittaker_out[i],
            epsilon = 1e-8
        )
    }
}

#[test]
fn validated_weighted_whittaker() {
    let input_data = read_input_to_vecs();
    let original_result_weights =
        read_output_to_vec("tests/data/output/output_y_with_weights_2e4_2.csv");

    let mut whittaker_smoother =
        WhittakerSmoother::new(2e4, 2, input_data.y.len(), None, Some(&input_data.weights))
            .unwrap();

    let rust_whittaker_out = whittaker_smoother.smooth(&input_data.y).unwrap();

    assert_eq!(original_result_weights.len(), rust_whittaker_out.len());
    for i in 0..original_result_weights.len() {
        assert_relative_eq!(
            original_result_weights[i],
            rust_whittaker_out[i],
            epsilon = 1e-8
        )
    }

    let original_result_random_weights =
        read_output_to_vec("tests/data/output/output_y_with_random_weights_2e4_3.csv");

    whittaker_smoother
        .update_weights(&input_data.random_weights)
        .unwrap();
    whittaker_smoother.update_order(3).unwrap();

    let rust_whittaker_out = whittaker_smoother.smooth(&input_data.y).unwrap();

    assert_eq!(
        original_result_random_weights.len(),
        rust_whittaker_out.len()
    );
    for i in 0..original_result_random_weights.len() {
        assert_relative_eq!(
            original_result_random_weights[i],
            rust_whittaker_out[i],
            epsilon = 1e-8
        )
    }
}

#[test]
fn validated_x_input_whittaker() {
    let input_data = read_input_to_vecs();
    let original_result = read_output_to_vec("tests/data/output/output_x_and_y_2e4_2.csv");

    let mut whittaker_smoother =
        WhittakerSmoother::new(2e4, 2, input_data.y.len(), Some(&input_data.x), None).unwrap();

    let rust_whittaker_out = whittaker_smoother.smooth(&input_data.y).unwrap();

    assert_eq!(original_result.len(), rust_whittaker_out.len());
    for i in 0..original_result.len() {
        assert_relative_eq!(original_result[i], rust_whittaker_out[i], epsilon = 1e-8)
    }

    let original_result_order_3 = read_output_to_vec("tests/data/output/output_x_and_y_2e4_3.csv");

    whittaker_smoother.update_order(3).unwrap();

    let rust_whittaker_out = whittaker_smoother.smooth(&input_data.y).unwrap();

    assert_eq!(original_result_order_3.len(), rust_whittaker_out.len());
    for i in 0..original_result_order_3.len() {
        assert_relative_eq!(
            original_result_order_3[i],
            rust_whittaker_out[i],
            epsilon = 1e-8
        )
    }
}
#[test]
fn validated_x_input_with_weights_whittaker() {
    let input_data = read_input_to_vecs();
    let original_result = read_output_to_vec("tests/data/output/output_x_y_and_weights_2e4_2.csv");

    let mut whittaker_smoother = WhittakerSmoother::new(
        2e4,
        2,
        input_data.y.len(),
        Some(&input_data.x),
        Some(&input_data.weights),
    )
    .unwrap();

    let rust_whittaker_out = whittaker_smoother.smooth(&input_data.y).unwrap();

    assert_eq!(original_result.len(), rust_whittaker_out.len());
    for i in 0..original_result.len() {
        assert_relative_eq!(original_result[i], rust_whittaker_out[i], epsilon = 1e-8)
    }

    let original_result_random_weights =
        read_output_to_vec("tests/data/output/output_x_y_and_random_weights_2e4_2.csv");

    whittaker_smoother
        .update_weights(&input_data.random_weights)
        .unwrap();

    let rust_whittaker_out = whittaker_smoother.smooth(&input_data.y).unwrap();

    assert_eq!(
        original_result_random_weights.len(),
        rust_whittaker_out.len()
    );
    for i in 0..original_result_random_weights.len() {
        assert_relative_eq!(
            original_result_random_weights[i],
            rust_whittaker_out[i],
            epsilon = 1e-8
        )
    }
}

#[test]
fn cross_validation_no_weights_100() {
    let input_data = read_input_to_vecs();

    let mut whittaker_smoother =
        WhittakerSmoother::new(2e4, 2, input_data.y[..100].len(), None, None).unwrap();

    let cve = whittaker_smoother
        .smooth_and_cross_validate(&input_data.y[..100])
        .unwrap();

    assert_relative_eq!(cve.cross_validation_error, 1.5806, epsilon = 1e-4); // Produced from matlab scripts.

    whittaker_smoother.update_order(3).unwrap();

    let cve = whittaker_smoother
        .smooth_and_cross_validate(&input_data.y[..100])
        .unwrap();

    assert_relative_eq!(cve.cross_validation_error, 1.6178, epsilon = 1e-4);
}
#[test]
fn cross_validation_no_weights() {
    let input_data = read_input_to_vecs();

    let mut whittaker_smoother =
        WhittakerSmoother::new(2e4, 2, input_data.y.len(), None, None).unwrap();

    let cve = whittaker_smoother
        .smooth_and_cross_validate(&input_data.y)
        .unwrap();

    assert_relative_eq!(cve.cross_validation_error, 3.3568, epsilon = 1e-4); // Produced from matlab scripts.

    whittaker_smoother.update_order(3).unwrap();

    let cve = whittaker_smoother
        .smooth_and_cross_validate(&input_data.y)
        .unwrap();

    assert_relative_eq!(cve.cross_validation_error, 2.6859, epsilon = 1e-4);
}
#[test]
fn cross_validation_weights_100() {
    let input_data = read_input_to_vecs();

    let whittaker_smoother = WhittakerSmoother::new(
        2e4,
        2,
        input_data.y[..100].len(),
        None,
        Some(&input_data.weights[..100].to_vec()),
    )
    .unwrap();

    let cve = whittaker_smoother
        .smooth_and_cross_validate(&input_data.y[..100])
        .unwrap();

    assert_relative_eq!(cve.cross_validation_error, 1.7282, epsilon = 1e-4);
}
#[test]
fn cross_validation_weights() {
    let input_data = read_input_to_vecs();

    let whittaker_smoother = WhittakerSmoother::new(
        2e4,
        2,
        input_data.y.len(),
        None,
        Some(&input_data.weights.to_vec()),
    )
    .unwrap();

    let cve = whittaker_smoother
        .smooth_and_cross_validate(&input_data.y)
        .unwrap();

    assert_relative_eq!(cve.cross_validation_error, 3.4549, epsilon = 1e-4);
}
#[test]
fn cross_validation_weights_x_input_100() {
    let input_data = read_input_to_vecs();

    let whittaker_smoother = WhittakerSmoother::new(
        2e4,
        2,
        input_data.y[..100].len(),
        Some(&input_data.x[..100].to_vec()),
        Some(&input_data.weights[..100].to_vec()),
    )
    .unwrap();

    let cve = whittaker_smoother
        .smooth_and_cross_validate(&input_data.y[..100])
        .unwrap();

    assert_relative_eq!(cve.cross_validation_error, 1.7426, epsilon = 1e-4);
}
#[test]
fn cross_validation_weights_x_input() {
    let input_data = read_input_to_vecs();

    let whittaker_smoother = WhittakerSmoother::new(
        2e4,
        2,
        input_data.y.len(),
        Some(&input_data.x.to_vec()),
        Some(&input_data.weights.to_vec()),
    )
    .unwrap();

    let cve = whittaker_smoother
        .smooth_and_cross_validate(&input_data.y)
        .unwrap();

    assert_relative_eq!(cve.cross_validation_error, 3.0762, epsilon = 1e-4);
}
#[test]
fn cross_validation_x_input_100() {
    let input_data = read_input_to_vecs();

    let whittaker_smoother = WhittakerSmoother::new(
        2e4,
        2,
        input_data.y[..100].len(),
        Some(&input_data.x[..100].to_vec()),
        None,
    )
    .unwrap();

    let cve = whittaker_smoother
        .smooth_and_cross_validate(&input_data.y[..100])
        .unwrap();

    assert_relative_eq!(cve.cross_validation_error, 1.5872, epsilon = 1e-4);
}
#[test]
fn cross_validation_x_input() {
    let input_data = read_input_to_vecs();

    let whittaker_smoother = WhittakerSmoother::new(
        2e4,
        2,
        input_data.y.len(),
        Some(&input_data.x.to_vec()),
        None,
    )
    .unwrap();

    let cve = whittaker_smoother
        .smooth_and_cross_validate(&input_data.y)
        .unwrap();

    assert_relative_eq!(cve.cross_validation_error, 3.0413, epsilon = 1e-4);
}

// #[test]
// fn smooth_and_optimise() {
//     let input_data = read_input_to_vecs();

//     let mut whittaker_smoother = WhittakerSmoother::new(
//         2e4,
//         2,
//         input_data.y[..1000].len(),
//         None,
//         Some(&vec![1.0; input_data.y[..1000].len()]),
//     )
//     .unwrap();

//     let cve = whittaker_smoother
//         .smooth_optimal(&input_data.y[..1000], false)
//         .unwrap();

//     let expected = vec![
//         2.1757, 2.1454, 2.0975, 2.0590, 2.0582, 2.0985, 2.1701, 2.2592, 2.3701, 2.5221, 2.7156,
//         2.9600, 3.2329, 3.4642, 3.6345, 3.7721, 3.9201, 4.1200, 4.4106, 4.8411, 5.5055,
//     ];

//     for (actual, expected) in cve.validation_results.iter().zip(expected) {
//         assert_relative_eq!(actual.cross_validation_error, expected, epsilon = 1e-4);
//     }
// }

const INPUT_DATA_LOC: &'static str = "tests/data/input/nmr_with_weights_and_x.csv";

pub struct InputData {
    pub x: Vec<f64>,
    pub y: Vec<f64>,
    pub weights: Vec<f64>,
    pub random_weights: Vec<f64>,
}

pub fn read_input_to_vecs() -> InputData {
    let file = File::open(INPUT_DATA_LOC).unwrap();
    let reader = BufReader::new(file);

    let mut x = Vec::with_capacity(1024);
    let mut y = Vec::with_capacity(1024);
    let mut weights = Vec::with_capacity(1024);
    let mut random_weights = Vec::with_capacity(1024);

    let mut line_string;

    for line in reader.lines() {
        line_string = line.unwrap();
        let mut columns = line_string.split(",");
        x.push(columns.next().unwrap().parse::<f64>().unwrap());
        y.push(columns.next().unwrap().parse::<f64>().unwrap());
        weights.push(columns.next().unwrap().parse::<f64>().unwrap());
        random_weights.push(columns.next().unwrap().parse::<f64>().unwrap());
    }

    return InputData {
        x,
        y,
        weights,
        random_weights,
    };
}

pub fn read_output_to_vec(file_name: &str) -> Vec<f64> {
    let file = File::open(file_name).unwrap();
    let reader = BufReader::new(file);

    let output = reader
        .lines()
        .map(|x| x.unwrap().parse::<f64>().unwrap())
        .collect();

    return output;
}
