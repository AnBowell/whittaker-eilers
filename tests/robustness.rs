use whittaker_eilers::WhittakerSmoother;

#[test]
fn short_data() {
    let whittaker_smoother = WhittakerSmoother::new(2e4, 2, 2, None, None).unwrap();

    assert!(whittaker_smoother.smooth(&vec![0.1, 0.2]).is_ok());
}

#[test]
fn mismatched_data_length() {
    let whittaker_smoother = WhittakerSmoother::new(2e4, 2, 3, None, None).unwrap();

    assert!(whittaker_smoother.smooth(&vec![0.1, 0.2]).is_err());

    assert!(WhittakerSmoother::new(2e4, 2, 3, Some(&vec![1.0, 2.0]), None).is_err());
    assert!(WhittakerSmoother::new(2e4, 2, 3, None, Some(&vec![1.0, 2.0])).is_err());
    assert!(
        WhittakerSmoother::new(2e4, 2, 3, Some(&vec![1.0, 2.0]), Some(&vec![1.0, 2.0])).is_err()
    );
}
#[test]
fn data_too_short() {
    assert!(WhittakerSmoother::new(2e4, 2, 1, None, None).is_err());
}

#[test]
fn x_not_monotonically_increasing() {
    let test_vec = vec![1.0, 2.0, 2.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0];

    assert!(WhittakerSmoother::new(2e4, 1, 10, Some(&test_vec), None).is_err());
}
#[test]
fn x_sampled_too_closely() {
    let test_vec = vec![1.0, 2.0, 2.0 + 1e-8, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0];

    assert!(WhittakerSmoother::new(2e4, 1, 10, Some(&test_vec), None).is_err());
}
