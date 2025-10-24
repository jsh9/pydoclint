# From https://github.com/jsh9/pydoclint/issues/216

def function_1(a: str, b: int, _c: dict, __d: list, _: float, __: bool):
    """
    My function.

    Args:
        a:
        b:
    """
    pass
