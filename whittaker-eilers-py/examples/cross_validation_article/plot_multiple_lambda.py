import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from whittaker_eilers import WhittakerSmoother
from astropy.io import fits

axis_color = "#d0d0fa"
face_color = "#00002a"


def main():
    plot_optical_spectra()


def plot_optical_spectra():
    col = "flux"
    with fits.open("cross_validation_article/spec-1939-53389-0138.fits") as data:
        data = pd.DataFrame(data[1].data)

    # print(data["and_mask"].to_list())
    # mask = data["and_mask"] > 65552
    data["weights"] = np.full(len(data), 1)
    # data["weights"][mask] = 0.0
    wavelengths = 10 ** data["loglam"]

    print(wavelengths)
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

    (fig, smooth_ax) = create_figure_and_axes()

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
        color="#fc8d28",
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
    for _lambda, colour, string_lambda in zip(
        [1e1, 1e4, 1e6], ["#66b0ff", "red", "#59f176"], ["$10^1$", "$10^4$", "$10^6$"]
    ):
        smoother.update_lambda(_lambda)
        smooth = smoother.smooth(data[col].to_list())
        smooth_ax.plot(
            wavelengths,
            smooth,
            color=colour,
            lw=2,
            label="λ={}".format(string_lambda),
            solid_capstyle="round",
        )

    smooth_ax.legend()
    fig.tight_layout()
    plt.savefig(
        "cross_validation_article/optical_spectra_multiple_lambda.png",
        dpi=800,
        bbox_inches="tight",
    )
    plt.show()


def create_figure_and_axes():
    (fig, ax) = plt.subplots(figsize=(8, 5), facecolor="#00002a")

    ax.spines["bottom"].set_color(axis_color)
    ax.spines["top"].set_color(axis_color)
    ax.spines["right"].set_color(axis_color)
    ax.spines["left"].set_color(axis_color)
    ax.tick_params(axis="y", direction="in", color=axis_color, labelcolor=axis_color)
    ax.tick_params(axis="x", direction="in", color=axis_color, labelcolor=axis_color)
    ax.grid(True, ls="--", alpha=0.6)
    ax.set_facecolor("#00002a")

    return (fig, ax)


if __name__ == "__main__":
    main()
