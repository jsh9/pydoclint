# This edge case was reported in https://github.com/jsh9/pydoclint/issues/164

# fmt: off

import numpy as np


def func(
        arg1: tuple[
            np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray,
            np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray,
            np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray,
        ],
) -> tuple[
        np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray,
        np.ndarray, np.ndarray, np.ndarray]:
    """Something

    :param arg1: A parameter
    :type arg1: tuple[
        np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray,
        np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray,
        np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray,
    ]

    :returns: Numpy arrays
    :rtype: tuple[
        np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray,
        np.ndarray, np.ndarray, np.ndarray]
    """
    return (
        np.array([]), np.array([]), np.array([]), np.array([]), np.array([]),
        np.array([]), np.array([]), np.array([]), np.array([]),
    )

# fmt: on
