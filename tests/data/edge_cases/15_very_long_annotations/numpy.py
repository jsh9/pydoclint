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
    """
    The docstring parser for the numpy style does not support line breaking
    in type hints. Therefore, in order to pass pydoclint's checks, we can only
    put long type hints in one line.

    Parameters
    ----------
    arg1 : tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]
        A parameter

    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]
        The return value
    """
    return (
        np.array([]), np.array([]), np.array([]), np.array([]), np.array([]),
        np.array([]), np.array([]), np.array([]), np.array([]),
    )

# fmt: on
