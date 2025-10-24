# Test cases for numpy-style docstring detection with dashes
# Issue: https://github.com/jsh9/pydoclint/issues/244


def add1(a: float, b: float) -> float:
    """
    Add two numbers.

    Args:
    -----
    a: First number.
    b: Second number.

    Returns:
    --------
    The sum of the two numbers.

    Examples:
    ---------
    >>> add(1, 2)
    3
    """
    return a + b


def add2(a: float, b: float) -> float:
    """
    Add two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
    --------
    The sum of the two numbers.

    Examples:
    ---------
    >>> add(1, 2)
    3
    """
    return a + b


def funcWithReturnsSection(arg1: str) -> str:
    """
    Test case from original issue - Returns section with dashes.

    Returns
    -------
    str
        The return value
    """
    return arg1


def funcWithArgsSection(arg1: str) -> str:
    """
    Test case from original issue - Args section with dashes.

    Parameters
    ----------
    arg1 : str
        The input argument

    Returns
    -------
    str
        The return value
    """
    return arg1


def funcWithExamplesSection() -> None:
    """
    Test case from original issue - Examples section with dashes.

    Examples
    --------
    >>> funcWithExamplesSection()
    """
    pass


def funcWithNumpyStyleDashes(arg1: str) -> str:
    """
    This function should be detected as numpy style due to dashes.

    Parameters
    ----------
    arg1 : str
        The input argument

    Returns
    -------
    str
        The return value
    """
    return arg1


def funcWithoutNumpyDashes(arg1: str) -> str:
    """
    This function should not be detected as numpy style.

    Parameters:
        arg1 (str): The input argument

    Returns:
        str: The return value
    """
    return arg1


def funcWithShortDashes(arg1: str) -> str:
    """
    This function has too few dashes so should not be detected.

    Parameters
    --
    arg1 : str
        The input argument
    """
    return arg1
