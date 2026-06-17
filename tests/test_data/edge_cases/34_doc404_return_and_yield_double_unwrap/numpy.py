from typing import Any, AsyncIterator, Dict, Generator, Iterator


def iteratorDict() -> Iterator[Dict[str, Any]]:
    """
    This test case verifies that Iterator keeps a nested Dict yield type.

    Yields
    ------
    Dict[str, Any]
        The outputs.
    """
    yield {}
    return


class Worker:
    async def asyncIteratorDict(
            self,
            batch: Dict[str, Any],
    ) -> AsyncIterator[Dict[str, Any]]:
        """
        This test case verifies that AsyncIterator methods keep Dict yields.

        Parameters
        ----------
        batch : Dict[str, Any]
            The input batch.

        Yields
        ------
        Dict[str, Any]
            The outputs.
        """
        if not batch:
            yield {}
            return
        yield {'a': 1}


def generatorDict() -> Generator[Dict[str, Any], None, str]:
    """
    This test case verifies that Generator keeps yield and return types.

    Yields
    ------
    Dict[str, Any]
        The outputs.

    Returns
    -------
    str
        The completion message.
    """
    yield {}
    return 'done'


def iteratorBuiltinDict() -> Iterator[dict[str, Any]]:
    """
    This test case verifies that Iterator keeps a built-in dict yield type.

    Yields
    ------
    dict[str, Any]
        The outputs.
    """
    yield {}
    return
