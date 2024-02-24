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
    np.random.seed(9420)
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

    (fig, smooth_ax, cve_ax) = create_figure_and_axes()

    cve_ax.plot(
        male_lambdas,
        male_cross_validation_errors,
        color="#59f176",
        label="Cross validation",
        marker=".",
        markersize=8,
    )
    cve_ax.plot(
        female_lambdas,
        female_cross_validation_errors,
        color="red",
        label="Cross validation",
        marker=".",
        markersize=8,
    )

    cve_ax.set_xlabel("λ", color=axis_color, fontsize=16)
    cve_ax.set_ylabel("RCVE", color=axis_color, fontsize=14)
    cve_ax.set_xscale("log")

    smooth_ax.set_xlabel("Age / year", color=axis_color, fontsize=14)
    smooth_ax.set_ylabel("Δ Spinal Bone Mineral Density", color=axis_color, fontsize=14)
    smooth_ax.set_xlim(10, 25)
    smooth_ax.scatter(
        x_input_male,
        y_raw_male,
        color="#59f176",
        alpha=0.6,
        s=10,
    )

    smooth_ax.scatter(
        x_input_female,
        y_raw_female,
        color="red",
        alpha=0.6,
        s=10,
    )

    smooth_ax.plot(
        x_input_male,
        male_smoothed,
        color="#59f176",
        lw=2,
        label="Male: λ = {:.0f}".format(male_optimal_smooth.get_optimal().get_lambda()),
        solid_capstyle="round",
    )
    smooth_ax.plot(
        x_input_female,
        female_smoothed,
        color="red",
        lw=2,
        label="Female: λ = {:.0f}".format(
            female_optimal_smooth.get_optimal().get_lambda()
        ),
        solid_capstyle="round",
    )
    smooth_ax.legend()
    fig.tight_layout()
    plt.savefig(
        "cross_validation_article/bone_mineral_density.png",
        dpi=800,
        bbox_inches="tight",
    )
    plt.show(block=False)


def plot_optical_spectra():
    col = "flux"
    with fits.open("cross_validation_article/spec-1939-53389-0138.fits") as data:
        data = pd.DataFrame(data[1].data)

    # print(data["and_mask"].to_list())
    # mask = data["and_mask"] > 65552
    data["weights"] = np.full(len(data), 1)
    # data["weights"][mask] = 0.0
    wavelengths = 10 ** data["loglam"]
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
    final_residuals = data[col].to_numpy() - np.array(
        optimal_smooth.get_optimal().get_smoothed()
    )

    (fig, smooth_ax, cve_ax) = create_figure_and_axes()

    cve_ax.plot(
        lambdas,
        cross_validation_errors,
        color="red",
        label="Cross validation",
        marker=".",
        markersize=8,
    )

    cve_ax.set_xscale("log")
    # cve_ax.set_yscale("log")
    cve_ax.spines["bottom"].set_color(axis_color)
    cve_ax.spines["top"].set_color(axis_color)
    cve_ax.spines["right"].set_color(axis_color)
    cve_ax.spines["left"].set_color(axis_color)
    cve_ax.set_xlabel("λ", color=axis_color, fontsize=16)
    cve_ax.set_ylabel("RCVE", color=axis_color, fontsize=14)
    cve_ax.tick_params(
        axis="y", direction="in", color=axis_color, labelcolor=axis_color
    )
    cve_ax.tick_params(
        axis="x", direction="in", color=axis_color, labelcolor=axis_color
    )
    cve_ax.grid(True, ls="--", alpha=0.6)

    cve_ax.set_facecolor("#00002a")
    plt.show(block=False)

    smooth_ax.spines["bottom"].set_color(axis_color)
    smooth_ax.spines["top"].set_color(axis_color)
    smooth_ax.spines["right"].set_color(axis_color)
    smooth_ax.spines["left"].set_color(axis_color)
    smooth_ax.set_xlabel("Wavelenghts / Ångströms", color=axis_color, fontsize=14)
    smooth_ax.set_ylabel("Flux / (10-17 erg/cm2/s/Å)", color=axis_color, fontsize=14)
    smooth_ax.tick_params(
        axis="y", direction="in", color=axis_color, labelcolor=axis_color
    )
    smooth_ax.tick_params(
        axis="x", direction="in", color=axis_color, labelcolor=axis_color
    )

    smooth_ax.grid(True, ls="--", alpha=0.6)
    smooth_ax.set_facecolor("#00002a")
    # ax1.set_xlim(0, 50)
    #
    smooth_ax.set_xlim(3800, 5000)
    smooth_ax.set_ylim(-0.5, 15)
    smooth_ax.plot(
        wavelengths,
        data[col],
        color="#59f176",
        marker=".",
        label="Measured",
        alpha=0.5,
        markersize=8,
    )
    # smooth_ax.scatter(
    #     data.index,
    #     data[col],
    #     color="yellow",
    #     # marker=".",
    #     label="Measured",
    #     alpha=0.75,
    #     s=20,
    # )

    smooth_ax.plot(
        wavelengths,
        smoothed,
        color="red",
        lw=2,
        label="λ = {:.0f}".format(optimal_smooth.get_optimal().get_lambda()),
        solid_capstyle="round",
    )
    smooth_ax.legend()
    fig.tight_layout()
    plt.savefig(
        "cross_validation_article/optical_spectra.png",
        dpi=800,
        bbox_inches="tight",
    )
    plt.show(block=False)


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
    final_residuals = data[col].to_numpy() - np.array(
        optimal_smooth.get_optimal().get_smoothed()
    )

    (fig, smooth_ax, cve_ax) = create_figure_and_axes()
    cve_ax.plot(
        lambdas,
        cross_validation_errors,
        color="red",
        marker=".",
        markersize=8,
    )

    cve_ax.set_xscale("log")

    cve_ax.set_xlabel("λ", color=axis_color, fontsize=16)
    cve_ax.set_ylabel("RCVE", color=axis_color, fontsize=14)

    smooth_ax.set_xlabel("Year", color=axis_color, fontsize=14)
    smooth_ax.set_ylabel("Absolute Humidity / (g/m3)", color=axis_color, fontsize=14)

    smooth_ax.set_ylim(0.6, 2.27)

    # fig.autofmt_xdate()
    smooth_ax.set_xlim(data["Date"].loc[4400], data["Date"].loc[4700])
    smooth_ax.plot(
        data["Date"],
        np.where(nan_filter, np.nan, data[col]),
        color="#59f176",
        marker=".",
        label="Measured",
        alpha=0.6,
        markersize=8,
    )

    smooth_ax.plot(
        data["Date"],
        smoothed,
        color="red",
        lw=2,
        label="λ = {:.0f}".format(optimal_smooth.get_optimal().get_lambda()),
        solid_capstyle="round",
    )
    smooth_ax.legend()
    fig.tight_layout()
    # smooth_ax.xaxis.set_major_locator(mdates.DayLocator())
    plt.savefig(
        "cross_validation_article/absolute_humidity.png",
        dpi=800,
        bbox_inches="tight",
    )

    plt.show()


def create_figure_and_axes():
    (fig, axes) = plt.subplots(
        2, 1, figsize=(9, 6), facecolor="#00002a", gridspec_kw={"height_ratios": [3, 1]}
    )

    for ax in axes:
        ax.spines["bottom"].set_color(axis_color)
        ax.spines["top"].set_color(axis_color)
        ax.spines["right"].set_color(axis_color)
        ax.spines["left"].set_color(axis_color)
        ax.tick_params(
            axis="y", direction="in", color=axis_color, labelcolor=axis_color
        )
        ax.tick_params(
            axis="x", direction="in", color=axis_color, labelcolor=axis_color
        )
        ax.grid(True, ls="--", alpha=0.6)
        ax.set_facecolor("#00002a")

    return (fig, axes[0], axes[1])


if __name__ == "__main__":
    main()
