# From this issue: https://github.com/jsh9/pydoclint/issues/56


def my_function(
        my_variable_1: int,
        my_variable_2: Literal[
            'option_1',
            'option_2',
            'option_3',
            'option_4',
            'option_5',
            'option_6',
        ],
) -> None:
    """
    Some random function.

    :param my_variable_1: Some integer that does something.
    :type my_variable_1: int
    :param my_variable_2: Some literal that does something.
    :type my_variable_2: Literal[
        "option_1",
        "option_2",
        "option_3",
        "option_4",
        "option_5",
        "option_6",
    ]
    """
    pass
