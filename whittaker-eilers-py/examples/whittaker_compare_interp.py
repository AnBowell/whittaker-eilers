from whittaker_eilers import WhittakerSmoother
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from scipy.ndimage import gaussian_filter1d
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.interpolate import interp1d


SAVE_PLOT = False

axis_color = "#d0d0fa"

data = np.loadtxt("graph.txt", skiprows=5)

years = data[:, 0]
temp_anom = data[:, 1]
other_smoothed = data[:, 2]

whittaker_smoother = WhittakerSmoother(lmbda=20, order=2, data_length=len(temp_anom))

whit_temp_anom_no_gaps = whittaker_smoother.smooth(temp_anom)

gauss_temp_anom_no_gaps = gaussian_filter1d(temp_anom, 2.0, order=0)

sav_gol_temp_anom_no_gaps = savgol_filter(temp_anom, window_length=35, polyorder=5)


lowes_temp_anom_no_gaps = lowess(
    temp_anom,
    years,
    frac=1.0 / 12.0,
    it=5,
    return_sorted=False,
    missing="drop",
    xvals=years,
)


weights = [1.0] * len(years)

for i in range(1, len(temp_anom)):
    if (i % 2 == 0) and i != len(temp_anom) - 1:
        temp_anom[i] = np.nan
        weights[i] = 0.0

    if i > 5 and i < 5 + 15:
        temp_anom[i] = np.nan
        weights[i] = 0.0

    if i > 96 and i < 96 + 30:
        temp_anom[i] = np.nan
        weights[i] = 0.0


whittaker_smoother = WhittakerSmoother(
    lmbda=20, order=2, data_length=len(temp_anom), weights=weights
)

interpolator = interp1d(
    years[~np.isnan(temp_anom)], temp_anom[~np.isnan(temp_anom)], kind="linear"
)

interpolated_data = interpolator(years)

whit_temp_anom = whittaker_smoother.smooth(list(np.nan_to_num(temp_anom)))

gauss_temp_anom = gaussian_filter1d(interpolated_data, 2.0, order=0)

sav_gol_temp_anom = savgol_filter(interpolated_data, window_length=35, polyorder=5)

lowes_temp_anom = lowess(
    interpolated_data,
    years,
    frac=1.0 / 12.0,
    it=5,
    return_sorted=False,
    missing="drop",
    xvals=years,
)

whit_mse = (
    np.mean((np.asarray(whit_temp_anom) - np.asarray(whit_temp_anom_no_gaps)) ** 2)
    ** 0.5
)
gauss_mse = np.mean((gauss_temp_anom - gauss_temp_anom_no_gaps) ** 2) ** 0.5
sav_golay_mse = np.mean((sav_gol_temp_anom - sav_gol_temp_anom_no_gaps) ** 2) ** 0.5
lowess_mse = np.mean((lowes_temp_anom - lowes_temp_anom_no_gaps) ** 2) ** 0.5

print("Whittaker MSE: {} deg".format(whit_mse))
print("Gauss MSE: {} deg".format(gauss_mse))
print("Sav Golay MSE: {} deg".format(sav_golay_mse))
print("Lowess MSE: {} deg".format(lowess_mse))


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
    gauss_temp_anom,
    color="#f003ef",
    lw=2,
    label="Gaussian Kernel",
    solid_capstyle="round",
)
ax1.plot(
    years,
    lowes_temp_anom,
    color="red",
    lw=2,
    label="LOWESS",
    solid_capstyle="round",
)
ax1.plot(
    years,
    sav_gol_temp_anom,
    color="#66b0ff",
    lw=2,
    label="Sav-Golay",
    solid_capstyle="round",
)

ax1.plot(
    years,
    whit_temp_anom,
    color="#59f176",
    lw=2,
    label="Whittaker",
    solid_capstyle="round",
)
plt.legend()

if SAVE_PLOT:
    plt.savefig(
        "whittaker_compare_interp.png",
        dpi=800,
        bbox_inches="tight",
    )
plt.show()
