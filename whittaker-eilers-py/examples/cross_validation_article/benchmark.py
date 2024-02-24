from whittaker_eilers import WhittakerSmoother
import numpy as np
from time import perf_counter
import matplotlib.pyplot as plt

axis_color = "#d0d0fa"
face_color = "#00002a"


def main():
    optimised_times = []
    smoothing_n_times = []
    data_lengths_to_test = [50, 100, 250, 500, 750, 1000, 5000, 10000]
    for data_length in data_lengths_to_test:
        x, original_y, y_with_noise = generate_data(data_length, 1.0)

        smoother = WhittakerSmoother(lmbda=100, order=2, data_length=len(y_with_noise))
        start_time = perf_counter()
        results = smoother.smooth_and_cross_validate(y_with_noise)
        end_time = perf_counter()
        optimised_times.append(end_time - start_time)

        smoother = WhittakerSmoother(
            lmbda=100, order=2, data_length=len(y_with_noise) - 1
        )

        start_time = perf_counter()
        for _i in range(len(y_with_noise)):
            smoothed = smoother.smooth(y_with_noise[:-1])
        end_time = perf_counter()
        smoothing_n_times.append(end_time - start_time)

    (time_fig, time_ax) = plt.subplots(
        figsize=(8, 4),
        facecolor=face_color,
    )
    [spine.set_color(axis_color) for (_, spine) in time_ax.spines.items()]

    time_ax.plot(
        data_lengths_to_test, optimised_times, label="Smoother Matrix", color="#59f176"
    )
    time_ax.plot(
        data_lengths_to_test, smoothing_n_times, label="Smoothing n Times", color="red"
    )

    time_ax.tick_params(
        which="both",
        axis="both",
        direction="in",
        color=axis_color,
        labelcolor=axis_color,
        labelsize=14,
    )
    # time_ax.yaxis.set_minor_locator(AutoMinorLocator())
    time_ax.tick_params(which="major", axis="y", length=6)
    time_ax.tick_params(which="major", axis="x", length=8)
    time_ax.tick_params(which="minor", axis="y", length=3)
    time_ax.tick_params(which="minor", axis="x", length=4)

    time_ax.grid(True, ls="--", alpha=0.6)
    time_ax.set_facecolor(face_color)
    time_ax.set_yscale("log")
    time_ax.set_xscale("log")

    time_ax.set_ylabel("Time Taken / s", color=axis_color)
    time_ax.set_xlabel("Data Length", color=axis_color)
    time_ax.legend()

    plt.savefig(
        "cross_validation_article/benchmark.png",
        dpi=800,
        bbox_inches="tight",
    )

    plt.show()


def generate_data(
    length: int, scale: float
) -> tuple[list[float], list[float], list[float]]:
    x = np.linspace(0, 2.0 * np.pi, length)
    y = np.cos(x)
    y_with_noise = y + np.random.normal(0, scale, x.size)

    return x, y, y_with_noise


if __name__ == "__main__":
    main()
