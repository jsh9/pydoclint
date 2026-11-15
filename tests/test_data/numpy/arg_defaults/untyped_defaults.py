# Arguments with default values but without type annotations
# (https://github.com/jsh9/pydoclint/issues/313). This fixture is checked with
# different combinations of the type-hint options and --check-arg-defaults.


def undocumentedDefault(value=3) -> None:
    """
    The docstring gives neither a type nor a default.

    Parameters
    ----------
    value
        A value.
    """


def defaultOnly(value=3) -> None:
    """
    The docstring gives the default but no type.

    Parameters
    ----------
    value : , default=3
        A value.
    """


def wrongDefaultOnly(value=3) -> None:
    """
    The docstring gives a wrong default and no type.

    Parameters
    ----------
    value : , default=4
        A value.
    """


def typedDocstring(values, alpha=0.05) -> None:
    """
    Only the docstring has types, which is common in code without annotations.

    Parameters
    ----------
    values : numpy.ndarray
        The values.
    alpha : float, default=0.05
        The alpha value.
    """


def typedDocstringWrongDefault(values, alpha=0.05) -> None:
    """
    The docstring has types, but a wrong default.

    Parameters
    ----------
    values : numpy.ndarray
        The values.
    alpha : float, default=0.5
        The alpha value.
    """


def typedDocstringMissingDefault(values, alpha=0.05) -> None:
    """
    The docstring has types, but no default.

    Parameters
    ----------
    values : numpy.ndarray
        The values.
    alpha : float
        The alpha value.
    """


def freeFormTypes(values=None, count=3) -> None:
    """
    The docstring types aren't valid Python, but the defaults are right.

    Parameters
    ----------
    values : array-like of shape (n,), default=None
        The values.
    count : int, default=3
        The count.
    """


def defaultForRequiredArg(values, count=3) -> None:
    """
    The docstring gives a default to an argument that doesn't have one.

    Parameters
    ----------
    values : list of int, default=None
        The values.
    count : int, default=3
        The count.
    """


def typedSignature(x: int = 3, y: str = 'a') -> None:
    """
    The signature has types, but the docstring only gives the defaults.

    Parameters
    ----------
    x : , default=3
        The x value.
    y : , default="b"
        The y value, with a wrong default.
    """


def partiallyTyped(count: int, value=3) -> None:
    """
    Only some arguments have types, in the signature and in the docstring.

    Parameters
    ----------
    count : int
        The count.
    value : , default=3
        A value.
    """
