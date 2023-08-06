import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import copy


def split_n(n, r):
    """
    Splits integer into round chunks given by ratio splits.

    Args:
    -----

        n (int): number to split.

        r (tuple): ratios by which to split "n". Note that the elements of "r"
        are expected to sum to 100, and that "n" will be split into len(r)
        chunks.

    Returns:
    --------

        splits (list): list containing integer splits for "n" by "r".
    """

    if not isinstance(n, int):
        raise TypeError(f"'n' must be integer; {type(n)} given.")
    if not all([isinstance(i, int) for i in r]):
        raise ValueError("Elements of 'r' must all be integer.")
    if sum(r) != 100:
        raise ValueError(f"Elements of 'r' must sum to 100; sum = {sum(r)}.")
    splits = []
    for i in r[:-1]:
        x = n * (i / 100)
        if x % 1 != 0:
            x = int(round(x, 0))
        else:
            x = int(x)
        splits.append(x)
    rem = n - sum(splits)
    if rem != 0:
        splits.append(rem)
    checksum = sum(splits)
    return splits if checksum == n else None


def lin_reg(X, Y):
    """
    Performs linear regression on X and Y data.

    Args:
    -----

        X (1-D array): X data array.

        Y (1-D array): Y data array.

    Returns:
    --------

        w (float): weight (gradient) of regression line.

        b (float): bias (offset) of regression line.
    """

    n = Y.shape[0]
    sum_X = np.sum(X)
    sum_Y = np.sum(Y)
    sum_XY = np.sum(X * Y)
    sum_Xsq = np.sum(X**2)
    numerator_w = (n * sum_XY) - (sum_X * sum_Y)
    numerator_b = (sum_Y * sum_Xsq) - (sum_X * sum_XY)
    denominator = (n * sum_Xsq) - (sum_X**2)
    w = numerator_w / denominator
    b = numerator_b / denominator
    return w, b


# def make_data(
#     X_range, n_samples, params=None, plot=False, fuzz=None, seed=None
# ):
#     rng = np.random.default_rng(seed)

#     if not isinstance(X_range, tuple):
#         raise ValueError(
#             f"Expected 2-tuple for 'X_range'; got {type(X_range)}."
#         )
#     if not all([isinstance(i, int) for i in X_range]):
#         raise ValueError(f"'X_range' must be tuple of integers: (min, max).")
#     if not isinstance(n_samples, int):
#         raise ValueError(
#             f"Expected integer for 'n_samples'; got {type(n_samples)}."
#         )
#     if fuzz:
#         if not isinstance(fuzz, int) or (not 0 <= fuzz <= 3):
#             raise ValueError(f"'fuzz' must be integer in [0,3].")
#     if params:
#         if not isinstance(params, tuple):
#             raise ValueError(
#                 f"Expected 5-tuple for 'params'; got {type(params)}."
#             )
#         if len(params) != 5:
#             raise ValueError(
#                 f"Expected 5-tuple for 'params'; got {len(params)}-tuple."
#             )

#         a, b, c, d, e = params

#     else:
#         mu = np.percentile(X_range, 25)
#         std = mu * 0.5

#         a = np.round(rng.normal(mu, std), 3)
#         b = np.round(rng.integers(np.floor(X_range[1])) + rng.random(), 3)
#         c = np.round(rng.integers(np.floor(X_range[1])) + rng.random(), 3)
#         d = np.round(rng.integers(np.floor(X_range[1])) + rng.random(), 3)
#         e = np.round(rng.uniform(-2, 2), 3)

#     X = np.linspace(X_range[0], X_range[1], n_samples)

#     cos_val = np.cos(2 * np.pi * X / b - c)
#     Y = a * cos_val + d + e * X

#     if fuzz == 1:
#         Y_fuzzy = add_fuzz(Y, 1, 0, X_range[1] * 0.01, seed=seed)

#     elif fuzz == 2:
#         Y_fuzzy = add_fuzz(Y, 1, 0, X_range[1] * 0.01, seed=seed)
#         Y_fuzzy = add_fuzz(Y_fuzzy, 0.3, 0, X_range[1] * 0.075, seed=seed)

#     elif fuzz == 3:
#         Y_fuzzy = add_fuzz(Y, 1, 0, X_range[1] * 0.01, seed=seed)
#         Y_fuzzy = add_fuzz(Y_fuzzy, 0.3, 0, X_range[1] * 0.075, seed=seed)
#         Y_fuzzy = add_fuzz(Y_fuzzy, 0.05, 0, X_range[1] * 0.3, seed=seed)

#     else:
#         Y_fuzzy = Y

#     if plot:
#         plt.figure(figsize=(12, 4))
#         plt.scatter(X, Y_fuzzy, color="teal", s=20, alpha=0.5)
#         plt.plot(
#             X,
#             Y,
#             color="mediumturquoise",
#             alpha=0.7,
#             linewidth=7,
#             solid_capstyle="round",
#         )
#         plt.show()

#     return a, b, c, d, e, X, Y_fuzzy


def add_fuzz(Y, fraction, error_mu, error_std, seed=None):
    """
    Adds fuzz (random error) to sample data.

    Args:
    -----

        Y (1-D array): Y data array.

        fraction (float): fraction of data for which to add error.

        error_mu (float): mean value for error.

        error_std (float): standard deviation for error.

    Kwargs:
    -------

        seed (int, default = None): value on which to set the random seed for
        reproducibility.

    Returns:
    --------

        Y_fuzzy (1-D array): Y_data with added fuzz.
    """

    rng = np.random.default_rng(seed)

    error_n = int(Y.shape[0] * fraction)
    error_idxs = rng.choice(Y.shape[0], error_n, replace=False)

    errors = rng.normal(error_mu, error_std, error_n)

    Y_fuzzy = np.array(Y)
    Y_fuzzy[error_idxs] += errors

    return Y_fuzzy


def min_max_scale(i, a, b, data_min, data_max):
    """
    Rescale data from range [data_min : data_max] to range [a : b].
    """

    scaled_i = (b - a) * (i - data_min) / (data_max - data_min) + a
    return scaled_i


def calculate_loss(Y, Y_pred):
    """
    Calculate MSE loss using Y data and predicted Y data.
    """

    n = Y.shape[0]

    sq_errors = [(i[0] - i[1]) ** 2 for i in np.dstack((Y, Y_pred))[0]]
    mse = np.sum(sq_errors) / n

    return mse


def calculate_r2(Y, Y_pred):
    """
    Calculate R-sqaured using Y data and predicted Y data.
    """

    n = Y.shape[0]
    Y_mu = np.mean(Y)

    sq_errors = [(i[0] - i[1]) ** 2 for i in np.dstack((Y, Y_pred))[0]]
    sse = np.sum(sq_errors)

    sq_totals = [(i - Y_mu) ** 2 for i in Y]
    sst = sum(sq_totals)

    r2 = 1 - sse / sst

    return r2


def scale_up_params(params, X_raw_min, X_raw_max, Y_raw_min, Y_raw_max):
    """
    Scales predicted parameters back to raw range. Note that the parameters are
    expected in list form.
    """

    a = params[0]
    b = params[1]
    c = params[2]
    d = params[3]
    e = params[4]

    alpha_x = X_raw_max - X_raw_min
    beta_x = X_raw_min
    alpha_y = Y_raw_max - Y_raw_min
    beta_y = Y_raw_min

    a_scaled = a * alpha_y
    b_scaled = b * alpha_x + beta_x
    c_scaled = c
    d_scaled = alpha_y * (d - e * beta_x / alpha_x) + beta_y
    e_scaled = alpha_y * e / alpha_x

    return a_scaled, b_scaled, c_scaled, d_scaled, e_scaled
