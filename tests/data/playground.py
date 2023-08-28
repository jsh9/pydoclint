# This file is intentionally left empty.
#
# If you'd like to quickly try out some edge cases, put them in this file,
# and run `testPlayground()` in `test_main.py`. This allows you to quickly
# diagnose and debug some issues.

from typing import Generator


def func82() -> Tuple[int, bool]:
    """
    If no summary here, the parser will mis-parse the return section

    Returns
    -------
    int
        Integer to return
    bool
        Boolean to return
    """
    return (1, 1.1)
