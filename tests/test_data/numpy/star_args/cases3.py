# fmt: off

# Requested in: https://github.com/jsh9/pydoclint/issues/268

def func8(first: int, *args: int, **kwargs: str) -> None:
    """
    Demonstrate documenting varargs without stars in numpy style.

    Parameters
    ----------
    first : int
        First value
    args : int
        Additional values
    kwargs : str
        Keyword options

    Returns
    -------
    None
    """
    return None


def func9(*args: int) -> None:
    """
    Docstring contains extra stars that should remain mismatched.

    Parameters
    ----------
    **args : int
        Should not match the signature

    Returns
    -------
    None
    """
    return None
