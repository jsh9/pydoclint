# From issue: https://github.com/jsh9/pydoclint/issues/87
def foo(_: int, __: str, __a: dict, b: float, ___: bool):
    """Bar.

    Args:
    :param __a: a dict
    :type __a: dict
    :param b: a number
    :type b: float
    """
    pass
