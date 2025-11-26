# fmt: off

# Requested in: https://github.com/jsh9/pydoclint/issues/268

def func8(first: int, *args: int, **kwargs: str) -> None:
    """
    Demonstrate documenting varargs without the leading stars.

    Args:
        first (int): First value
        args (int): Additional values
        kwargs (str): Keyword options

    Returns:
        None: Nothing.
    """
    return None


def func9(*args: int) -> None:
    """
    Docstring contains extra stars that should remain mismatched.

    Args:
        **args (int): Should not match the signature

    Returns:
        None: Nothing.
    """
    return None
