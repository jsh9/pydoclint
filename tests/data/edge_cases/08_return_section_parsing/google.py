from typing import Any


def test_function() -> dict[str, Any] | None:
    """Some function

    This edge case comes from: https://github.com/jsh9/pydoclint/issues/84

    Returns:
        dict[str, Any] | None: Something
    """
    pass
