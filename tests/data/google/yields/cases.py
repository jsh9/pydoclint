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

        Args:
            arg1 (int):
        """
        yield 1

    def method2(self, arg1: float):
        """
        Do something

        Args:
            arg1 (float):
        """
        yield 2

    def method3(self, arg1: int):
        """
        Do something

        Args:
            arg1 (int):

        Yields:
            int: Something to yield
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

        Args:
            arg1 (int):
        """
        yield 2

    def method7a(self, arg1: int) -> Iterator[int]:
        """
        Do something

        Args:
            arg1 (int):

        Yields:
            int: something
        """
        yield 1
        yield 2
        yield 3

    def method8a(self, arg1: int) -> Iterator[int]:
        """
        Do something

        Args:
            arg1 (int):
        """
        yield 1
        yield 2
        yield 3

    def method7b(self, arg1: int) -> Iterable[int]:
        """
        Do something

        Args:
            arg1 (int):

        Yields:
            int: something
        """
        i = 0
        while i < 10:
            yield i
            i += 1

    def method8b(self, arg1: int) -> Iterable[int]:
        """
        Do something

        Args:
            arg1 (int):
        """
        i = 0
        while i < 10:
            yield i
            i += 1

    def method7c(self, data: list) -> AsyncIterator[int]:
        """
        Do something

        Args:
            data (list):

        Yields:
            int: something
        """
        yield from data

    def method8c(self, data: list) -> AsyncIterator[int]:
        """
        Do something

        Args:
            data (list):
        """
        yield from data

    def method7d(self, data: list) -> AsyncIterable[int]:
        """
        Do something

        Args:
            data (list):

        Yields:
            int: something
        """
        yield from data

    def method8d(self, data: list) -> AsyncIterable[int]:
        """
        Do something

        Args:
            data (list):
        """
        yield from data

    def zipLists1(
            self,
            list1: List[Any],
            list2: List[Any],
    ) -> Iterator[Tuple[Any, Any]]:
        """
        Zip 2 lists.

        Args:
            list1 (List[Any]) : The first list
            list2 (List[Any]) : The second list

        Returns:
            The zipped result
        """
        return zip(list1, list2)

    def zipLists2(
            self,
            list1: List[Any],
            list2: List[Any],
    ) -> Iterator[Tuple[Any, Any]]:
        """
        Zip 2 lists.

        Args:
            list1 (List[Any]) : The first list
            list2 (List[Any]) : The second list

        Yields:
            The zipped result
        """
        return zip(list1, list2)

    def method9a(self, arg1: List[int]) -> str:
        """
        There should not be any violations in this method

        Args:
            arg1 (List[int]): Arg 1

        Returns:
            str: Return value
        """

        def inner9a(inner_arg1: List[int]) -> Iterable[str]:
            """
            Do something else

            Args:
                inner_arg1 (List[int]): Inner arg 1

            Yields:
                Iterable[str]: Values to yield
            """
            for i in inner_arg1:
                yield str(inner_arg1)

        return ','.join(inner9a(arg1))

    def method9b(self, arg1: List[int]) -> str:
        """
        There should not be any violations in the outer method

        Args:
            arg1 (List[int]): Arg 1

        Returns:
            str: Return value
        """

        def inner9b(inner_arg1: List[int]) -> Iterable[str]:
            """
            There should be DOC402 in this inner method

            Args:
                inner_arg1 (List[int]): Inner arg 1
            """
            for i in inner_arg1:
                yield str(inner_arg1)

        return ','.join(inner9b(arg1))

    def method9c(self, arg1: List[int]) -> str:
        """
        There should be DOC201 and DOC403 in the outer method

        Args:
            arg1 (List[int]): Arg 1

        Yields:
            Iterable[str]: Values to yield
        """

        def inner9c(inner_arg1: List[int]) -> Iterable[str]:
            """
            There shouldn't be any violations in this inner method

            Args:
                inner_arg1 (List[int]): Inner arg 1

            Yields:
                Iterable[str]: Values to yield
            """
            for i in inner_arg1:
                yield str(inner_arg1)

        return ','.join(inner9c(arg1))

    def method9d(self, arg1: List[int]) -> Iterable[str]:
        """
        There should be DOC402 in this outer method

        Args:
            arg1 (List[int]): Arg 1
        """

        def inner9d(inner_arg1: List[int]) -> Iterable[str]:
            """
            There should be DOC402 in this inner method

            Args:
                inner_arg1 (List[int]): Inner arg 1
            """
            for i in inner_arg1:
                yield str(inner_arg1)

        yield inner9d(arg1)

    def method10a(self, n: int) -> Generator[str, None, None]:
        """Description

        Args:
            n (int): Description

        Yields:
            int: Description
        """
        yield from range(n)

    def method10b(self, n: int) -> Generator[tuple[float, ...], None, None]:
        """Foo

        Args:
            n (int): Description.

        Yields:
            tuple[float, ...]: Description.
        """
        yield from ((*self.bar, i) for i in range(self.baz))
