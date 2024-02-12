import numpy as np
from whittaker_eilers import WhittakerSmoother
import matplotlib.pyplot as plt

axis_color = "#d0d0fa"
face_color = "#00002a"
data_length = 1000


def main():
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

        actual_errors = [
            np.sqrt(np.mean((original_y - np.array(series)) ** 2))
            for series in smoothed_data
        ]

        print(
            "Cross validation chosen lambda: {}".format(
                lambdas[np.argmin(cross_validation_errors)]
            )
        )

        print("RMSE Chosen lambda: {}".format(lambdas[np.argmin(actual_errors)]))

        cve_ax = next(cve_axes_iter)
        [spine.set_color(axis_color) for (_, spine) in cve_ax.spines.items()]

        cve_ax.plot(
            lambdas,
            cross_validation_errors,
            color="#fc8d28",
            label="Cross validation",
            marker=".",
            markersize=8,
        )
        ax2 = cve_ax.twinx()
        ax2.plot(
            lambdas,
            actual_errors,
            color="#66b0ff",
            label="RMSE",
            marker=".",
            markersize=8,
        )

        ax2.tick_params(
            axis="y", direction="in", color=axis_color, labelcolor=axis_color
        )
        ax2.tick_params(
            axis="x", direction="in", color=axis_color, labelcolor=axis_color
        )

        cve_ax.set_xscale("log")
        # cve_ax.set_yscale("log")

        cve_ax.tick_params(
            axis="y", direction="in", color=axis_color, labelcolor=axis_color
        )
        cve_ax.tick_params(
            axis="x", direction="in", color=axis_color, labelcolor=axis_color
        )
        cve_ax.grid(True, ls="--", alpha=0.6)
        cve_ax.set_facecolor("#00002a")

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

        smoothed_ax.plot(x, original_y, label="Original", color="white")
        smoothed_ax.plot(
            x,
            y_with_noise,
            color="#59f176",
            marker=".",
            label="Measured",
            alpha=0.6,
            markersize=8,
        )

        smoothed_ax.plot(
            x,
            optimal_smooth.get_optimal().get_smoothed(),
            color="red",
            lw=2,
            label="Whittaker",
            solid_capstyle="round",
        )

        match counter:
            case 0:
                smoothed_ax.set_ylim(-1.25, 1.25)
            case 1:
                smoothed_ax.set_ylim(-1.25, 1.25)
            case 2:
                smoothed_ax.set_ylim(-3.25, 3.25)
            case 3:
                smoothed_ax.set_ylim(-10, 10)
            case _:
                pass
        smoothed_fig.supxlabel("x / Radians", color=axis_color, fontsize=18)
        y_label = smoothed_fig.supylabel("Amplitude", color=axis_color, fontsize=18)
        y_label.set_x(0.07)
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
