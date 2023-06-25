class MyClass:
    def __init__(self):
        pass

    @staticmethod
    def func1_1() -> None:
        pass

    @staticmethod
    def func1_2() -> None:
        """"""
        pass

    @staticmethod
    def func1_3() -> bool:
        """Something"""
        return True

    @staticmethod
    def func1_4() -> bool:
        return False

    @staticmethod
    def func1_5() -> None:
        """Something"""
        return None

    @staticmethod
    def func1_6(arg1: int) -> None:
        """
        Something

        Parameters
        ----------
        arg1 : int
            Arg 1
        """
        return None

    @staticmethod
    def func2(arg2: float, arg3: str) -> int | list[float]:
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

    @staticmethod
    def func3() -> int:
        """
        Do something.

        Returns
        -------
        int :
            Result
        """
        return 1

    @staticmethod
    def func4() -> int:
        """
        Do something.

        Returns
        -------
        float :
            Result
        """
        return 1.0

    @staticmethod
    def func5() -> int:
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

    @staticmethod
    def func6():
        """
        Returns
        -------
        int :
            Something to return
        """
        print(123)

    @staticmethod
    def func62() -> float:
        """
        Returns
        -------
        int :
            Something to return
        """
        print(123)

    @staticmethod
    def func7():
        """
        Returns
        -------
        int :
            Something to return
        """
        return 123

    @staticmethod
    def func81() -> Tuple[int, bool]:
        """
        If no summary here, the parser will mis-parse the return section

        Returns
        -------
        Tuple[int, bool] :
            Something to return
        """
        return (1, 1.1)

    @staticmethod
    def func82() -> Tuple[int, bool]:
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
