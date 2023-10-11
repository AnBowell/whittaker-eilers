from whittaker_eilers import WhittakerSmoother


def smooth_equally_spaced():
    data_to_smooth = [1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0]

    whittaker_smoother = WhittakerSmoother(
        lmbda=2e4, order=2, data_length=len(data_to_smooth)
    )

    smoothed_data = whittaker_smoother.smooth(data_to_smooth)

    print("Smoothed equally spaced data: {}".format(smoothed_data))


def smoothed_non_equally_spaced_data():
    x_input = [1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0]
    data_to_smooth = [1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0]

    whittaker_smoother = WhittakerSmoother(
        lmbda=2e4, order=2, data_length=len(data_to_smooth), x_input=x_input
    )

    smoothed_data = whittaker_smoother.smooth(data_to_smooth)

    print("Smoothed non-equally spaced data: {}".format(smoothed_data))


def smoothed_weighted_and_interpolation():
    x_input = [1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0]
    data_to_smooth = [1.1, 1.9, 3.1, 3.91, 5.0, 6.02, 7.01, 7.7, 9.0, 10.0]
    weights = [1.0] * len(x_input)
    weights[5] = 0.0

    whittaker_smoother = WhittakerSmoother(
        lmbda=2e4,
        order=2,
        data_length=len(data_to_smooth),
        x_input=x_input,
        weights=weights,
    )

    smoothed_data = whittaker_smoother.smooth(data_to_smooth)

    print("Smoothed and interpolated weighted data: {}".format(smoothed_data))


if __name__ == "__main__":
    smooth_equally_spaced()
    smoothed_non_equally_spaced_data()
    smoothed_weighted_and_interpolation()
