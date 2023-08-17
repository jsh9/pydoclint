from typing import (
    Any,
    AsyncGenerator,
    AsyncIterable,
    AsyncIterator,
    Generator,
    Iterable,
    Iterator,
    List,
    Tuple,
)


class A:
    def __init__(self, arg1):
        self.data = arg1

    def method1(self, arg1: int) -> Generator[int, int, int]:
        """
        Do something

        :param arg1:
        :type arg1: int
        """
        yield 1

    def method2(self, arg1: float):
        """
        Do something

        :param arg1:
        :type arg1: float
        """
        yield 2

    def method3(self, arg1: int):
        """
        Do something

        :param arg1:
        :type arg1: int
        :yield: Something to yield
        :rtype: int
        """
        print(1)

    def method4(self, arg1: int) -> Generator[int, int, int]:
        yield 2

    def method5(self, arg1: int) -> Generator[int, int, int]:
        """Do something else"""
        yield 2

    def method6(self, arg1: int) -> AsyncGenerator[int, int, int]:
        """
        Do something

        :param arg1:
        :type arg1: int
        """
        yield 2

    def method7a(self, arg1: int) -> Iterator[int]:
        """
        Do something

        :param arg1:
        :type arg1: int
        :yield: something
        :rtype: int
        """
        yield 1
        yield 2
        yield 3

    def method8a(self, arg1: int) -> Iterator[int]:
        """
        Do something

        :param arg1:
        :type arg1: int
        """
        yield 1
        yield 2
        yield 3

    def method7b(self, arg1: int) -> Iterable[int]:
        """
        Do something

        :param arg1:
        :type arg1: int
        :yield: something
        :rtype: int
        """
        i = 0
        while i < 10:
            yield i
            i += 1

    def method8b(self, arg1: int) -> Iterable[int]:
        """
        Do something

        :param arg1:
        :type arg1: int
        """
        i = 0
        while i < 10:
            yield i
            i += 1

    def method7c(self, data: list) -> AsyncIterator[int]:
        """
        Do something

        :param data:
        :type data: list
        :yield: something
        :rtype: int
        """
        yield from data

    def method8c(self, data: list) -> AsyncIterator[int]:
        """
        Do something

        :param data:
        :type data: list
        """
        yield from data

    def method7d(self, data: list) -> AsyncIterable[int]:
        """
        Do something

        :param data:
        :type data: list
        :yield: something
        :rtype: int
        """
        yield from data

    def method8d(self, data: list) -> AsyncIterable[int]:
        """
        Do something

        :param data:
        :type data: list
        """
        yield from data

    def zipLists1(
            self,
            list1: List[Any],
            list2: List[Any],
    ) -> Iterator[Tuple[Any, Any]]:
        """
        Zip 2 lists.

        :param list1: The first list
        :type list1: List[Any]
        :param list2: The second list
        :type list2: List[Any]
        :return: The zipped result
        """
        return zip(list1, list2)

    def zipLists2(
            self,
            list1: List[Any],
            list2: List[Any],
    ) -> Iterator[Tuple[Any, Any]]:
        """
        Zip 2 lists.

        :param list1: The first list
        :type list1: List[Any]
        :param list2: The second list
        :type list2: List[Any]
        :yield: The zipped result
        """
        return zip(list1, list2)

    def method9a(self, arg1: List[int]) -> str:
        """
        There should not be any violations in this method

        :param arg1: Arg 1
        :type arg1: List[int]
        :return: Return value
        :rtype: str
        """

        def inner9a(inner_arg1: List[int]) -> Iterable[str]:
            """
            Do something else

            :param inner_arg1: Inner arg 1
            :type inner_arg1: List[int]
            :yield: Values to yield
            :rtype: Iterable[str]
            """
            for i in inner_arg1:
                yield str(inner_arg1)

        return ','.join(inner9a(arg1))

    def method9b(self, arg1: List[int]) -> str:
        """
        There should not be any violations in the outer method

        :param arg1: Arg 1
        :type arg1: List[int]
        :return: Return value
        :rtype: str
        """

        def inner9b(inner_arg1: List[int]) -> Iterable[str]:
            """
            There should be DOC402 in this inner method

            :param inner_arg1: Inner arg 1
            :type inner_arg1: List[int]
            """
            for i in inner_arg1:
                yield str(inner_arg1)

        return ','.join(inner9b(arg1))

    def method9c(self, arg1: List[int]) -> str:
        """
        There should be DOC201 and DOC403 in the outer method

        :param arg1: Arg 1
        :type arg1: List[int]
        :yield: Values to yield
        :rtype: Iterable[str]
        """

        def inner9c(inner_arg1: List[int]) -> Iterable[str]:
            """
            There shouldn't be any violations in this inner method

            :param inner_arg1: Inner arg 1
            :type inner_arg1: List[int]
            :yield: Values to yield
            :rtype: Iterable[str]
            """
            for i in inner_arg1:
                yield str(inner_arg1)

        return ','.join(inner9c(arg1))

    def method9d(self, arg1: List[int]) -> Iterable[str]:
        """
        There should be DOC402 in this outer method

        :param arg1: Arg 1
        :type arg1: List[int]
        """

        def inner9d(inner_arg1: List[int]) -> Iterable[str]:
            """
            There should be DOC402 in this inner method

            :param inner_arg1: Innter arg 1
            :type inner_arg1: List[int]
            """
            for i in inner_arg1:
                yield str(inner_arg1)

        yield inner9d(arg1)

    def func10(self, arg0: bool) -> Iterable[int]:
        """
        There should be a DOC402 violation for this function

        :param arg0: Arg 0
        :type arg0: bool
        :raises ValueError: When there is a value error
        """
        for i in range(10):
            match i:
                case [0, 1]:
                    yield i
                case [2, 3]:
                    yield i + 1
                case _:
                    raise ValueError('Hello world')
