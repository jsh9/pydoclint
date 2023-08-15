# Related issue: https://github.com/jsh9/pydoclint/issues/59


def func1(a='a'):
    """
    Title

    Parameters
    ----------
    a : str, default a
    """
    pass


def func2(a='a'):
    """
    Title

    Parameters
    ----------
    a : str, default=a
    """
    pass


def func3(a='a'):
    """
    Title

    Parameters
    ----------
    a : str, default: a
    """
    pass
