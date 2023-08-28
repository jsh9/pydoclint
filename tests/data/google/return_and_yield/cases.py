from typing import Generator, Iterator


def func1(num: int) -> Generator[int, None, str]:
    """
    Do something

    Args:
        num (int): A number

    Returns:
        str: A string

    Yields:
        int: Another number
    """
    for i in range(num):
        yield i

    return 'All numbers yielded!'


def func2(num: int) -> Iterator[int]:
    """
    Do something

    Args:
        num (int): A number

    Returns:
        str: A string

    Yields:
        int: Another number
    """
    for i in range(num):
        yield i

    return 'All numbers yielded!'


def func3(num: int) -> Generator[bool, None, float]:
    """
    Do something

    Args:
        num (int): A number

    Returns:
        str: A string

    Yields:
        int: Another number
    """
    for i in range(num):
        yield i

    return 0.01


def func4(num: int) -> Generator:
    """
    Do something

    Args:
        num (int): A number

    Returns:
        str: A string

    Yields:
        int: Another number
    """
    for i in range(num):
        yield i

    return 0.01


def func5(num: int) -> Iterator:
    """
    Do something

    Args:
        num (int): A number

    Returns:
        str: A string

    Yields:
        int: Another number
    """
    for i in range(num):
        yield i

    return 0.01
