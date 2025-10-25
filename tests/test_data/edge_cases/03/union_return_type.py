# From this issue: https://github.com/jsh9/pydoclint/issues/66


def myFunc(arg1: int | str) -> str | bool | None:
    """
    The docstring parser for Google-style docstring should be able to
    parse the docstring without issues.

    And then, pydoclint should be able to detect the discrepancy
    between the return type hints in the signature and in the
    docstring.

    Args:
        arg1 (int | str): Arg 1

    Returns:
        str | bool | float: The return value
    """
    pass
