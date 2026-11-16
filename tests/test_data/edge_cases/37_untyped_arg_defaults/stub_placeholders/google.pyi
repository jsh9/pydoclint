def f(x=..., y=3) -> None:
    """
    `x` has the `...` placeholder default, so any documented default is fine,
    even after a type that isn't valid Python.

    Args:
        x (list of int, default=None): The x value.
        y (int, default=3): The y value.
    """
