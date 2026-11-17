def hashInDefault(color: str = '#1f77b4') -> None:
    """
    The documented default is wrong. It starts with `#`, which is part of the
    string, not the start of a comment, so this must get DOC105.

    Parameters
    ----------
    color : str, default='#ff0000'
        The color.
    """


def defaultWrittenDifferently(count: int, ratio=0.00001) -> None:
    """
    `ratio` has no type, only a default. The documented default is written as
    in the code (`0.00001`), while pydoclint reads the code's default as
    `1e-05`. It's the same value, so this must not get DOC105. (It gets
    DOC107/DOC110 because `ratio` has no type hint.)

    Parameters
    ----------
    count : int
        The count.
    ratio : , default=0.00001
        The ratio.
    """
