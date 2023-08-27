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

        :param arg1: Arg 1
        :type arg1: int
        """
        return None

    @staticmethod
    def func2(arg2: float, arg3: str) -> int | list[float]:
        """
        Do something.

        :param arg1: Arg 1
        :type arg1: int
        :return: Result
        :rtype: int
        """
        return 1

    @staticmethod
    def func3() -> int:
        """
        Do something.

        :return: Result
        :rtype: int
        """
        return 1

    @staticmethod
    def func4() -> int:
        """
        Do something.

        :return: Result
        :rtype: float
        """
        return 1.0

    @staticmethod
    def func5() -> int:
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

    @staticmethod
    def func6():
        """
        If no summary here, the parser will mis-parse the return section

        :return: Something to return
        :rtype: int
        """
        print(123)

    @staticmethod
    def func62() -> float:
        """
        If no summary here, the parser will mis-parse the return section

        :return: Something to return
        :rtype: int
        """
        print(123)

    @staticmethod
    def func7():
        """
        If no summary here, the parser will mis-parse the return section

        :return: Something to return
        :rtype: int
        """
        return 123

    @staticmethod
    def func81() -> Tuple[int, bool]:
        """
        If no summary here, the parser will mis-parse the return section

        :return: Something to return
        :rtype: Tuple[int, bool]
        """
        return (1, 1.1)

    @staticmethod
    def func82() -> Tuple[int, bool]:
        """
        If no summary here, the parser will mis-parse the return section

        :return: Integer to return
        :rtype: int
        :return: Boolean to return
        :rtype: bool
        """
        return (1, 1.1)

    @staticmethod
    def func91() -> Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]:
        """
        No violation should be reported here.

        :return: Something
        :rtype: Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]
        """
        print(1)

    @staticmethod
    def func92() -> Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]:
        """
        No violation should be reported here.

        :return: Something
        :rtype: Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]
        """
        print(1)

    @staticmethod
    def func93() -> Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]:
        """
        No violation should be reported here.

        :return: Something
        :rtype: Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]
        """
        print(1)

    @staticmethod
    def func94() -> Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]:
        """
        No violation should be reported here.

        :return: Something
        :rtype: Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]
        """
        print(1)

    @staticmethod
    def func95() -> Tuple[Dict[MyClass1, 'MyClass2'], List['MyClass3']]:
        """
        No violation should be reported here.

        :return: Something
        :rtype: Tuple[Dict["MyClass1", MyClass2], List['MyClass3']]
        """
        print(1)

    @staticmethod
    def func101(arg0: float):
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

    @staticmethod
    def func102(arg0: float):
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

    @staticmethod
    def zipLists1(
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
