# Regression coverage for https://github.com/jsh9/pydoclint/issues/216
def function_1(
        a: str,
        b: int,
        _c: dict,
        __d: list,
        _: float,
        __: bool,
        __special__: str,
) -> None:
    """My function.

    Args:
        a:
        b:
    """


def function_2(a: str, *_: int, **__special__: str) -> None:
    """My function with starred underscore-only and special arguments.

    Args:
        a:
    """


def function_3(a: str, *_private: int, **__: str) -> None:
    """My function with starred private and underscore-only arguments.

    Args:
        a:
    """
