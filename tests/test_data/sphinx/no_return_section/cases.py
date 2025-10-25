from typing import NoReturn, Optional


def func1(text: str) -> None:
    """A return section can be omitted if requireReturnSectionWhenReturningNothing
    is set to False.

    :param text: Text for the function
    :type text: str
    """
    print(123)


def func2(text: str) -> int:
    """A return section is always required because it returns something

    :param text: Text for the function
    :type text: str
    """
    return 1


def func3(text: str) -> Optional[int]:
    """A return section is always required because it returns something

    :param text: Text for the function
    :type text: str
    """
    return 1


def func4(text: str):
    """A return section is always required because it has explicit "return"
    in the function body (even if it is "return None")

    :param text: Text for the function
    :type text: str
    """
    return None


def func5(text: str):
    """A return section is always required because it has explicit "return"
    in the function body (even if it is just "return")

    :param text: Text for the function
    :type text: str
    """
    return


def func6(text: str):
    """A return section is never necessary because it doesn't return
    anything and there is no return type annotation.

    :param text: Text for the function
    :type text: str
    """
    print(123)


def func7(text: str) -> NoReturn:
    """A return section is never necessary because it doesn't return
    anything or even return ever, as there is a NoReturn annotation.

    :param text: Text for the function
    :type text: str
    """
    exit(1)


def func8(num: int) -> Generator[None, None, None]:
    """
    Do something

    :param num: A number
    :type num: int
    """
    for i in range(num):
        yield i

    return 'All numbers yielded!'


def func9(num: int) -> Generator[None, None, NoReturn]:
    """
    Do something

    :param num: A number
    :type num: int
    """
    for i in range(num):
        yield i

    return 'All numbers yielded!'


def func10(num: int) -> Generator[bool, None, str]:
    """
    Do something

    :param num: A number
    :type num: int
    """
    for i in range(num):
        yield i

    return 'All numbers yielded!'
