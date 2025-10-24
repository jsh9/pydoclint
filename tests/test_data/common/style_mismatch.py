def func1a(arg1: int) -> bool:
    """
    This docstring is written in Google style.

    Args:
        arg1 (int): Arg 1

    Returns:
        bool: The return value.
    """
    return arg1 > 0


def func1b(arg1: int) -> bool:
    """

    Args:
        arg1 (int): Arg 1

    Returns:
        bool: The return value.
    """
    return arg1 > 0


def func2a(arg1: int) -> bool:
    """
    This docstring is written in numpy style.

    Parameters
    ----------
    arg1 : int
        Arg 1

    Returns
    -------
    bool
        The return value.
    """
    return arg1 > 0


def func2b(arg1: int) -> bool:
    """


    Parameters
    ----------
    arg1 : int
        Arg 1

    Returns
    -------
    bool
        The return value.
    """
    return arg1 > 0


def func3a(arg1: int) -> bool:
    """
    This docstring is written in reST (or Sphinx) style.

    :param arg1: Arg 1
    :type arg1: int
    :return: The return value.
    :rtype: bool
    """
    return arg1 > 0


def func3b(arg1: int) -> bool:
    """
    :param arg1: Arg 1
    :type arg1: int
    :return: The return value.
    :rtype: bool
    """
    return arg1 > 0
