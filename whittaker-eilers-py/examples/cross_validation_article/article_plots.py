import numpy as np
from whittaker_eilers import WhittakerSmoother
import matplotlib.pyplot as plt
import pandas as pd
from astropy.io import fits

axis_color = "#d0d0fa"
face_color = "#00002a"


def main():  #
    plot_bone_mineral_density()
    plot_optical_spectra()
    plot_humidity()


def plot_bone_mineral_density():
    # data = pd.read_csv("cross_validation_article/bone.data", delimiter=" ")
    data = pd.read_table("cross_validation_article/bone.data")

    data["age"] += np.random.uniform(0.2, 0.3, len(data))
    data.sort_values(by="age", inplace=True)

    male = data[data["gender"] == "male"]
    female = data[data["gender"] == "female"]

    y_raw_male = male["spnbmd"].to_list()
    x_input_male = male["age"]

    y_raw_female = female["spnbmd"].to_list()
    x_input_female = female["age"]

    male_smoother = WhittakerSmoother(
        1,
        2,
        len(x_input_male),
        x_input=x_input_male,
    )
    male_optimal_smooth = male_smoother.smooth_optimal(
        y_raw_male, break_serial_correlation=True
    )
    male_smoothed = male_optimal_smooth.get_optimal().get_smoothed()
    female_smoother = WhittakerSmoother(
        1,
        2,
        len(x_input_female),
        x_input=x_input_female,
    )
    female_optimal_smooth = female_smoother.smooth_optimal(
        y_raw_female, break_serial_correlation=True
    )
    female_smoothed = female_optimal_smooth.get_optimal().get_smoothed()

    (male_cross_validation_errors, smoothed_data, male_lambdas) = zip(
        *[
            (res.get_cross_validation_error(), res.get_smoothed(), res.get_lambda())
            for res in male_optimal_smooth.get_all()
        ]
    )
    (female_cross_validation_errors, smoothed_data, female_lambdas) = zip(
        *[
            (res.get_cross_validation_error(), res.get_smoothed(), res.get_lambda())
            for res in female_optimal_smooth.get_all()
        ]
    )

    print(
        "Cross male validation chosen lambda: {}".format(
            male_lambdas[np.argmin(male_cross_validation_errors)]
        )
    )
    print(
        "Cross female validation chosen lambda: {}".format(
            female_lambdas[np.argmin(female_cross_validation_errors)]
        )
    )
    (fig, ax1) = plt.subplots(figsize=(8, 4), facecolor="#00002a")
    ax1.plot(
        male_lambdas,
        male_cross_validation_errors,
        color="#59f176",
        label="Cross validation",
        marker=".",
        markersize=8,
    )
    ax1.plot(
        female_lambdas,
        female_cross_validation_errors,
        color="red",
        label="Cross validation",
        marker=".",
        markersize=8,
    )

    ax1.set_xscale("log")
    # ax1.set_yscale("log")
    ax1.spines["bottom"].set_color(axis_color)
    ax1.spines["top"].set_color(axis_color)
    ax1.spines["right"].set_color(axis_color)
    ax1.spines["left"].set_color(axis_color)

    ax1.tick_params(axis="y", direction="in", color=axis_color, labelcolor=axis_color)
    ax1.tick_params(axis="x", direction="in", color=axis_color, labelcolor=axis_color)
    ax1.grid(True, ls="--", alpha=0.6)
    # ax1.set_xlim(1e1, 1e5)
    ax1.set_facecolor("#00002a")
    plt.show(block=False)

    (fig, ax1) = plt.subplots(figsize=(8, 4), facecolor="#00002a")

    ax1.spines["bottom"].set_color(axis_color)
    ax1.spines["top"].set_color(axis_color)
    ax1.spines["right"].set_color(axis_color)
    ax1.spines["left"].set_color(axis_color)
    ax1.set_xlabel("Ages / Years", color=axis_color)
    ax1.set_ylabel("Relative Change in Spinal Bone Mineral Density", color=axis_color)
    ax1.tick_params(axis="y", direction="in", color=axis_color, labelcolor=axis_color)
    ax1.tick_params(axis="x", direction="in", color=axis_color, labelcolor=axis_color)
    ax1.grid(True, ls="--", alpha=0.6)
    ax1.set_facecolor("#00002a")
    # ax1.set_xlim(0, 50)
    #
    ax1.scatter(
        x_input_male,
        y_raw_male,
        color="#59f176",
        # label="Measured",
        alpha=0.6,
        s=10,
    )

    ax1.scatter(
        x_input_female,
        y_raw_female,
        color="red",
        # label="Measured Female",
        alpha=0.6,
        s=10,
    )

    ax1.plot(
        x_input_male,
        male_smoothed,
        color="#59f176",
        lw=2,
        label="Male",
        solid_capstyle="round",
    )
    ax1.plot(
        x_input_female,
        female_smoothed,
        color="red",
        lw=2,
        label="Female",
        solid_capstyle="round",
    )
    ax1.legend()
    plt.show()


def plot_optical_spectra():
    col = "flux"
    with fits.open("cross_validation_article/spec-1939-53389-0138.fits") as data:
        data = pd.DataFrame(data[1].data)

    # print(data["and_mask"].to_list())
    # mask = data["and_mask"] > 65552
    data["weights"] = np.full(len(data), 1)
    # data["weights"][mask] = 0.0

    smoother = WhittakerSmoother(
        5e1,
        2,
        len(data),
        x_input=data.index.to_list(),
    )

    # weights = np.bitwise_and(data["weights"].to_numpy(), data["and_mask"].to_numpy())
    # print(weights)

    smoothed = smoother.smooth(data[col].to_list())

    optimal_smooth = smoother.smooth_optimal(
        data[col].to_list(), break_serial_correlation=False
    )
    smoothed = optimal_smooth.get_optimal().get_smoothed()

    (fig, ax1) = plt.subplots(figsize=(8, 4), facecolor="#00002a")
    (cross_validation_errors, smoothed_data, lambdas) = zip(
        *[
            (res.get_cross_validation_error(), res.get_smoothed(), res.get_lambda())
            for res in optimal_smooth.get_all()
        ]
    )

    print(
        "Cross validation chosen lambda: {}".format(
            lambdas[np.argmin(cross_validation_errors)]
        )
    )

    ax1.plot(
        lambdas,
        cross_validation_errors,
        color="#fc8d28",
        label="Cross validation",
        marker=".",
        markersize=8,
    )

    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.spines["bottom"].set_color(axis_color)
    ax1.spines["top"].set_color(axis_color)
    ax1.spines["right"].set_color(axis_color)
    ax1.spines["left"].set_color(axis_color)

    ax1.tick_params(axis="y", direction="in", color=axis_color, labelcolor=axis_color)
    ax1.tick_params(axis="x", direction="in", color=axis_color, labelcolor=axis_color)
    ax1.grid(True, ls="--", alpha=0.6)
    # ax1.set_xlim(1e1, 1e5)
    ax1.set_facecolor("#00002a")
    plt.show(block=False)

    (fig, ax1) = plt.subplots(figsize=(8, 4), facecolor="#00002a")

    ax1.spines["bottom"].set_color(axis_color)
    ax1.spines["top"].set_color(axis_color)
    ax1.spines["right"].set_color(axis_color)
    ax1.spines["left"].set_color(axis_color)
    ax1.set_xlabel("Wavelenghts / Ångströms", color=axis_color)
    ax1.set_ylabel("Flux / [10-17 erg/cm2/s/Å]", color=axis_color)
    ax1.tick_params(axis="y", direction="in", color=axis_color, labelcolor=axis_color)
    ax1.tick_params(axis="x", direction="in", color=axis_color, labelcolor=axis_color)
    ax1.grid(True, ls="--", alpha=0.6)
    ax1.set_facecolor("#00002a")
    # ax1.set_xlim(0, 50)
    #
    ax1.plot(
        data.index,
        data[col],
        color="#fc8d28",
        marker=".",
        label="Measured",
        alpha=0.6,
        markersize=8,
    )

    ax1.plot(
        data.index,
        smoothed,
        color="#59f176",
        lw=2,
        label="Whittaker",
        solid_capstyle="round",
    )
    plt.show()


def plot_humidity():
    col = "AH"
    data = pd.read_csv(
        "cross_validation_article/AirQualityUCI.csv",
        delimiter=";",
        na_values=-200,
        decimal=",",
    )

    data["Date"] = pd.to_datetime(
        data["Date"] + data["Time"], format="%d/%m/%Y%H.%M.%S"
    )
    # data["Time"] = pd.to_datetime(data["Date"], format="%d/%m/%Y")

    # data["x"] = pd.Timestamp.combine(data["Date"], data["Time"])
    data["x_input"] = np.arange(0, len(data)) + 1.0
    data["weights"] = np.full(len(data), 1.0)
    nan_filter = data[col].isna()

    data["weights"][nan_filter] = 0.0
    data[col][nan_filter] = 0.0

    # data.fillna(subset=[col], inplace=True)

    smoother = WhittakerSmoother(
        5e1,
        2,
        len(data),
        x_input=data["x_input"].to_list(),
        weights=data["weights"].to_list(),
    )
    smoothed = smoother.smooth(data[col].to_list())

    optimal_smooth = smoother.smooth_optimal(
        data[col].to_list(), break_serial_correlation=True
    )
    smoothed = optimal_smooth.get_optimal().get_smoothed()

    (fig, ax1) = plt.subplots(figsize=(8, 4), facecolor="#00002a")
    (cross_validation_errors, smoothed_data, lambdas) = zip(
        *[
            (res.get_cross_validation_error(), res.get_smoothed(), res.get_lambda())
            for res in optimal_smooth.get_all()
        ]
    )

    print(
        "Cross validation chosen lambda: {}".format(
            lambdas[np.argmin(cross_validation_errors)]
        )
    )

    ax1.plot(
        lambdas,
        cross_validation_errors,
        color="#fc8d28",
        label="Cross validation",
        marker=".",
        markersize=8,
    )

    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.spines["bottom"].set_color(axis_color)
    ax1.spines["top"].set_color(axis_color)
    ax1.spines["right"].set_color(axis_color)
    ax1.spines["left"].set_color(axis_color)

    ax1.tick_params(axis="y", direction="in", color=axis_color, labelcolor=axis_color)
    ax1.tick_params(axis="x", direction="in", color=axis_color, labelcolor=axis_color)
    ax1.grid(True, ls="--", alpha=0.6)
    # ax1.set_xlim(1e1, 1e5)
    ax1.set_facecolor("#00002a")
    plt.show(block=False)

    (fig, ax1) = plt.subplots(figsize=(8, 4), facecolor="#00002a")

    ax1.spines["bottom"].set_color(axis_color)
    ax1.spines["top"].set_color(axis_color)
    ax1.spines["right"].set_color(axis_color)
    ax1.spines["left"].set_color(axis_color)
    ax1.set_xlabel("Year", color=axis_color)
    ax1.set_ylabel("Temperature Anomaly / °C", color=axis_color)
    ax1.tick_params(axis="y", direction="in", color=axis_color, labelcolor=axis_color)
    ax1.tick_params(axis="x", direction="in", color=axis_color, labelcolor=axis_color)
    ax1.grid(True, ls="--", alpha=0.6)
    ax1.set_facecolor("#00002a")
    # ax1.set_xlim(0, 50)
    #
    ax1.plot(
        data["Date"],
        np.where(nan_filter, np.nan, data[col]),
        color="#fc8d28",
        marker=".",
        label="Measured",
        alpha=0.6,
        markersize=8,
    )

    ax1.plot(
        data["Date"],
        smoothed,
        color="#59f176",
        lw=2,
        label="Whittaker",
        solid_capstyle="round",
    )
    plt.show()


if __name__ == "__main__":
    main()
