from typing import Optional, Iterable

# Bit of a pain having to handcraft these! Especially with the docs.
class WhittakerSmoother:
    """A new Whittaker-Eilers smoother and interpolator.

    The smoother is configured through it's `lambda` and it's `order`. `Lambda` controls the smoothness of the data and `order` controls
    the order of which the penalities are applied (generally 2 - 4). The smoother can then be configured to weight measurements between 0 and 1
    to interpolate (0 weight) or to complete trust (1 weight) the measurement. The smoother can handle equally spaced measurements by simply not passing
    an `x_input` or unequally spaced data by providing the sampling times/positions as `x_input`.

    The smoother parameters can be updated using the provided functions to avoid remaking this costly struct. The only time the WhittakerSmoother should be
    remade is when the data length has changed, or a different sampling rate has been provided.

    Parameters
    ----------
     lambda : Controls the smoothing strength, the larger, the smoother. Must be positive.
     order : The order of the filter. Must be positive.
     data_length : The length of the data which is to be smoothed. Must be positive.
     x_input : The time/position at which the y measurement was taken. Used to smooth unequally spaced data. Must be monotonically increasing.
     weights : The weight of each y measurement."""

    def __init__(
        self,
        lmbda: float,
        order: int,
        data_length: int,
        x_input: Optional[list] = None,
        weights: Optional[list] = None,
    ) -> None: ...
    def get_order(self) -> int:
        """Retrieve the smoother's current lambda."""
    ...
    def get_lambda(self) -> float:
        """Retrieve the smoother's current lambda."""
        ...
    def get_data_length(self) -> int:
        """Retrieve the smoother's current order."""
        ...
    def update_weights(self, weights: list) -> None:
        """Updates the weights of the data to be smoothed.
        The length of weights should be equal to that of the data you are to smooth. The values of the weights should fall between 0 and 1.

        Parameters
        ----------
        weights : The weights of the measurements to be smoothed. The smaller the weight the more the measurement will be ignored. Setting a weight to 0 results in interpolation.
        """
        ...
    def update_order(self, order: int) -> None:
        """Updates the order of the Whittaker-Eilers smoother.

        Efficiently updates the order at which the Whittaker will use to smooth the data.

        Parameters
        ----------
        order : The order to smooth."""
        ...
    def update_lambda(self, lmbda: float) -> None:
        """Updates the smoothing constant `lambda` of the Whittaker-Eilers smoother.

        Efficiently update the target smoothness of the Whittaker smoother. The larger the `lambda`, the smoother the data.

        Parameters
        ----------
        lambda : The smoothing constant of the Whittaker-Eilers smoother.
        """
        ...
    def smooth(self, y_vals: list) -> list:
        """Run Whittaker-Eilers smoothing and interpolation.

        This function actually runs the solver which results in the smoothed data. If you just wish to continuously smooth
        data of different y values with the sample rate remaining the same, simply call this function with different data. Remaking the `WhittakerSmoother` class
        will result in a lot of overhead.

        Parameters
        ----------
        vals_y : The values which are to be smoothed and interpolated by the Whittaker-Eilers smoother.

        Returns
        -------
        The smoothed and interpolated data."""
        ...
