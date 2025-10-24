class MyClass:
    def __init__(self):
        pass

    def func1_1(self, arg1: int, arg2: float) -> None:
        pass

    def func1_1a(self, arg1: int, arg2: float) -> None:
        self.func2(arg1, arg2)

    def func1_2(self, arg1: int, arg2: float) -> None:
        """"""
        pass

    def func1_3(self, arg1: str, arg2: list[int]) -> bool:
        """Something

        :return: Something else
        :rtype: bool
        """
        return True

    def func1_4(self) -> bool:
        return False

    def func1_5(self) -> None:
        """Something

        :return: None
        :rtype: None
        """
        return None

    def func1_6(self) -> None:
        """
        Something

        :param arg1: Arg 1
        :type arg1: int
        :return: None
        :rtype: None
        """
        return None

    def func2(self, arg1: int, arg2: float | int | None) -> int | list[float]:
        """
        Do something.

        :param arg1: Arg 1
        :type arg1: int
        :return: Result
        :rtype: int
        """
        return 1

    def func3(self, arg1: int, arg2: float) -> int:
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

    async def func4(self, arg1: int, arg2: float) -> int:
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

    def func5(self, arg1: int, arg2: float) -> int:
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

    def func6(self, arg1: int, arg2: float) -> int:
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

    def func7(self, arg1: int, arg2: float) -> int:
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

    def func8(self, arg1: 'MyClass', arg2: 'SomeClass') -> int:
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
