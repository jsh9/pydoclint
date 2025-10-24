# From: https://github.com/jsh9/pydoclint/issues/126

from contextlib import contextmanager


@contextmanager
def my_func_1(db: Optional[int]) -> Iterator[int]:
    """Test a function.

    Args:
        db: the database

    Yields:
        Some stuff.
    """
    if db is not None:
        yield db
        return

    db = ...
    yield db


def my_func_2(arg1: int) -> None:
    """
    Test a function.

    Args:
        arg1: some argument

    Returns:
        The return value
    """
    pass
