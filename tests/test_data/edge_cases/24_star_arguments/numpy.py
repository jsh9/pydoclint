# From: https://github.com/jsh9/pydoclint/issues/121

def function_1(arg1: int, *args: Any, **kwargs: Any) -> None:
    """
    Do something

    Parameters
    ----------
    arg1 : int
        Arg 1
    """
    pass


def function_2(arg1: int, *args: Any, **kwargs: Any) -> None:
    """
    Do something

    Parameters
    ----------
    arg1 : int
        Arg 1
    *args : Any
        Args
    **kwargs : Any
        Kwargs
    """
    pass


def function_3(arg1: int, *args: Any, **kwargs: Any) -> None:
    """
    Do something

    Parameters
    ----------
    arg1 : int
        Arg 1
    **kwargs : Any
        Kwargs
    """
    pass
