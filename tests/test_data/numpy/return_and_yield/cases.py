from typing import AsyncGenerator, Generator, Iterator


def func1(num: int) -> Generator[int, None, str]:
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

    Yields
    ------
    int
        Another number
    """
    for i in range(num):
        yield i

    return 'All numbers yielded!'


def func2(num: int) -> Iterator[int]:
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

    Yields
    ------
    int
        Another number
    """
    for i in range(num):
        yield i

    return 'All numbers yielded!'


def func3(num: int) -> Generator[bool, None, float]:
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

    Yields
    ------
    int
        Another number
    """
    for i in range(num):
        yield i

    return 0.01


def func4(num: int) -> Generator:
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

    Yields
    ------
    int
        Another number
    """
    for i in range(num):
        yield i

    return 0.01


def func5(num: int) -> Iterator:
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

    Yields
    ------
    int
        Another number
    """
    for i in range(num):
        yield i

    return 0.01


def func6(num: int) -> Generator[int]:
    """
    Test a one-argument Generator annotation.

    Expected: Generator[int] yields int and defaults the generator return
    value to None, so no Returns section is required.

    Parameters
    ----------
    num : int
        A number

    Yields
    ------
    int
        Another number
    """
    yield num

    return None


def func7(num: int) -> Generator[int, str]:
    """
    Test a two-argument Generator annotation.

    Expected: Generator[int, str] yields int, treats str as SendType, and
    defaults the generator return value to None.

    Parameters
    ----------
    num : int
        A number

    Yields
    ------
    int
        Another number
    """
    yield num

    return None


def func8(num: int) -> Generator[int, str, bool]:
    """
    Test a three-argument Generator annotation.

    Expected: Generator[int, str, bool] yields int and uses bool as the
    generator return type, so both documented sections should pass.

    Parameters
    ----------
    num : int
        A number

    Returns
    -------
    bool
        A flag

    Yields
    ------
    int
        Another number
    """
    yield num

    return True


def func9(num: int) -> Generator[int, str]:
    """
    Test that the second Generator argument is not the return type.

    Expected: this fixture reports DOC203 because str is SendType, while the
    generator return type defaults to None under PEP 696.

    Parameters
    ----------
    num : int
        A number

    Returns
    -------
    str
        A string

    Yields
    ------
    int
        Another number
    """
    yield num

    return None


def func10(num: int) -> Iterator[int]:
    """
    This fixture covers the Iterator[int] + value-returning return case. Even
    though Iterator[int] has one subscript argument, pydoclint must not run it
    through Generator return-type defaulting or treat the generator return type
    as None. Because the function returns 'done', the missing Returns section
    should still trigger DOC201.

    Parameters
    ----------
    num : int
        A number

    Yields
    ------
    int
        Another number
    """
    yield num

    return 'done'


def func11(num: int) -> Generator[int, str, bool, bytes]:
    """
    This fixture covers malformed Generator annotations with too many
    subscript arguments. Pydoclint should keep the full annotation instead of
    extracting int as the yield type and bool as the return type. Therefore,
    the documented Returns bool should trigger DOC203, and the documented
    Yields int should trigger DOC404.

    Parameters
    ----------
    num : int
        A number

    Returns
    -------
    bool
        A flag

    Yields
    ------
    int
        Another number
    """
    yield num

    return True


def func12(num: int) -> AsyncGenerator[int, str]:
    """
    Test that the second AsyncGenerator argument is not a return type.

    Expected: this fixture reports DOC203 because AsyncGenerator has no return
    type argument, so the return type is None.

    Parameters
    ----------
    num : int
        A number

    Returns
    -------
    str
        A string

    Yields
    ------
    int
        Another number
    """
    yield num

    return None
