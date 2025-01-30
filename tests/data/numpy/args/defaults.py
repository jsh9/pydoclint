
def func1(arg_1: str = 'value 1',
          arg_2: str = 'value 2',
          arg_3: str = 'value 3',
          arg_4: str = 'value 4',
          ) -> int:
    """
    Function to test arg default spec

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


def func2(arg_1: str = 'value 1',
          arg_2: str = 'value 2',
          arg_3: str = 'value 3',
          arg_4: str = 'value 4',
          ) -> int:
    """
    Function to test arg default spec

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

def func3(arg_1: str = 'value 1',
          arg_2: str = 'value 2',
          arg_3: str = 'value 3',
          arg_4: str = 'value 4',
          ) -> int:
    """
    Function to test arg default spec

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
