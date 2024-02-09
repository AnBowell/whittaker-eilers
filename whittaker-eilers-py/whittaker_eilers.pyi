from typing import Optional, List

class CrossValidationResult:
    def get_lambda(self) -> float: ...
    def get_smoothed(self) -> List[float]: ...
    def get_cross_validation_error(self) -> float: ...
    ...

class OptimisedSmoothResult:
    def get_optimal(self) -> CrossValidationResult: ...
    def get_all(self) -> List[CrossValidationResult]: ...

# Bit of a pain having to handcraft these! Especially with the docs.
class WhittakerSmoother:
    """A new Whittaker-Eilers smoother and interpolator.

    The smoother is configured through it's `lambda` and it's `order`. `Lambda` controls the smoothness of the data (1e2~1e4) and `order` controls
    the order of which the penalities are applied (generally 2~4). The smoother can then be configured to weight measurements between 0 and 1
    to interpolate (0 weight) or to complete trust (1 weight) the measurement. The smoother can handle equally spaced measurements by simply not passing
    an `x_input` or unequally spaced data by providing the sampling times/positions as `x_input`.

    The smoother parameters can be updated using the provided functions to avoid remaking this costly struct. The only time the WhittakerSmoother should be
    remade is when the data length has changed, or a different sampling rate has been provided.

    Parameters
    ----------
     lmbda : Controls the smoothing strength, the larger, the smoother. Try 1e2~2e4 to start with and adjust based on the result. `lmbda` must be positive.
     order : The order of the filter. Try 2~4 to start with. Order must be positive.
     data_length : The length of the data which is to be smoothed. Must be positive.
     x_input : The time/position at which the y measurement was taken. Used to smooth unequally spaced data. Must be monotonically increasing.
     weights : The weight of each y measurement."""

    def __init__(
        self,
        lmbda: float,
        order: int,
        data_length: int,
        x_input: Optional[List] = None,
        weights: Optional[List] = None,
    ) -> None: ...
    def get_order(self) -> int:
        """Retrieve the smoother's current order."""
    ...
    def get_lambda(self) -> float:
        """Retrieve the smoother's current lambda."""
        ...
    def get_data_length(self) -> int:
        """Retrieve the smoother's current length."""
        ...
    def update_weights(self, weights: List) -> None:
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
        lmbda : The smoothing constant of the Whittaker-Eilers smoother.
        """
        ...
    def smooth(self, y_vals: List[float]) -> List:
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

    def smooth_and_cross_validate(self, y_vals: List[float]) -> CrossValidationResult:
        """Run Whittaker-Eilers smoothing, interpolation and cross validation.

        This function will run the smoother and assess the cross validation error on the result. This is defined in Eiler's
        2003 paper: "A Perfect Smoother".  It involves computing the "hat matrix" or "smoother matrix" which inverses a sparse matrix. The
        inverse of a sparse matrix is usually dense, so this function will take much longer to run in comparison to just running `smooth`.

        Parameters
        ----------
        y_vals: The values which are to be smoothed and interpolated and have their cross validation error calculated.

        Returns
        -------
        CrossValidationResult: The smoothed data, lambda it was smoothed at, and the cross validation error.

        """
    ...

    def smooth_optimal(
        self, y_vals: List[float], break_serial_correlation: bool = True
    ) -> OptimisedSmoothResult:
        """Runs Whittaker-Eilers smoothing for a variety of lambdas and selects the optimally smoothed time series.

        This function runs the smoother for lambdas varying from 1e-2 to 1e8 in logarithmic steps of 0.5. It computes the
        hat/smoother matrix and finds the optimal lambda for the data. If the time-series exhibits serial correlation the optimal
        lambda can be very small and mean the smoothed data doesn't differ from the input data. To avoid this, use `break_serial_correlation = true`

        It will return the smoothed data, lambda, and cross validation error for each lambda tested!

        As the smoother matrix requires the inversion of a sparse matrix (which usually becomes a dense matrix), this code is extremely slow compared to smoothing
        with a known lambda. Use sparingly!

        Parameters
        ----------
        y_input: The values which are to be smoothed, interpolated, and cross validated for a variety of lambdas.
        break_serial_correlation: Defaults to `true`. Without it, data that exhibits serial correlation is barely smoothed.

        Returns
        -------
        OptimisedSmoothResult: The smoothed data, lambda, and error for each tested lambda. Calling get_optimal, returns the best smoothed series.
        """
    ...
