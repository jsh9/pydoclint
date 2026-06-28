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


def func6(num: int) -> Generator[int]:
    """
    Test a one-argument Generator annotation.

    Expected: Generator[int] yields int and defaults the generator return
    value to None, so no return field is required.

    :param num: A number
    :type num: int
    :yield: Another number
    :ytype: int
    """
    yield num

    return None


def func7(num: int) -> Generator[int, str]:
    """
    Test a two-argument Generator annotation.

    Expected: Generator[int, str] yields int, treats str as SendType, and
    defaults the generator return value to None.

    :param num: A number
    :type num: int
    :yield: Another number
    :ytype: int
    """
    yield num

    return None


def func8(num: int) -> Generator[int, str, bool]:
    """
    Test a three-argument Generator annotation.

    Expected: Generator[int, str, bool] yields int and uses bool as the
    generator return type, so both documented fields should pass.

    :param num: A number
    :type num: int
    :return: A flag
    :rtype: bool
    :yield: Another number
    :ytype: int
    """
    yield num

    return True


def func9(num: int) -> Generator[int, str]:
    """
    Test that the second Generator argument is not the return type.

    Expected: this fixture reports DOC203 because str is SendType, while the
    generator return type defaults to None under PEP 696.

    :param num: A number
    :type num: int
    :return: A string
    :rtype: str
    :yield: Another number
    :ytype: int
    """
    yield num

    return None
