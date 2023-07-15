from typing import Optional


def func1(text: str) -> None:
    """A return section can be omitted if requireReturnSectionWhenReturningNone
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
