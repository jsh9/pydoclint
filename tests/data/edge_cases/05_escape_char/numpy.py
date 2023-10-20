# From these issues:
#   https://github.com/jsh9/pydoclint/issues/73
#   https://github.com/jsh9/pydoclint/issues/92


def myFunc(
        arg1_: int,
        arg2__: int,
        arg3___: int,
        arg4____: int,
        some_thing_1_: int,
        some_thing_2__: int,
        some_thing_3___: int,
        some_thing_4____: int,
        some_thing_5_____: str,
        *args: Any,
        **kwargs: Any,
) -> None:
    r"""
    Do something.

    Parameters
    ----------
    arg1\_ : int
        Arg
    arg2\_\_ : int
        Arg
    arg3\_\_\_ : int
        Arg
    arg4\_\_\_\_ : int
        Arg
    some_thing_1\_ : int
        Arg
    some_thing_2\_\_ : int
        Arg
    some_thing_3\_\_\_ : int
        Arg
    some_thing_4\_\_\_\_ : int
        Arg
    some_thing_5_____ : str
        Arg
    *args : Any
        Args
    **kwargs : Any
        Keyword args

    Returns
    -------
    None
        Return value
    """
    pass
