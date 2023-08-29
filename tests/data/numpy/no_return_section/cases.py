from typing import NoReturn, Optional


def func1(text: str) -> None:
    """A return section can be omitted if requireReturnSectionWhenReturningNothing
    is set to False.

    Parameters
    ----------
    text : str
        Text for the function
    """
    print(123)


def func2(text: str) -> int:
    """A return section is always required because it returns something

    Parameters
    ----------
    text : str
        Text for the function
    """
    return 1


def func3(text: str) -> Optional[int]:
    """A return section is always required because it returns something

    Parameters
    ----------
    text : str
        Text for the function
    """
    return 1


def func4(text: str):
    """A return section is always required because it has explicit "return"
    in the function body (even if it is "return None")

    Parameters
    ----------
    text : str
        Text for the function
    """
    return None


def func5(text: str):
    """A return section is always required because it has explicit "return"
    in the function body (even if it is just "return")

    Parameters
    ----------
    text : str
        Text for the function
    """
    return


def func6(text: str):
    """A return section is never necessary because it doesn't return
    anything and there is no return type annotation.

    Parameters
    ----------
    text : str
        Text for the function
    """
    print(123)


def func7(text: str) -> NoReturn:
    """A return section is never necessary because it doesn't return
    anything or even return ever, as there is a NoReturn annotation.

    Parameters
    ----------
    text : str
        Text for the function
    """
    exit(1)


def func8(num: int) -> Generator[None, None, None]:
    """
    Do something

    Parameters
    ----------
    num : int
        A number
    """
    for i in range(num):
        yield i

    return 'All numbers yielded!'


def func9(num: int) -> Generator[None, None, NoReturn]:
    """
    Do something

    Parameters
    ----------
    num : int
        A number
    """
    for i in range(num):
        yield i

    return 'All numbers yielded!'


def func10(num: int) -> Generator[bool, None, str]:
    """
    Do something

    Parameters
    ----------
    num : int
        A number
    """
    for i in range(num):
        yield i

    return 'All numbers yielded!'
