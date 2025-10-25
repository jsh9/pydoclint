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

        :return: Something else
        :rtype: bool
        """
        return True

    @classmethod
    def func1_4(cls) -> bool:
        return False

    @classmethod
    def func1_5(cls) -> None:
        """Something

        :return: None
        :rtype: None
        """
        return None

    @classmethod
    def func1_6(cls) -> None:
        """
        Something

        :param arg1: Arg 1
        :type arg1: int
        :return: None
        :rtype: None
        """
        return None

    @classmethod
    def func2(cls, arg1: int, arg2: float | int | None) -> int | list[float]:
        """
        Do something.

        :param arg1: Arg 1
        :type arg1: int
        :return: Result
        :rtype: int
        """
        return 1

    @classmethod
    def func3(cls, arg1: int, arg2: float) -> int:
        """
        Do something.

        :param arg1: Arg 1
        :type arg1: int
        :param arg2: Arg 2
        :type arg2: float
        :param arg3: Arg 3
        :type arg3: Optional[Union[float, int, str]]
        :return: Result
        :rtype: int
        """
        return 1

    @classmethod
    async def func4(cls, arg1: int, arg2: float) -> int:
        """
        Do something.

        :param arg2: Arg 2
        :type arg2: float
        :param arg1: Arg 1
        :type arg1: int
        :return: Result
        :rtype: int
        """
        return 1

    @classmethod
    def func5(cls, arg1: int, arg2: float) -> int:
        """
        Do something.

        :param arg1: Arg 1
        :type arg1: list[str]
        :param arg2: Arg 2
        :type arg2: str
        :return: Result
        :rtype: int
        """
        return 1

    @classmethod
    def func6(cls, arg1: int, arg2: float) -> int:
        """
        Do something.

        :param arg2: Arg 2
        :type arg2: str
        :param arg1: Arg 1
        :type arg1: list[str]
        :return: Result
        :rtype: int
        """
        return 1

    @classmethod
    def func7(cls, arg1: int, arg2: float) -> int:
        """
        Do something.

        :param arg1: Arg 1
        :type arg1: int
        :param arg2: Arg 2
        :type arg2: float
        :return: Result
        :rtype: int
        """

        def func72(arg3: list, arg4: tuple, arg5: dict) -> None:
            """
            Do something else

            arg100: Some arg
            :type arg100: int
            :return: None
            :rtype: None
            """
            return None

        return 2

    @classmethod
    def func8(cls, arg1: 'MyClass', arg2: 'SomeClass') -> int:
        """
        Something

        :param arg1: Arg 1
        :type arg1: MyClass
        :param arg2: Arg 2
        :type arg2: SomeClass
        :return: Result
        :rtype: int
        """
        return MyClass()
