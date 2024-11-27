"""Demonstrates smoothing many series in parallel"""

from whittaker_eilers import WhittakerSmoother
from time import perf_counter
import numpy as np


NUMBER_OF_SERIES = 100000


def main():

    data = np.loadtxt("graph.txt", skiprows=5)
    years = data[:, 0]
    temp_anom = data[:, 1]

    smooth_only_y(temp_anom)
    smooth_y_with_x(years, temp_anom)
    smooth_y_with_x_and_weights(years, temp_anom)


def smooth_only_y(y):
    whittaker_smoother = WhittakerSmoother(lmbda=20, order=2, data_length=len(y))

    many_inputs = [y] * NUMBER_OF_SERIES

    start_time = perf_counter()
    result = whittaker_smoother.smooth_parallel(many_inputs)
    end_time = perf_counter()

    print(
        "Took: {:.2f}s to process {} time-series".format(
            end_time - start_time, len(result)
        )
    )


def smooth_y_with_x(x, y):
    whittaker_smoother = WhittakerSmoother(
        lmbda=90000, order=3, data_length=len(y), x_input=x
    )

    many_inputs = [y] * NUMBER_OF_SERIES

    many_inputs[-1] = many_inputs[-1][
        100:
    ].tolist()  # Creates an error as it's of a different length! Represented as None...

    start_time = perf_counter()
    result = whittaker_smoother.smooth_parallel(many_inputs)
    end_time = perf_counter()
    print(
        "Took: {:.2f}s to process {} time-series with x inputs".format(
            end_time - start_time, len(result)
        )
    )


def smooth_y_with_x_and_weights(x, y):

    weights = np.full(x.size, 1.0)
    weights[::5] = 0.0

    whittaker_smoother = WhittakerSmoother(
        lmbda=20, order=2, data_length=len(y), x_input=x, weights=weights.tolist()
    )
    many_inputs = [y] * NUMBER_OF_SERIES

    start_time = perf_counter()
    result = whittaker_smoother.smooth_parallel(many_inputs)
    end_time = perf_counter()

    print(
        "Took: {:.2f}s to process {} time-series with x inputs & weights".format(
            end_time - start_time, len(result)
        )
    )


if __name__ == "__main__":
    main()
