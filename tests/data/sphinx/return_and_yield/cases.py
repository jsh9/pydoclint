from typing import Generator, Iterator


def func1(num: int) -> Generator[int, None, str]:
    """
    Do something

    :param num: A number
    :type num: int
    :return: A string
    :rtype: str
    :yield: Another number
    :ytype: int
    """
    for i in range(num):
        yield i

    return 'All numbers yielded!'


def func2(num: int) -> Iterator[int]:
    """
    Do something

    :param num: A number
    :type num: int
    :return: A string
    :rtype: str
    :yield: Another number
    :ytype: int
    """
    for i in range(num):
        yield i

    return 'All numbers yielded!'


def func3(num: int) -> Generator[bool, None, float]:
    """
    Do something

    :param num: A number
    :type num: int
    :return: A string
    :rtype: str
    :yield: Another number
    :ytype: int
    """
    for i in range(num):
        yield i

    return 0.01


def func4(num: int) -> Generator:
    """
    Do something

    :param num: A number
    :type num: int
    :return: A string
    :rtype: str
    :yield: Another number
    :ytype: int
    """
    for i in range(num):
        yield i

    return 0.01


def func5(num: int) -> Iterator:
    """
    Do something

    :param num: A number
    :type num: int
    :return: A string
    :rtype: str
    :yield: Another number
    :ytype: int
    """
    for i in range(num):
        yield i

    return 0.01
