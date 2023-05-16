# fmt: off
def func1(arg1: int,
          *, arg2: str,
          arg3: bool,
          **kwargs) -> float:
    """
    Do something.

    Parameters
    ----------
    arg1 : int
        Arg 1
    arg2 : str
        Arg 2
    arg3 : bool
        Arg 3
    **kwargs :
        Keyword arguments

    Returns
    -------
    float
        Result
    """
    return 2.0


def func2(
        arg1: int, *, arg2: str,
        arg3: bool, **kwargs) -> float:
    """
    Do something.

    Parameters
    ----------
    arg1 : int
        Arg 1
    arg2 : str
        Arg 2
    arg3 : bool
        Arg 3
    kwargs :
        Keyword arguments

    Returns
    -------
    float
        Result
    """
    return 2.0


def func3(
        arg1: int, arg2: str,
        arg3: bool,
        *args, **kwargs,
) -> float:
    """
    Do something.

    Parameters
    ----------
    arg1 : int
        Arg 1
    arg2 : str
        Arg 2
    arg3 : bool
        Arg 3
    *args :
        Args
    **kwargs :
        Keyword arguments

    Returns
    -------
    float
        Result
    """
    return 2.0


def func4(arg1: int,
          arg2: str,
          arg3: bool,
          *args,
          **kwargs
          ) -> float:
    """
    Do something.

    Parameters
    ----------
    arg1 : int
        Arg 1
    arg2 : str
        Arg 2
    arg3 : bool
        Arg 3
    args :
        Args
    **kwargs :
        Keyword arguments

    Returns
    -------
    float
        Result
    """
    return 2.0


def func5(arg1: int, *, arg2: str, arg3: bool) -> float:
    """
    Do something.

    Parameters
    ----------
    arg1 : int
        Arg 1
    arg2 : str
        Arg 2
    arg3 : bool
        Arg 3

    Returns
    -------
    float
        Result
    """
    return 2.0


def func6(arg1: int, arg2: str, arg3: bool, *args, **kwargs) -> float:
    """
    Do something.

    Parameters
    ----------
    arg1 : int
        Arg 1
    arg2 : str
        Arg 2
    arg3 : bool
        Arg 3

    Returns
    -------
    float
        Result
    """
    return 2.0


def func7(arg1: float, arg2: str, arg3: bool, *args, **kwargs) -> float:
    """
    Do something.

    Parameters
    ----------
    arg2 : dict
        Arg 2
    arg1 : int
        Arg 1
    arg3 : bool
        Arg 3

    Returns
    -------
    float
        Result
    """
    return 2.0
