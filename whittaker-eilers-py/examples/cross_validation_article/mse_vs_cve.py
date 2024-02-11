import numpy as np
from whittaker_eilers import WhittakerSmoother
import matplotlib.pyplot as plt

axis_color = "#d0d0fa"
face_color = "#00002a"
data_length = 1000


def main():
    for scale in [0.0001, 0.001, 0.01, 1.0, 5.0]:
        x, original_y, y_with_noise = generate_data(data_length, scale)

        smoother = WhittakerSmoother(1, 2, data_length)  # x_input=x)

        optimal_smooth = smoother.smooth_optimal(
            y_with_noise, break_serial_correlation=False
        )

        (fig, ax1) = plt.subplots(figsize=(8, 4), facecolor="#00002a")
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
        ax1.plot(
            lambdas,
            cross_validation_errors,
            color="#fc8d28",
            label="Cross validation",
            marker=".",
            markersize=8,
        )
        ax2 = ax1.twinx()
        ax2.plot(
            lambdas,
            actual_errors,
            color="blue",
            label="RMSE",
            marker=".",
            markersize=8,
        )
        ax1.set_xscale("log")
        ax1.set_yscale("log")
        ax1.spines["bottom"].set_color(axis_color)
        ax1.spines["top"].set_color(axis_color)
        ax1.spines["right"].set_color(axis_color)
        ax1.spines["left"].set_color(axis_color)

        ax1.tick_params(
            axis="y", direction="in", color=axis_color, labelcolor=axis_color
        )
        ax1.tick_params(
            axis="x", direction="in", color=axis_color, labelcolor=axis_color
        )
        ax1.grid(True, ls="--", alpha=0.6)
        ax1.set_facecolor("#00002a")
        plt.show(block=False)

        (fig, ax1) = plt.subplots(figsize=(8, 4), facecolor="#00002a")

        ax1.spines["bottom"].set_color(axis_color)
        ax1.spines["top"].set_color(axis_color)
        ax1.spines["right"].set_color(axis_color)
        ax1.spines["left"].set_color(axis_color)
        ax1.set_xlabel("Year", color=axis_color)
        ax1.set_ylabel("Temperature Anomaly / °C", color=axis_color)
        ax1.tick_params(
            axis="y", direction="in", color=axis_color, labelcolor=axis_color
        )
        ax1.tick_params(
            axis="x", direction="in", color=axis_color, labelcolor=axis_color
        )
        ax1.grid(True, ls="--", alpha=0.6)
        ax1.set_facecolor("#00002a")
        # ax1.set_xlim(0, 2 * np.pi)

        ax1.plot(x, original_y, label="Original", color="white")
        ax1.plot(
            x,
            y_with_noise,
            color="#fc8d28",
            marker=".",
            label="Measured",
            alpha=0.6,
            markersize=8,
        )

        ax1.plot(
            x,
            optimal_smooth.get_optimal().get_smoothed(),
            color="#59f176",
            lw=2,
            label="Whittaker",
            solid_capstyle="round",
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
