
def func1(
        arg_1: str = 'value 1',
        arg_2: str = 'value 2',
        arg_3: str = 'value 3',
        arg_4: str = 'value 4',
) -> int:
    """
    Function to test arg default spec

    There should not be any violations in this function.

    Parameters
    ----------
    arg_1 : str, default 'value 1'
        ok

    arg_2 : str, default = 'value 2'
        ok

    arg_3 : str, default: 'value 3'
        ok

    arg_4 : str = 'value 4'
        ok

    Returns
    -------
    int
        Result
    """

    return 1


def func2(
        arg_1: str = 'value 1',
        arg_2: str = 'value 2',
        arg_3: str = 'value 3',
        arg_4: str = 'value 4',
) -> int:
    """
    Function to test arg default spec.

    There should not be any violations in this function.

    The difference between this function and `func1` is: in the docstring of
    this function, there is no space before the colon (":") in the Parameters
    section.

    Parameters
    ----------
    arg_1: str, default 'value 1'
        ok

    arg_2: str, default = 'value 2'
        ok

    arg_3: str, default: 'value 3'
        ok

    arg_4: str = 'value 4'
        ok

    Returns
    -------
    int
        Result
    """

    return 1


def func3(
        arg_1: str = 'value 1',
        arg_2: str = 'value 2',
        arg_3: str = 'value 3',
        arg_4: str = 'value 4',
) -> int:
    """
    Function to test arg default spec.

    DOC105 violation will be raised for `arg_1` and `arg_4`, because they
    don't follow the expected style for annotating argument defaults.

    Parameters
    ----------
    arg_1: str, has default 'value 1'
        not ok

    arg_2: str, optional
        ok

    arg_3: str, optional
        default is 'value 3'
        ok

    arg_4: str, optional: 'value 4'
        ok

    Returns
    -------
    int
        Result
    """

    return 1
