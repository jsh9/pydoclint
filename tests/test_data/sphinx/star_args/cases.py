# fmt: off
def func1(arg1: int,
          *, arg2: str,
          arg3: bool,
          **kwargs) -> float:
    """
    Do something.

    :param arg1: Arg 1
    :type arg1: int
    :param arg2: Arg 2
    :type arg2: str
    :param arg3: Arg 3
    :type arg3: bool
    :param **kwargs: Keyword arguments
    :return: Result
    :rtype: float
    """
    return 2.0


def func2(
        arg1: int, *, arg2: str,
        arg3: bool, **kwargs) -> float:
    """
    Do something.

    :param arg1: Arg 1
    :type arg1: int
    :param arg2: Arg 2
    :type arg2: str
    :param arg3: Arg 3
    :type arg3: bool
    :param kwargs: Keyword arguments
    :return: Result
    :rtype: float
    """
    return 2.0


def func3(
        arg1: int, arg2: str,
        arg3: bool,
        *args, **kwargs,
) -> float:
    """
    Do something.

    :param arg1: Arg 1
    :type arg1: int
    :param arg2: Arg 2
    :type arg2: str
    :param arg3: Arg 3
    :type arg3: bool
    :param *args: Args
    :param **kwargs: Keyword arguments
    :return: Result
    :rtype: float
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

    :param arg1: Arg 1
    :type arg1: int
    :param arg2: Arg 2
    :type arg2: str
    :param arg3: Arg 3
    :type arg3: bool
    :param args: Args
    :param **kwargs: Keyword arguments
    :return: Result
    :rtype: float

    """
    return 2.0


def func5(arg1: int, *, arg2: str, arg3: bool) -> float:
    """
    Do something.

    :param arg1: Arg 1
    :type arg1: int
    :param arg2: Arg 2
    :type arg2: str
    :param arg3: Arg 3
    :type arg3: bool
    :return: Result
    :rtype: float
    """
    return 2.0


def func6(arg1: int, arg2: str, arg3: bool, *args, **kwargs) -> float:
    """
    Do something.

    :param arg1: Arg 1
    :type arg1: int
    :param arg2: Arg 2
    :type arg2: str
    :param arg3: Arg 3
    :type arg3: bool
    :return: Result
    :rtype: float
    """
    return 2.0


def func7(arg1: float, arg2: str, arg3: bool, *args, **kwargs) -> float:
    """
    Do something.

    :param arg2: Arg 2
    :type arg2: dict
    :param arg1: Arg 1
    :type arg1: int
    :param arg3: Arg 3
    :type arg3: bool
    :return: Result
    :rtype: float
    """
    return 2.0
