# fmt: off

# Requested in: https://github.com/jsh9/pydoclint/issues/268

def func8(first: int, *args: int, **kwargs: str) -> None:
    """
    Demonstrate documenting varargs without stars in sphinx style.

    :param first: First value
    :type first: int
    :param args: Additional values
    :type args: int
    :param kwargs: Keyword options
    :type kwargs: str
    :return: Nothing
    :rtype: None
    """
    return None


def func9(*args: int) -> None:
    """
    Docstring contains extra stars that should remain mismatched.

    :param **args: Should not match the signature
    :type **args: int
    :return: Nothing
    :rtype: None
    """
    return None
