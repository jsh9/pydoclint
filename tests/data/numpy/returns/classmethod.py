class MyClass:
    def __init__(self):
        pass

    @classmethod
    def func1_1(cls) -> None:
        pass

    @classmethod
    def func1_2(cls) -> None:
        """"""
        pass

    @classmethod
    def func1_3(cls) -> bool:
        """Something"""
        return True

    @classmethod
    def func1_4(cls) -> bool:
        return False

    @classmethod
    def func1_5(cls) -> None:
        """Something"""
        return None

    @classmethod
    def func1_6(cls, arg1: int) -> None:
        """
        Something

        Parameters
        ----------
        arg1 : int
            Arg 1
        """
        return None

    @classmethod
    def func2(cls, arg2: float, arg3: str) -> int | list[float]:
        """
        Do something.

        Parameters
        ----------
        arg1 : int
            Arg 1

        Returns
        -------
        int :
            Result
        """
        return 1

    @classmethod
    def func3(cls) -> int:
        """
        Do something.

        Returns
        -------
        int :
            Result
        """
        return 1

    @classmethod
    def func4(cls) -> int:
        """
        Do something.

        Returns
        -------
        float :
            Result
        """
        return 1.0

    @classmethod
    def func5(cls) -> int:
        """
        Do something.

        Returns
        -------
        int :
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

    @classmethod
    def func6(cls):
        """
        Returns
        -------
        int :
            Something to return
        """
        print(123)

    @classmethod
    def func62(cls) -> float:
        """
        Returns
        -------
        int :
            Something to return
        """
        print(123)

    @classmethod
    def func7(cls):
        """
        Returns
        -------
        int :
            Something to return
        """
        return 123

    @classmethod
    def func81(cls) -> Tuple[int, bool]:
        """
        If no summary here, the parser will mis-parse the return section

        Returns
        -------
        Tuple[int, bool] :
            Something to return
        """
        return (1, 1.1)

    @classmethod
    def func82(cls) -> Tuple[int, bool]:
        """
        If no summary here, the parser will mis-parse the return section

        Returns
        -------
        int :
            Integer to return
        bool :
            Boolean to return
        """
        return (1, 1.1)
