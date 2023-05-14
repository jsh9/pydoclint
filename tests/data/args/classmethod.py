class MyClass:
    def __init__(self):
        pass

    @classmethod
    def func1_1(cls, arg1: int, arg2: float) -> None:
        pass

    @classmethod
    def func1_1a(cls, arg1: int, arg2: float) -> None:
        cls.func2(arg1, arg2)

    @classmethod
    def func1_2(cls, arg1: int, arg2: float) -> None:
        """"""
        pass

    @classmethod
    def func1_3(cls, arg1: str, arg2: list[int]) -> bool:
        """Something

        Returns
        -------
        bool
            Something else
        """
        return True

    @classmethod
    def func1_4(cls) -> bool:
        return False

    @classmethod
    def func1_5(cls) -> None:
        """Something

        Returns
        -------
        None
        """
        return None

    @classmethod
    def func1_6(cls) -> None:
        """
        Something

        Parameters
        ----------
        arg1 : int
            Arg 1

        Returns
        -------
        None
        """
        return None

    @classmethod
    def func2(cls, arg1: int, arg2: float | int | None) -> int | list[float]:
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
    def func3(cls, arg1: int, arg2: float) -> int:
        """
        Do something.

        Parameters
        ----------
        arg1 : int
            Arg 1
        arg2 : float
            Arg 2
        arg3 : Optional[Union[float, int, str]]
            Arg 3

        Returns
        -------
        int :
            Result
        """
        return 1

    @classmethod
    async def func4(cls, arg1: int, arg2: float) -> int:
        """
        Do something.

        Parameters
        ----------
        arg2 : float
            Arg 2
        arg1 : int
            Arg 1

        Returns
        -------
        int :
            Result
        """
        return 1

    @classmethod
    def func5(cls, arg1: int, arg2: float) -> int:
        """
        Do something.

        Parameters
        ----------
        arg1 : list[str]
            Arg 1
        arg2 : str
            Arg 2

        Returns
        -------
        int :
            Result
        """
        return 1

    @classmethod
    def func6(cls, arg1: int, arg2: float) -> int:
        """
        Do something.

        Parameters
        ----------
        arg2 : str
            Arg 2
        arg1 : list[str]
            Arg 1

        Returns
        -------
        int :
            Result
        """
        return 1

    @classmethod
    def func7(cls, arg1: int, arg2: float) -> int:
        """
        Do something.

        Parameters
        ----------
        arg1 : int
            Arg 1
        arg2 : float
            Arg 2

        Returns
        -------
        int :
            Result
        """

        def func72(arg3: list, arg4: tuple, arg5: dict) -> None:
            """
            Do something else

            arg100: int
                Some arg

            Returns
            -------
            None
            """
            return None

        return 2

    @classmethod
    def func8(cls, arg1: 'MyClass', arg2: 'SomeClass') -> int:
        """
        Something

        Parameters
        ----------
        arg1 : MyClass
            Arg 1
        arg2 : SomeClass
            Arg 2

        Returns
        -------
        int
            Result
        """
        return MyClass()
