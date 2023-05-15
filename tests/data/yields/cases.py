from typing import Generator


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
