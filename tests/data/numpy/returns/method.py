class MyClass:
    def __init__(self):
        pass

    def func1_1(self) -> None:
        pass

    def func1_2(self) -> None:
        """"""
        pass

    def func1_3(self) -> bool:
        """Something"""
        return True

    def func1_4(self) -> bool:
        return False

    def func1_5(self) -> None:
        """Something"""
        return None

    def func1_6(self, arg1: int) -> None:
        """
        Something

        Parameters
        ----------
        arg1 : int
            Arg 1
        """
        return None

    def func2(self, arg2: float, arg3: str) -> int | list[float]:
        """
        Do something.

        Parameters
        ----------
        arg1 : int
            Arg 1

        Returns
        -------
        int
            Result
        """
        return 1

    def func3(self) -> int:
        """
        Do something.

        Returns
        -------
        int
            Result
        """
        return 1

    def func4(self) -> int:
        """
        Do something.

        Returns
        -------
        float
            Result
        """
        return 1.0

    def func5(self) -> int:
        """
        Do something.

        Returns
        -------
        int
            Result
        """

        def func52() -> None:
            """
            Do something else

            arg100: int
                Some arg
            """
            return None

        return 2

    def func6(self):
        """
        Returns
        -------
        int
            Something to return
        """
        print(123)

    def func62(self) -> float:
        """
        Returns
        -------
        int
            Something to return
        """
        print(123)

    def func7(self):
        """
        Returns
        -------
        int
            Something to return
        """
        return 123

    def func81(self) -> Tuple[int, bool]:
        """
        If no summary here, the parser will mis-parse the return section

        Returns
        -------
        Tuple[int, bool]
            Something to return
        """
        return (1, 1.1)

    def func82(self) -> Tuple[int, bool]:
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
