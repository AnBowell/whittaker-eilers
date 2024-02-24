from matplotlib.ticker import AutoMinorLocator
from whittaker_eilers import WhittakerSmoother
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from scipy.ndimage import gaussian_filter1d
from statsmodels.nonparametric.smoothers_lowess import lowess
import timeit
import json

REPEATS = 3
NUMBER_OF_RUNS = 50

SAVE_PLOT = False
BENCHMARK = False

axis_color = "#d0d0fa"
face_color = "#00002a"

color_dict = {
    "Sav-Golay": "#66b0ff",
    "Gaussian Kernel": "#f003ef",
    "LOWESS": "red",
    "Whittaker": "#59f176",
}


def main():
    data_lengths_to_bench = [40, 50, 60, 70, 1e2, 5e2, 1e3, 5e3, 1e4, 1e5]
    data_lengths_to_plot = [40, 1e2, 1e3, 1e4]
    methods = ["Sav-Golay", "Gaussian Kernel", "LOWESS", "Whittaker"]
    benchmark_results = {x: {} for x in methods}

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(16, 8),
        sharex=True,
        sharey=True,
        facecolor=face_color,
        gridspec_kw={"wspace": 0, "hspace": 0},
    )
    axes_iter = iter(axes.flatten())
    for loop_counter, data_len in enumerate(data_lengths_to_bench):
        data_len = int(data_len)
        if BENCHMARK:
            print("~~~~~~~~~~ Data Length: {} ~~~~~~~~~~~~".format(data_len))
            benchmark_results["Whittaker"][data_len] = whittaker_time(data_len)
            benchmark_results["Sav-Golay"][data_len] = sav_golay_time(data_len)
            benchmark_results["Gaussian Kernel"][data_len] = gauss_time(data_len)

            if data_len <= 1e4:
                benchmark_results["LOWESS"][data_len] = lowess_time(data_len)

        # Check outputs

        if data_len not in data_lengths_to_plot:
            continue

        x, y, y_with_noise = generate_data(data_len)
        sav_golay_smoothed = run_sav_golay(y_with_noise)
        whittaker_smoother = WhittakerSmoother(
            lmbda=1e-2, order=2, data_length=len(x), x_input=x
        )
        whittaker_smoothed = run_whittaker(whittaker_smoother, y_with_noise)
        gauss_smoothed = run_gauss(y_with_noise)
        lowess_smoothed = run_lowess(x, y_with_noise)

        ax = next(axes_iter)
        [spine.set_color(axis_color) for (_, spine) in ax.spines.items()]

        ax.tick_params(
            axis="both",
            direction="in",
            color=axis_color,
            labelcolor=axis_color,
            labelsize=14,
        )

        # ax.tick_params(
        #     axis="x", direction="in", color=axis_color, labelcolor=axis_color
        # )
        ax.grid(True, ls="--", alpha=0.6)
        ax.set_facecolor(face_color)

        ax.plot(x, y, label="Original", color="white")
        ax.scatter(
            x,
            y_with_noise,
            label="Measured",
            color="#fc8d28",
            alpha=0.5,
        )
        ax.plot(x, sav_golay_smoothed, label="Sav-Golay", color="#66b0ff")
        ax.plot(x, gauss_smoothed, label="Gaussian Kernel", color="#f003ef")
        ax.plot(x, lowess_smoothed, label="LOWESS", color="red")
        ax.plot(x, whittaker_smoothed, label="Whittaker", color="#59f176")

        ax.set_xlim(0.0, 2.0 * np.pi)

        if loop_counter == 0:
            ax.legend(fontsize=14)

    fig.supxlabel("x / Radians", color=axis_color, fontsize=18)
    y_label = fig.supylabel("Amplitude", color=axis_color, fontsize=18)
    y_label.set_x(0.07)

    if SAVE_PLOT:
        plt.savefig(
            "public/blog/scripts/outputs/whittaker_sine_end.png",
            dpi=800,
            bbox_inches="tight",
        )
    plt.show()

    if not BENCHMARK:
        return
    with open("public/blog/scripts/outputs/benchmarks.json", "w") as bench_file:
        json.dump(benchmark_results, bench_file)

    (time_fig, time_ax) = plt.subplots(
        figsize=(8, 4),
        facecolor=face_color,
    )

    for method, results in benchmark_results.items():
        data_lengths, times_taken = (results.keys(), results.values())

        time_ax.plot(data_lengths, times_taken, label=method, color=color_dict[method])

    [spine.set_color(axis_color) for (_, spine) in time_ax.spines.items()]

    time_ax.tick_params(
        which="both",
        axis="both",
        direction="in",
        color=axis_color,
        labelcolor=axis_color,
        labelsize=14,
    )
    time_ax.yaxis.set_minor_locator(AutoMinorLocator())
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

    if SAVE_PLOT:
        plt.savefig(
            "benchmarks.png",
            dpi=800,
            bbox_inches="tight",
        )

    plt.show()


def whittaker_time(data_length: int) -> float:
    setup = """
from whittaker_eilers import WhittakerSmoother
from __main__ import run_whittaker, generate_data
import numpy as np
x, y, y_with_noise = generate_data({})
x, y, y_with_noise = x.tolist(), y.tolist(), y_with_noise.tolist()
whittaker_smoother = WhittakerSmoother(lmbda=5e3, order=2, data_length=len(x))
    """.format(data_length)

    benchmark_code = """
run_whittaker(whittaker_smoother, y_with_noise)
    """
    mean_time = np.mean(
        timeit.repeat(
            setup=setup, stmt=benchmark_code, number=NUMBER_OF_RUNS, repeat=REPEATS
        )
    )
    print(
        "Whittaker time taken: {}".format(mean_time),
    )

    return mean_time


def sav_golay_time(data_length: int) -> float:
    setup = """
from scipy.signal import savgol_filter
from __main__ import run_sav_golay, generate_data
import numpy as np

x, y, y_with_noise = generate_data({})
    """.format(data_length)

    benchmark_code = """
run_sav_golay(y_with_noise)
    """

    mean_time = np.mean(
        timeit.repeat(
            setup=setup, stmt=benchmark_code, number=NUMBER_OF_RUNS, repeat=REPEATS
        )
    )
    print(
        "Sav golay time taken: {}".format(mean_time),
    )
    return mean_time


def lowess_time(data_length: int) -> float:
    setup = """
from scipy.ndimage import gaussian_filter1d
from __main__ import run_lowess, generate_data
import numpy as np

x, y, y_with_noise = generate_data({})
    """.format(data_length)

    benchmark_code = """
run_lowess(x, y_with_noise)
    """

    mean_time = np.mean(
        timeit.repeat(
            setup=setup, stmt=benchmark_code, number=NUMBER_OF_RUNS, repeat=REPEATS
        )
    )
    print(
        "Lowess time taken: {}".format(mean_time),
    )
    return mean_time


def gauss_time(data_length: int) -> float:
    setup = """
from statsmodels.nonparametric.smoothers_lowess import lowess
from __main__ import run_gauss, generate_data
import numpy as np

x, y, y_with_noise = generate_data({})
    """.format(data_length)

    benchmark_code = """
run_gauss(y_with_noise)
    """

    mean_time = np.mean(
        timeit.repeat(
            setup=setup, stmt=benchmark_code, number=NUMBER_OF_RUNS, repeat=REPEATS
        )
    )
    print("Gauss time taken: {}".format(mean_time))

    return mean_time


def generate_data(length: int) -> tuple[list[float], list[float], list[float]]:
    x = np.linspace(0, 2.0 * np.pi, length)
    y = np.sin(x)
    y_with_noise = y + np.random.normal(0, 0.1, x.size)

    return x, y, y_with_noise


def run_whittaker(smoother: WhittakerSmoother, data: list[float]) -> list[float]:
    whit_y = smoother.smooth(data)
    return whit_y


def run_sav_golay(data: list[float]) -> list[float]:
    sav_gol_y = savgol_filter(data, window_length=int(len(data) / 8), polyorder=2)
    return sav_gol_y


def run_lowess(x: list[float], data: list[float]) -> list[float]:
    lowes_y = lowess(
        data,
        x,
        frac=1.0 / 10.0,
        it=1,  # Only 1 iteration for fastest result
        return_sorted=False,
        xvals=x,
    )

    return lowes_y


def run_gauss(data: list[float]) -> list[float]:
    gauss_y = gaussian_filter1d(
        data, len(data) / 25, order=0, radius=int(len(data) / 20)
    )

    return gauss_y


if __name__ == "__main__":
    main()
