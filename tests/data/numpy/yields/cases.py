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

        Parameters
        ----------
        arg1 : int
        """
        yield 1

    def method2(self, arg1: float):
        """
        Do something

        Parameters
        ----------
        arg1 : float
        """
        yield 2

    def method3(self, arg1: int):
        """
        Do something

        Parameters
        ----------
        arg1 : int

        Yields
        ------
        int
            Something to yield
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

        Parameters
        ----------
        arg1 : int
        """
        yield 2

    def method7a(self, arg1: int) -> Iterator[int]:
        """
        Do something

        Parameters
        ----------
        arg1 : int

        Yields
        ------
        int
            something
        """
        yield 1
        yield 2
        yield 3

    def method8a(self, arg1: int) -> Iterator[int]:
        """
        Do something

        Parameters
        ----------
        arg1 : int
        """
        yield 1
        yield 2
        yield 3

    def method7b(self, arg1: int) -> Iterable[int]:
        """
        Do something

        Parameters
        ----------
        arg1 : int

        Yields
        ------
        int
            something
        """
        i = 0
        while i < 10:
            yield i
            i += 1

    def method8b(self, arg1: int) -> Iterable[int]:
        """
        Do something

        Parameters
        ----------
        arg1 : int
        """
        i = 0
        while i < 10:
            yield i
            i += 1

    def method7c(self, data: list) -> AsyncIterator[int]:
        """
        Do something

        Parameters
        ----------
        data : list

        Yields
        ------
        int
            something
        """
        yield from data

    def method8c(self, data: list) -> AsyncIterator[int]:
        """
        Do something

        Parameters
        ----------
        data : list
        """
        yield from data

    def method7d(self, data: list) -> AsyncIterable[int]:
        """
        Do something

        Parameters
        ----------
        data : list

        Yields
        ------
        int
            something
        """
        yield from data

    def method8d(self, data: list) -> AsyncIterable[int]:
        """
        Do something

        Parameters
        ----------
        data : list
        """
        yield from data

    def zipLists1(
            self,
            list1: List[Any],
            list2: List[Any],
    ) -> Iterator[Tuple[Any, Any]]:
        """
        Zip 2 lists.

        Parameters
        ----------
        list1 : List[Any]
            The first list
        list2 : List[Any]
            The second list

        Returns
        -------
        Iterator[Tuple[Any, Any]]
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

        Parameters
        ----------
        list1 : List[Any]
            The first list
        list2 : List[Any]
            The second list

        Yields
        -------
        Iterator[Tuple[Any, Any]]
            The zipped result
        """
        return zip(list1, list2)
