from typing import Any, AsyncIterator, Dict, Generator, Iterator


def iteratorDict() -> Iterator[Dict[str, Any]]:
    """This test case verifies that Iterator keeps a nested Dict yield type.

    :yield: The outputs.
    :ytype: Dict[str, Any]
    """
    yield {}
    return


class Worker:
    async def asyncIteratorDict(
            self,
            batch: Dict[str, Any],
    ) -> AsyncIterator[Dict[str, Any]]:
        """This test case verifies that AsyncIterator methods keep Dict yields.

        :param batch: The input batch.
        :type batch: Dict[str, Any]
        :yield: The outputs.
        :ytype: Dict[str, Any]
        """
        if not batch:
            yield {}
            return
        yield {'a': 1}


def generatorDict() -> Generator[Dict[str, Any], None, str]:
    """This test case verifies that Generator keeps yield and return types.

    :yield: The outputs.
    :ytype: Dict[str, Any]
    :return: The completion message.
    :rtype: str
    """
    yield {}
    return 'done'


def iteratorBuiltinDict() -> Iterator[dict[str, Any]]:
    """This test case verifies that Iterator keeps a built-in dict yield type.

    :yield: The outputs.
    :ytype: dict[str, Any]
    """
    yield {}
    return
