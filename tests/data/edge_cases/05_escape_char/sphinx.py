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

    :param arg1\_: Arg
    :type arg1\_: int
    :param arg2\_\_: Arg
    :type arg2\_\_: int
    :param arg3\_\_\_: Arg
    :type arg3\_\_\_: int
    :param arg4\_\_\_\_: Arg
    :type arg4\_\_\_\_: int
    :param some_thing_1\_: Arg
    :type some_thing_1\_: int
    :param some_thing_2\_\_: Arg
    :type some_thing_2\_\_: int
    :param some_thing_3\_\_\_: Arg
    :type some_thing_3\_\_\_: int
    :param some_thing_4\_\_\_\_: Arg
    :type some_thing_4\_\_\_\_: int
    :param some_thing_5_____: Arg
    :type some_thing_5_____: str
    :param \\*args: Args
    :type \\*args: Any
    :param \\**kwargs: Args
    :type \\**kwargs: Any
    :return: Return value
    :rtype: None
    """
    pass
