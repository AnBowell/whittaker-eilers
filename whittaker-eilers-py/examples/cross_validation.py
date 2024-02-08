from whittaker_eilers import WhittakerSmoother
import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt("graph.txt", skiprows=5)
axis_color = "#d0d0fa"

years = data[:, 0]
temp_anom = data[:, 1]
other_smoothed = data[:, 2]

whittaker_smoother = WhittakerSmoother(lmbda=20, order=2, data_length=len(temp_anom))


res = whittaker_smoother.smooth_and_cross_validate(list(temp_anom))


res = whittaker_smoother.smooth_and_optimise(list(temp_anom))

print(res.get_optimal().get_lambda())


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
ax1.set_xlim(1880, 2020)

ax1.plot(
    years,
    temp_anom,
    color="#fc8d28",
    marker=".",
    label="Measured",
    alpha=0.6,
    markersize=8,
)

ax1.plot(
    years,
    res.get_optimal().get_smoothed(),
    color="#59f176",
    lw=2,
    label="Whittaker",
    solid_capstyle="round",
)
plt.show()
