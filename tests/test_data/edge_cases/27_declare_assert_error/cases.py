# From: https://github.com/jsh9/pydoclint/issues/213#issuecomment-2766710687

def func() -> None:
    """
    Some function.

    Raises:
        TypeError: If the function is called with an invalid type.
    """
    if 1 == 2:
        raise TypeError("Invalid type")
    else:
        assert True
