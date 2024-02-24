import numpy as np
from whittaker_eilers import WhittakerSmoother
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import FormatStrFormatter

axis_color = "#d0d0fa"
face_color = "#00002a"
data_length = 1000


def main():
    np.random.seed(9243)
    cve_fig, cve_axes = plt.subplots(
        2,
        2,
        figsize=(16, 8),
        sharex=True,
        # sharey=True,
        facecolor=face_color,
        gridspec_kw={"wspace": 0.15, "hspace": 0.15},
    )
    cve_axes_iter = iter(cve_axes.flatten())
    pse_fig, mse_axes = plt.subplots(
        2,
        2,
        figsize=(16, 8),
        sharex=True,
        # sharey=True,
        facecolor=face_color,
        gridspec_kw={"wspace": 0.15, "hspace": 0.15},
    )
    pse_axes_iter = iter(mse_axes.flatten())
    smoothed_fig, smoothed_axes = plt.subplots(
        2,
        2,
        figsize=(16, 8),
        sharex=True,
        # sharey=True,
        facecolor=face_color,
        gridspec_kw={"wspace": 0, "hspace": 0},
    )
    smoothed_axes_iter = iter(smoothed_axes.flatten())

    root_mean_squared_errors_y = []
    cross_validation_errors_x = []

    for counter, scale in enumerate([0.01, 0.1, 1.0, 5.0]):
        x, original_y, y_with_noise = generate_data(data_length, scale)

        smoother = WhittakerSmoother(1, 2, data_length)  # x_input=x)

        optimal_smooth = smoother.smooth_optimal(
            y_with_noise, break_serial_correlation=False
        )

        (cross_validation_errors, smoothed_data, lambdas) = zip(
            *[
                (res.get_cross_validation_error(), res.get_smoothed(), res.get_lambda())
                for res in optimal_smooth.get_all()
            ]
        )

        actual_errors = np.array(
            [
                np.sqrt(np.mean((original_y - np.array(series)) ** 2))
                for series in smoothed_data
            ]
        )

        sigmas = np.array(
            [np.mean((original_y - np.array(series)) ** 2) for series in smoothed_data]
        )

        print(
            "Cross validation chosen lambda: {}".format(
                lambdas[np.argmin(cross_validation_errors)]
            )
        )

        print("RMSE Chosen lambda: {}".format(lambdas[np.argmin(actual_errors)]))

        cve_ax = next(cve_axes_iter)
        [spine.set_color(axis_color) for (_, spine) in cve_ax.spines.items()]  #
        pse_ax = next(pse_axes_iter)
        [spine.set_color(axis_color) for (_, spine) in pse_ax.spines.items()]

        cve_plot = pse_ax.plot(
            lambdas,
            np.array(cross_validation_errors) ** 2,
            color="#59f176",
            label="RCVE",
            marker=".",
            markersize=8,
        )
        rmse_plot = pse_ax.plot(
            lambdas,
            actual_errors**2 + scale**2,
            color="red",
            label="RMSE",
            marker=".",
            markersize=8,
        )

        cve_plot = cve_ax.plot(
            lambdas,
            np.array(cross_validation_errors),
            color="#59f176",
            label="RCVE",
            marker=".",
            markersize=8,
        )
        ax2 = cve_ax.twinx()
        rmse_plot = ax2.plot(
            lambdas,
            np.array(actual_errors),
            color="red",
            label="RMSE",
            marker=".",
            markersize=8,
        )
        [spine.set_color(axis_color) for (_, spine) in ax2.spines.items()]

        ax2.tick_params(axis="y", direction="in", color="red", labelcolor=axis_color)
        ax2.tick_params(axis="x", direction="in", color="red", labelcolor=axis_color)

        ax2.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
        cve_ax.set_xscale("log")
        pse_ax.set_xscale("log")

        pse_ax.tick_params(
            axis="y", direction="in", color=axis_color, labelcolor=axis_color
        )
        pse_ax.tick_params(
            axis="x", direction="in", color=axis_color, labelcolor=axis_color
        )

        cve_ax.yaxis.set_major_locator(MaxNLocator(nbins=4, integer=False))
        # cve_ax.set_yscale("log")
        cve_ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
        cve_ax.tick_params(
            axis="y", direction="in", color="#59f176", labelcolor=axis_color
        )
        cve_ax.tick_params(
            axis="x", direction="in", color="#59f176", labelcolor=axis_color
        )
        cve_ax.grid(True, ls="--", alpha=0.3, color="#59f176")
        pse_ax.grid(True, ls="--", alpha=0.5)
        ax2.grid(True, ls="--", alpha=0.3, color="red")
        cve_ax.set_facecolor("#00002a")
        pse_ax.set_facecolor("#00002a")
        smoothed_ax = next(smoothed_axes_iter)
        [spine.set_color(axis_color) for (_, spine) in smoothed_ax.spines.items()]

        # smoothed_ax.set_xlabel("x / Radians", color=axis_color)
        # smoothed_ax.set_ylabel("Amplitude", color=axis_color)
        smoothed_ax.tick_params(
            axis="y", direction="in", color=axis_color, labelcolor=axis_color
        )
        smoothed_ax.tick_params(
            axis="x", direction="in", color=axis_color, labelcolor=axis_color
        )
        smoothed_ax.grid(True, ls="--", alpha=0.6)
        smoothed_ax.set_facecolor("#00002a")
        # ax1.set_xlim(0, 2 * np.pi)

        smoothed_ax.plot(
            x,
            y_with_noise,
            color="#59f176",
            marker=".",
            label="Measured",
            alpha=0.6,
            markersize=8,
        )
        smoothed_ax.plot(x, original_y, label="Original", color="#f003ef")
        smoothed_ax.plot(
            x,
            optimal_smooth.get_optimal().get_smoothed(),
            color="red",
            lw=2,
            label="Whittaker",
            solid_capstyle="round",
        )

        root_mean_squared_errors_y.append(actual_errors)
        cross_validation_errors_x.append(cross_validation_errors)

        match counter:
            case 0:
                smoothed_ax.set_ylim(-1.25, 1.25)
                smoothed_ax.legend(fontsize=14)
                lns = cve_plot + rmse_plot
                labs = [l.get_label() for l in lns]
                cve_ax.legend(lns, labs, fontsize=14)
                cve_ax.set_ylabel("RCVE", fontsize=14, color=axis_color)

            case 1:
                smoothed_ax.set_ylim(-1.25, 1.25)
                # smoothed_ax.yaxis.set_label_position("right")
                # smoothed_ax.yaxis.tick_right()
                smoothed_ax.yaxis.set_tick_params(labelleft=False)

                ax2.set_ylabel("RMSE", fontsize=14, color=axis_color)

            case 2:
                smoothed_ax.set_ylim(-10.0, 10.0)
                cve_ax.set_ylabel("RCVE", fontsize=14, color=axis_color)

            case 3:
                smoothed_ax.set_ylim(-10, 10)
                smoothed_ax.yaxis.set_tick_params(labelleft=False)
                ax2.set_ylabel("RMSE", fontsize=14, color=axis_color)
                # smoothed_ax.yaxis.set_label_position("right")
                # smoothed_ax.yaxis.tick_right()
            case _:
                pass
        smoothed_fig.supxlabel("x / Radians", color=axis_color, fontsize=18)
        y_label = smoothed_fig.supylabel("Amplitude", color=axis_color, fontsize=18)
        y_label.set_x(0.07)

        cve_fig.supxlabel("λ", color=axis_color, fontsize=18)
        # y_label_cve = cve_fig.supylabel("CVE", color=axis_color, fontsize=18)
        # y_label_cve.set_x(0.09)

        # y_label_cve = cve_fig.supylabel("RMSE", color=axis_color, fontsize=18)
        # y_label_cve.set_x(0.96)
    # smoothed_fig.tight_layout()
    # cve_fig.tight_layout()
    # smooth_ax.xaxis.set_major_locator(mdates.DayLocator())
    smoothed_fig.savefig(
        "cross_validation_article/smoothed_rmse_compare.png",
        dpi=600,
        bbox_inches="tight",
    )
    cve_fig.savefig(
        "cross_validation_article/cve_vs_rmse.png",
        dpi=800,
        bbox_inches="tight",
    )
    pse_fig.savefig(
        "cross_validation_article/pse.png",
        dpi=800,
        bbox_inches="tight",
    )
    plt.show(block=False)

    for cross_val, rmse in zip(cross_validation_errors_x, root_mean_squared_errors_y):
        # ax1.scatter(cross_val, rmse)
        print(np.corrcoef(cross_val, rmse))
    # ax1.set_yscale("log")
    # ax1.set_xscale("log")
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
