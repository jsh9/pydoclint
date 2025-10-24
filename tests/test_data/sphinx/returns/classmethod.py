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

        :param arg1: Arg 1
        :type arg1: int
        """
        return None

    @classmethod
    def func2(cls, arg2: float, arg3: str) -> int | list[float]:
        """
        Do something.

        :param arg1: Arg 1
        :type arg1: int
        :return: Result
        :rtype: int
        """
        return 1

    @classmethod
    def func3(cls) -> int:
        """
        Do something.

        :return: Result
        :rtype: int
        """
        return 1

    @classmethod
    def func4(cls) -> int:
        """
        Do something.

        :return: Result
        :rtype: float
        """
        return 1.0

    @classmethod
    def func5(cls) -> int:
        """
        Do something.

        :return: Result
        :rtype: int
        """

        def func52() -> None:
            """
            Do something else

            arg100: Some arg
            :type arg100: int
            """
            return None

        return 2

    @classmethod
    def func6(cls):
        """
        If no summary here, the parser will mis-parse the return section

        :return: Something to return
        :rtype: int
        """
        print(123)

    @classmethod
    def func62(cls) -> float:
        """
        If no summary here, the parser will mis-parse the return section

        :return: Something to return
        :rtype: int
        """
        print(123)

    @classmethod
    def func7(cls):
        """
        If no summary here, the parser will mis-parse the return section

        :return: Something to return
        :rtype: int
        """
        return 123

    @classmethod
    def func81(cls) -> Tuple[int, bool]:
        """
        If no summary here, the parser will mis-parse the return section

        :return: Something to return
        :rtype: Tuple[int, bool]
        """
        return (1, 1.1)

    @classmethod
    def func82(cls) -> Tuple[int, bool]:
        """
        If no summary here, the parser will mis-parse the return section

        :return: Integer to return
        :rtype: int
        :return: Boolean to return
        :rtype: bool
        """
        return (1, 1.1)

    @classmethod
    def func91(cls) -> Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]:
        """
        No violation should be reported here.

        :return: Something
        :rtype: Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]
        """
        print(1)

    @classmethod
    def func92(cls) -> Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]:
        """
        No violation should be reported here.

        :return: Something
        :rtype: Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]
        """
        print(1)

    @classmethod
    def func93(cls) -> Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]:
        """
        No violation should be reported here.

        :return: Something
        :rtype: Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]
        """
        print(1)

    @classmethod
    def func94(cls) -> Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]:
        """
        No violation should be reported here.

        :return: Something
        :rtype: Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]
        """
        print(1)

    @classmethod
    def func95(cls) -> Tuple[Dict[MyClass1, 'MyClass2'], List['MyClass3']]:
        """
        No violation should be reported here.

        :return: Something
        :rtype: Tuple[Dict["MyClass1", MyClass2], List['MyClass3']]
        """
        print(1)

    @classmethod
    def func101(cls, arg0: float):
        """
        Expected violations: DOC202, DOC203

        :param arg0: Arg 0
        :type arg0: float
        :return: Return value
        :rtype: bool
        """

        def inner101(arg1: str) -> bool:
            """
            Expected violations: DOC201, DOC203

            :param arg1: Arg 1
            :type arg1: str
            """
            if arg1 > 'a':
                return True
            else:
                return False

        print(2)

    @classmethod
    def func102(cls, arg0: float):
        """
        There should not be any violations

        :param arg0: Arg 0
        :type arg0: float
        """

        def inner102(arg1: str) -> bool:
            """
            There should not be any violations

            :param arg1: Arg 1
            :type arg1: str
            :return: Return value
            :rtype: bool
            """
            if arg1 > 'a':
                return True
            else:
                return False

        print(2)

    @classmethod
    def zipLists1(
            cls,
            list1: List[Any],
            list2: List[Any],
    ) -> Iterator[Tuple[Any, Any]]:
        """
        Zip 2 lists.

        :param list1: The first list
        :type list1: List[Any]
        :param list2: The second list
        :type list2: List[Any]
        :return: The zipped list
        :rtype: Iterator[Tuple[Any, int]]
        """
        return zip(list1, list2)
