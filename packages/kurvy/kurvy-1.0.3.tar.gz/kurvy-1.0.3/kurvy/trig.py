import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import copy
from kurvy import utils


def make_trig_data(X_range, n_samples, params=None, fuzz=None, seed=None):
    """
    Generates random trigonometric sample data.

    Args:
    -----

        X_range (2-tuple): desired X-value range for data.

        n_samples (int): number of samples to generate.

    Kwargs:
    -------

        params (5-tuple, default = None): specifc parameter values, if required.

        fuzz (int, default = None): how much random 'fuzziness' to apply to the
        data generator, in order to introduce synthetic error. Acceptable values
        are None, 1, 2, or 3; with the severity of the error increasing with the
        value given.

        seed (int, default = None): value on which to set the random seed for
        reproducibility.

    Returns:
    --------

        a (float): value generated for amplitude.

        b (float): value generated for period.

        c (float): value generated for phase shift.

        d (float): value generated for vertical offset.

        e (float): value generated for linear trend.

        X (1-D array): X data.

        Y_fuzzy (1-D array): Y_data.
    """

    rng = np.random.default_rng(seed)

    if not isinstance(X_range, tuple):
        raise ValueError(
            f"Expected 2-tuple for 'X_range'; got {type(X_range)}."
        )
    if not all([isinstance(i, int) for i in X_range]):
        raise ValueError(f"'X_range' must be tuple of integers: (min, max).")
    if not isinstance(n_samples, int):
        raise ValueError(
            f"Expected integer for 'n_samples'; got {type(n_samples)}."
        )
    if fuzz:
        if not isinstance(fuzz, int) or (not 0 <= fuzz <= 3):
            raise ValueError(f"'fuzz' must be integer in [0,3].")
    if params:
        if not isinstance(params, tuple):
            raise ValueError(
                f"Expected 5-tuple for 'params'; got {type(params)}."
            )
        if len(params) != 5:
            raise ValueError(
                f"Expected 5-tuple for 'params'; got {len(params)}-tuple."
            )

        a, b, c, d, e = params

    else:
        mu = np.mean(X_range)
        std = mu * 0.5

        a = np.round(rng.normal(mu, std), 3)
        b = np.round(
            rng.integers(np.floor(X_range[1] * 0.75)) + rng.random(), 3
        )
        c = np.round(rng.integers(np.floor(b)) + rng.random(), 3)
        d = np.round(rng.integers(np.floor(X_range[1] * 2)) + rng.random(), 3)
        e = np.round(rng.uniform(-10, 10), 3)

    X = np.linspace(X_range[0], X_range[1], n_samples)

    cos_val = np.cos(2 * np.pi * X / b - c)
    Y = a * cos_val + d + e * X

    # add random error (fuzz)
    if fuzz == 1:
        Y_fuzzy = utils.add_fuzz(Y, 1, 0, X_range[1] * 0.01, seed=seed)

    elif fuzz == 2:
        Y_fuzzy = utils.add_fuzz(Y, 1, 0, X_range[1] * 0.01, seed=seed)
        Y_fuzzy = utils.add_fuzz(Y_fuzzy, 0.3, 0, X_range[1] * 0.075, seed=seed)

    elif fuzz == 3:
        Y_fuzzy = utils.add_fuzz(Y, 1, 0, X_range[1] * 0.01, seed=seed)
        Y_fuzzy = utils.add_fuzz(Y_fuzzy, 0.3, 0, X_range[1] * 0.075, seed=seed)
        Y_fuzzy = utils.add_fuzz(Y_fuzzy, 0.05, 0, X_range[1] * 0.3, seed=seed)

    else:
        Y_fuzzy = Y

    return (a, b, c, d, e), X, Y_fuzzy


class ParamEstimator:

    """
    Trigonometric data parameter estimator.

    Attributes:
    -----------

        X_data (1-D array): X data array.

        Y_data (1-D array): Y data array.

        trend (float): estimated linear trend parameter for data.

        offset (float): estimated vertical offset parameter for data.

        Y_reg (1-D array): data fit to regression line.

        p0 (2-tuple): cordinates for first point of data.

        start_sign (int): sign (positive or negative) for first data point.

        p1 (2-tuple): cordinates for first intersection with regression line.

        p2 (2-tuple): cordinates for second intersection with regression line.

        p3 (2-tuple): cordinates for third intersection with regression line.

        period (float): estimated period parameter for data.

        q_dist (float): quater of estimated period value.

        peak_0_reg (2-tuple): coordinates for first data peak cast onto
        regression line.

        peak_0 (2-tuple): coordinates for first data peak.

        amplitude (float): estimated period parameter for data.

        phase_shift (float): estimated phase shift parameter for data.

    Methods:
    --------

        _period_estimation: estimates curve period.

        fit: fits estimator to data.

        plot: plots data and annotations showing estimated parameters.
    """

    def __init__(self):
        """
        Initialises the ParamEstimator object.
        """

    def _period_estimation(self, X_data, Y_data, Y_reg, window_size):
        """
        Estimates curve period by locating boundry points at which the
        difference between the rolling mean of the data and the data fit to a
        regression line changes sign.

        Args:
        -----

            X_data (1-D array): X data array.

            Y_data (1-D array): Y data array.

            Y_reg (1-D array): data fit to regression line.

            window_size (int): number of samples to include in rolling mean.

        Returns:
        --------

            p1 (2-tuple): cordinates for first intersection with regression
            line.

            p2 (2-tuple): cordinates for second intersection with regression
            line.

            p3 (2-tuple): cordinates for third intersection with regression
            line.
        """

        window = window_size
        window_start = 0

        Y_window = Y_data[0:window]
        Y_reg_window = Y_reg[0:window]
        self.start_sign = np.sign(np.mean(Y_window - Y_reg_window))
        start_sign = self.start_sign

        Y_window_n = Y_data[window_start:window]
        Y_reg_window_n = Y_reg[window_start:window]
        window_sign = np.sign(np.mean(Y_window_n - Y_reg_window_n))

        while window_sign == start_sign:
            window += 1
            window_start += 1
            Y_window_n = Y_data[window_start:window]
            Y_reg_window_n = Y_reg[window_start:window]
            window_sign = np.sign(np.mean(Y_window_n - Y_reg_window_n))
        p1 = int(np.mean((window_start, window)))

        start_sign = np.sign(np.mean(Y_window_n - Y_reg_window_n))
        while window_sign == start_sign:
            window += 1
            window_start += 1
            Y_window_n = Y_data[window_start:window]
            Y_reg_window_n = Y_reg[window_start:window]
            window_sign = np.sign(np.mean(Y_window_n - Y_reg_window_n))
        p2 = int(np.mean((window_start, window)))

        start_sign = np.sign(np.mean(Y_window_n - Y_reg_window_n))
        while window_sign == start_sign:
            window += 1
            window_start += 1
            Y_window_n = Y_data[window_start:window]
            Y_reg_window_n = Y_reg[window_start:window]
            window_sign = np.sign(np.mean(Y_window_n - Y_reg_window_n))
        p3 = int(np.mean((window_start, window)))

        return p1, p2, p3

    def fit(self, X_data, Y_data, window_size=100, sort_data=False):
        """
        Fits the initialised parameter estimator to data.

        Args:
        -----

            X_data (1-D array): X data array.

            Y_data (1-D array): Y data array.

        Kwargs:
        -------

            window_size (int, default = 100): number of samples to include in
            rolling mean for period estimation.

            sort_data (bool, default = False): whether or not to sort X and Y
            data (by X value). Note that the estimator expects data to be
            sorted.

        Yields:
        -------

            self.X_data

            self.Y_data

            self.trend

            self.offset

            self.Y_reg

            self.p0

            self.start_sign

            self.p1

            self.p2

            self.p3

            self.period

            self.q_dist

            self.peak_0_reg

            self.peak_0

            self.amplitude

            self.phase_shift
        """

        if sort_data:
            XY_data = np.dstack((X_data, Y_data))[0]
            self.X_data = XY_data[np.argsort(XY_data[:, 0])][:, 0]
            self.Y_data = XY_data[np.argsort(XY_data[:, 0])][:, 1]

        else:
            self.X_data = X_data
            self.Y_data = Y_data

        # compute regression line for X points
        self.trend, self.offset = utils.lin_reg(self.X_data, self.Y_data)
        self.Y_reg = self.X_data * self.trend + self.offset

        self.p0 = (self.X_data[0], self.Y_reg[0])

        p1, p2, p3 = self._period_estimation(
            self.X_data, self.Y_data, self.Y_reg, window_size
        )

        self.p1 = (self.X_data[p1], self.X_data[p1] * self.trend + self.offset)
        self.p2 = (self.X_data[p2], self.X_data[p2] * self.trend + self.offset)
        self.p3 = (self.X_data[p3], self.X_data[p3] * self.trend + self.offset)

        self.period = self.X_data[p3] - self.X_data[p1]
        self.q_dist = self.period / 4

        # find first peak
        # (assumed to be a quarter of the period back from p1)
        # first peak cast onto regression line
        if self.p1[0] - self.q_dist < 0:
            self.peak_0_reg = (
                self.p1[0] - self.q_dist + self.period,
                (self.p1[0] - self.q_dist + self.period) * self.trend
                + self.offset,
            )
        else:
            self.peak_0_reg = (
                self.p1[0] - self.q_dist,
                (self.p1[0] - self.q_dist) * self.trend + self.offset,
            )

        # find nearest value in X data to computed first peak
        nearest_idx = np.argmin(np.abs(self.X_data - self.peak_0_reg[0]))

        # find coords on regression line for nearest value
        X_peakval = self.X_data[nearest_idx]
        Y_reg_peakval = X_peakval * self.trend + self.offset

        # find coords in Y data for nearest value
        # use mean abs value of points either side to exlcude fuzz
        Y_peakval = np.mean(
            [np.abs(self.Y_data[nearest_idx + i]) for i in range(-5, 5)]
        )

        # set coords value to nearest value
        self.peak_0_reg = (X_peakval, Y_reg_peakval)
        self.peak_0 = (X_peakval, Y_peakval)

        # set amplitude sign based on first section of curve
        abs_amplitude = np.abs(Y_peakval - Y_reg_peakval)
        self.amplitude = abs_amplitude * self.start_sign

        # estimate Y with no phase shift keeping other params fixed
        est_cos_val_c0 = np.cos(2 * np.pi * self.X_data / self.period - 0)
        Y_est_c0 = (
            self.amplitude * est_cos_val_c0
            + self.offset
            + self.trend * self.X_data
        )

        # use smaller window size
        c0_window = int(window_size / 2)
        p1_c0, p2_c0, p3_c0 = self._period_estimation(
            self.X_data, Y_est_c0, self.Y_reg, window_size=c0_window
        )

        mean_shift = np.mean(
            [
                self.X_data[p1] - self.X_data[p1_c0],
                self.X_data[p3] - self.X_data[p3_c0],
            ]
        )

        self.phase_shift = mean_shift / self.period * 2 * np.pi

    def plot(self):
        """
        Plots data with annotations showing estimated parameters.
        """

        fig, ax = plt.subplots(figsize=(12, 4))

        # (sorted) raw data
        ax.scatter(
            self.X_data,
            self.Y_data,
            color="white",
            edgecolors="teal",
            alpha=0.5,
            s=20,
            zorder=-1,
        )

        # regression line
        ax.plot(
            (self.X_data[0], self.X_data[-1]),
            (self.Y_reg[0], self.Y_reg[-1]),
            color="dodgerblue",
            linewidth=3,
            alpha=0.7,
            solid_capstyle="round",
            zorder=1,
        )

        # points of interest
        ax.scatter(
            *self.p1,
            color="white",
            edgecolors="tomato",
            s=60,
            linewidth=2,
            zorder=4,
        )
        ax.scatter(
            *self.p3,
            color="white",
            edgecolors="tomato",
            s=60,
            linewidth=2,
            zorder=4,
        )
        ax.scatter(
            *self.peak_0,
            color="white",
            edgecolors="teal",
            s=60,
            linewidth=2,
            zorder=4,
        )
        ax.scatter(
            *self.peak_0_reg,
            color="white",
            edgecolors="dodgerblue",
            s=60,
            linewidth=2,
            zorder=4,
        )

        # vertical period lines
        ax.axvline(
            x=self.p1[0], color="tomato", alpha=0.9, linestyle="--", zorder=2
        )
        ax.axvline(
            x=self.p3[0], color="tomato", alpha=0.9, linestyle="--", zorder=2
        )

        # regression line trace in period
        ax.plot(
            (self.p1[0], self.p3[0]),
            (self.p1[1], self.p3[1]),
            color="white",
            alpha=1,
            linestyle="--",
            zorder=1,
        )

        # vertical amplitude line
        ax.plot(
            (self.peak_0[0], self.peak_0[0]),
            (self.peak_0_reg[1], self.peak_0[1]),
            color="black",
            linestyle="dotted",
            zorder=3,
        )

        # estimator
        est_cos_val = np.cos(
            2 * np.pi * self.X_data / self.period - self.phase_shift
        )
        Y_est = (
            self.amplitude * est_cos_val
            + self.offset
            + self.trend * self.X_data
        )
        ax.plot(
            self.X_data,
            Y_est,
            color="cyan",
            linewidth=5,
            alpha=0.8,
            solid_capstyle="round",
            zorder=1,
        )

        ax.grid(visible=True)
        ax.set_axisbelow(True)
        plt.show()


class TrigModel:

    """
    Gradient descent algorithm for trigonometric curve approximation.

    Attributes:
    -----------

        smart (bool): boolean flag relating to whether or not smart
        initialization is utilized.

        initial_params (dict): nested dict of parameter starting values and
        trainable/fixed flag.

        params (dict): nested dict of parameter values and trainable/fixed
        flag.

        training_history (2-D array): array containing training records where:
            column 0 contains loss values per epoch,
            column 1 contains r2 values per epoch,
            column 2 contains param "a" values per epoch,
            column 3 contains param "b" values per epoch,
            column 4 contains param "c" values per epoch,
            column 5 contains param "d" values per epoch,
            column 6 contains param "e" values per epoch.

        best_epoch (int): epoch with best performance (optimized loss).

        best_params (1-D array): parameter values with best performance, where:
            element 0 is parameter "a",
            element 1 is parameter "b",
            element 2 is parameter "c",
            element 3 is parameter "d",
            element 4 is parameter "e".

    Methods:
    --------

        predict: predicts y value from the x value the stored parameters.

        dL_da: computes the partial derivative of the loss function with respect
        to the parameter "a".

        dL_db: computes the partial derivative of the loss function with respect
        to the parameter "b".

        dL_dc: computes the partial derivative of the loss function with respect
        to the parameter "c".

        dL_dd: computes the partial derivative of the loss function with respect
        to the parameter "d".

        dL_de: computes the partial derivative of the loss function with respect
        to the parameter "e".

        compile_diff_funcs: compiles trainable parameters and their respective
        derivative calculations.

        fit: fit the approximator to the data using gradient descent.

    """

    def __init__(
        self, initial_params=None, initializer=None, smart_init=False, seed=None
    ):
        """
        Initialises the TrigModel object.

        Kwargs:
        -------

            initial_params (dict, default = None): parameters to initialize the
            curve approximator, if desired. Note that the dict must take the
            following form:

                dict = {
                    "a": {"value": float, "trainable": bool},
                    "b": {"value": float, "trainable": bool},
                    "c": {"value": float, "trainable": bool},
                    "d": {"value": float, "trainable": bool},
                    "e": {"value": float, "trainable": bool},
                }

                where each initial parameter value is given, along with a bool
                flag to determine whether the parameter is trainable or fixed.

            initializer (numpy.random._generator.Generator, default = None):
            numpy rng built-in method for customised random parameter
            initialization.

            smart_init (bool, default = False): whether or not to use a
            kurvy.trig.ParamEstimator to initialize parameters (note that this
            generally leads to better results).

            seed (int, default = None): value on which to set the random seed for
            reproducibility.

        Yields:
        -------

            self.smart

            self.initial_params

            self.params

            self.training_history

        """

        if initial_params is None:
            initial_params = {
                "a": {"value": None, "trainable": True},
                "b": {"value": None, "trainable": True},
                "c": {"value": None, "trainable": True},
                "d": {"value": None, "trainable": True},
                "e": {"value": None, "trainable": True},
            }

        init_rng = np.random.default_rng(seed)

        if initializer is not None:
            random_init = initializer
        else:
            random_init = init_rng.uniform(-1, 1, size=5)

        for i, (k, v) in enumerate(initial_params.items()):
            if v["value"] is None:
                v["value"] = random_init[i]

        self.smart = False
        if smart_init:
            self.smart = True

        self.initial_params = copy.deepcopy(initial_params)
        self.params = copy.deepcopy(initial_params)
        self.training_history = None

    def predict(self, x):
        """
        Calculates the predicted y value from the x value the stored parameters.
        """

        a = self.params["a"]["value"]
        b = self.params["b"]["value"]
        c = self.params["c"]["value"]
        d = self.params["d"]["value"]
        e = self.params["e"]["value"]

        cos_val = np.cos(2 * np.pi * x / b - c)
        pred = a * cos_val + d + e * x

        return pred

    def dL_da(self, X, Y):
        """
        Calculates the partial derivative of the loss function with respect
        to the parameter "a".
        """

        a = self.params["a"]["value"]
        b = self.params["b"]["value"]
        c = self.params["c"]["value"]
        d = self.params["d"]["value"]
        e = self.params["e"]["value"]
        n = X.shape[0]

        cos_val = np.cos(2 * np.pi * X / b - c)
        dL_da = (1 / n) * np.sum(2 * cos_val * (a * cos_val + d + e * X - Y))
        return dL_da

    def dL_db(self, X, Y):
        """
        Calculates the partial derivative of the loss function with respect
        to the parameter "b".
        """

        a = self.params["a"]["value"]
        b = self.params["b"]["value"]
        c = self.params["c"]["value"]
        d = self.params["d"]["value"]
        e = self.params["e"]["value"]
        n = X.shape[0]

        cos_val = np.cos(2 * np.pi * X / b - c)
        sin_val = np.sin(2 * np.pi * X / b - c)
        dL_db = (1 / n) * np.sum(
            (4 * np.pi * a * X * (a * cos_val + d + e * X - Y) * sin_val)
            / b**2
        )
        return dL_db

    def dL_dc(self, X, Y):
        """
        Calculates the partial derivative of the loss function with respect
        to the parameter "c".
        """

        a = self.params["a"]["value"]
        b = self.params["b"]["value"]
        c = self.params["c"]["value"]
        d = self.params["d"]["value"]
        e = self.params["e"]["value"]
        n = X.shape[0]

        cos_val = np.cos(2 * np.pi * X / b - c)
        sin_val = np.sin(2 * np.pi * X / b - c)
        dL_dc = (1 / n) * np.sum(
            2 * (a * cos_val + d + e * X - Y) * (a * sin_val)
        )
        return dL_dc

    def dL_dd(self, X, Y):
        """
        Calculates the partial derivative of the loss function with respect
        to the parameter "d".
        """

        a = self.params["a"]["value"]
        b = self.params["b"]["value"]
        c = self.params["c"]["value"]
        d = self.params["d"]["value"]
        e = self.params["e"]["value"]
        n = X.shape[0]

        cos_val = np.cos(2 * np.pi * X / b - c)
        dL_dd = (1 / n) * np.sum(2 * (a * cos_val + d + e * X - Y))
        return dL_dd

    def dL_de(self, X, Y):
        """
        Calculates the partial derivative of the loss function with respect
        to the parameter "e".
        """

        a = self.params["a"]["value"]
        b = self.params["b"]["value"]
        c = self.params["c"]["value"]
        d = self.params["d"]["value"]
        e = self.params["e"]["value"]
        n = X.shape[0]

        cos_val = np.cos(2 * np.pi * X / b - c)
        dL_de = (1 / n) * np.sum(2 * X * (a * cos_val + d + e * X - Y))
        return dL_de

    def compile_diff_funcs(self):
        """
        Helper function to compile trainable parameters and their respective
        derivative calculations.
        """

        diff_funcs = [
            ("a", self.dL_da),
            ("b", self.dL_db),
            ("c", self.dL_dc),
            ("d", self.dL_dd),
            ("e", self.dL_de),
        ]

        trainable_params = {
            k: v["value"]
            for k, v in self.params.items()
            if self.params[k]["trainable"]
        }
        diff_funcs = [f for f in diff_funcs if f[0] in trainable_params.keys()]

        return diff_funcs

    def fit(
        self,
        X,
        Y,
        epochs=5,
        learning_rate=0.1,
        momentum=None,
        lambda_2=None,
        window_size=None,
        save_best=False,
    ):
        """
        Fits the initialised curve approximator to data using gradient descent.
        After the method has run, the "params" attribute will be the optimized
        values obtained during training.

        Args:
        -----

            X (1-D array): X data array.

            Y (1-D array): Y data array.


        Kwargs:
        -------

            epochs (int, default = 5): number of times to process entire dataset
            and update parameter values through gradient descent.

            learning_rate (float, default = 0.1): constant multiple for
            calculating parameter update step in each epoch, where:
                update = -learning_rate * deriv
                new param value = old param value + update

            momentum (float, default = None): if given, will apply gradient
            descent with momentum, taking into account prior gradients, where:
                new v = momentum * old v - learning_rate * deriv
                update = new v
                new param value = old param value + update

            lambda_2 (dict, default = None): where keys are param names and
            values are lambda values. If given, will apply L2
            regularization penalty to training, where:
                new v = momentum * old v - learning_rate * deriv
                update = new v - learning_rate * lambda_2 * old param value
                (with momentum)
                update = -learning_rate * deriv - learning_rate * lambda_2
                * old param value
                (without momentum)
                new param value = old param value + update

            window_size (int, default = None): number of samples to include in
            rolling mean for period estimation. Must be given if using smart
            initialization.

            save_best (bool, default = False): whether or not to store the best
            performing parameter values.

        Yields:
        -------

            self.best_epoch (int): epoch with best performance (optimized loss).

            self.best_params (1-D array): parameter values with best
            performance, where:
                element 0 is parameter "a",
                element 1 is parameter "b",
                element 2 is parameter "c",
                element 3 is parameter "d",
                element 4 is parameter "e".

        """

        # smart initialization with kurvy.trig.ParamEstimator
        if self.smart == True:
            if window_size is None:
                raise ValueError(
                    "Must provide value for 'window_size' if using smart inititalization."
                )
            else:
                pe = ParamEstimator()
                pe.fit(X, Y, window_size=window_size, sort_data=True)
                self.params["a"]["value"] = pe.amplitude
                self.params["b"]["value"] = pe.period
                self.params["c"]["value"] = pe.phase_shift
                self.params["d"]["value"] = pe.offset
                self.params["e"]["value"] = pe.trend

        # get initial loss and R2 values
        Y_pred = self.predict(X)
        mse = utils.calculate_loss(Y_pred, Y)
        r2 = utils.calculate_r2(Y, Y_pred)

        # set up training history
        training_history = np.array(
            [
                mse,
                r2,
                self.params["a"]["value"],
                self.params["b"]["value"],
                self.params["c"]["value"],
                self.params["d"]["value"],
                self.params["e"]["value"],
            ]
        )

        if self.training_history is None:
            self.training_history = training_history

        print(f"Initial Loss: {mse}")

        # compile trainable params and derivative calculations
        self.diff_funcs = self.compile_diff_funcs()

        if momentum:
            v = np.zeros(len(self.diff_funcs))

        if lambda_2:
            if not all([self.params[k]["trainable"] for k in lambda_2.keys()]):
                raise ValueError(
                    "Can only use L2 regularization on trainable params."
                )

        # training loop
        for epoch in tqdm(range(1, epochs + 1)):
            res = np.array(training_history)

            for i, f in enumerate(self.diff_funcs):
                param_name = f[0]
                p = self.__dict__["params"][param_name]["value"]

                dL_dp = f[1]
                dp = dL_dp(X, Y)

                if lambda_2:
                    if param_name in lambda_2.keys():
                        l2_reg = lambda_2[param_name]
                        if momentum:
                            v[i] = momentum * v[i] - learning_rate * dp
                            update = v[i] - learning_rate * l2_reg * p
                        else:
                            update = (
                                -learning_rate * dp - learning_rate * l2_reg * p
                            )
                    else:
                        if momentum:
                            v[i] = momentum * v[i] - learning_rate * dp
                            update = v[i]
                else:
                    if momentum:
                        v[i] = momentum * v[i] - learning_rate * dp
                        update = v[i]
                    else:
                        update = -learning_rate * dp

                p = p + update

                self.__dict__["params"][param_name]["value"] = p

                res[i + 2] = p

            Y_pred = self.predict(X)

            mse = utils.calculate_loss(Y_pred, Y)
            res[0] = mse

            r2 = utils.calculate_r2(Y, Y_pred)
            res[1] = r2

            self.training_history = np.vstack((self.training_history, res))

        print(f"Final Loss: {mse}")

        self.best_epoch = self.training_history.argmin(axis=0)[0]

        self.best_params = self.training_history[self.best_epoch][2:]

        if save_best:
            self.params["a"]["value"] = self.best_params[0]
            self.params["b"]["value"] = self.best_params[1]
            self.params["c"]["value"] = self.best_params[2]
            self.params["d"]["value"] = self.best_params[3]
            self.params["e"]["value"] = self.best_params[4]
