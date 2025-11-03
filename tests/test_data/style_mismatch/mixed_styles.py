def mixedStyleFunc(arg1: int, arg2: str) -> str:
    """
    Docstring combining multiple styles to simulate ambiguity.

    Args:
        arg1 (int): First argument documented in Google style.

    :param arg2: Second argument documented in Sphinx style.
    :type arg2: str

    Returns:
        str: Google-style return section.

    :return: Sphinx-style return section for the same value.
    :rtype: str
    """
    return f'{arg1}-{arg2}'
