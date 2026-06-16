from typing import Any, Dict, Iterator


def f() -> Iterator[Dict[str, Any]]:
    """Do work.

    Yields:
        Dict[str, Any]: The outputs.
    """
    yield {}
    return
