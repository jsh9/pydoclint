def func1(arg1: int) -> Iterator[None]:
    """
    This function doesn't yield anything.

    Parameters
    ----------
    arg1 : int
        Arg 1
    """
    # It doesn't matter what actually is yielded.  pydoclint only checks
    # the yield type in the signature's return annotation
    yield 1


def func2(arg1: int) -> Generator[None, None, None]:
    """
    This function doesn't yield anything.

    Parameters
    ----------
    arg1 : int
        Arg 1
    """
    # It doesn't matter what actually is yielded.  pydoclint only checks
    # the yield type in the signature's return annotation
    yield 2


def func3(arg1: int) -> Generator[str, None, None]:
    """
    This function doesn't yield anything.

    Parameters
    ----------
    arg1 : int
        Arg 1
    """
    # It doesn't matter what actually is yielded.  pydoclint only checks
    # the yield type in the signature's return annotation
    yield 2


def func4(num: int) -> Generator[None, None, str]:
    """
    Do something

    Parameters
    ----------
    num : int
        A number

    Returns
    -------
    str
        A string
    """
    for i in range(num):
        yield i

    return 'All numbers yielded!'


def func5(num: int) -> Generator[bool, None, str]:
    """
    Do something

    Parameters
    ----------
    num : int
        A number

    Returns
    -------
    str
        A string
    """
    for i in range(num):
        yield i

    return 'All numbers yielded!'
