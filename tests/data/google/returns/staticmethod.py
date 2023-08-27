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

        Args:
            arg1 (int): Arg 1
        """
        return None

    @staticmethod
    def func2(arg2: float, arg3: str) -> int | list[float]:
        """
        Do something.

        Args:
            arg1 (int): Arg 1

        Returns:
            int: Result
        """
        return 1

    @staticmethod
    def func3() -> int:
        """
        Do something.

        Returns:
            int: Result
        """
        return 1

    @staticmethod
    def func4() -> int:
        """
        Do something.

        Returns:
            float: Result
        """
        return 1.0

    @staticmethod
    def func5() -> int:
        """
        Do something.

        Returns:
            int: Result
        """

        def func52() -> None:
            """
            Do something else

            arg100 (int): Some arg
            """
            return None

        return 2

    @staticmethod
    def func6():
        """
        If no summary here, the parser will mis-parse the return section

        Returns:
            int: Something to return
        """
        print(123)

    @staticmethod
    def func62() -> float:
        """
        If no summary here, the parser will mis-parse the return section

        Returns:
            int: Something to return
        """
        print(123)

    @staticmethod
    def func7():
        """
        If no summary here, the parser will mis-parse the return section

        Returns:
            int: Something to return
        """
        return 123

    @staticmethod
    def func81() -> Tuple[int, bool]:
        """
        If no summary here, the parser will mis-parse the return section

        Returns:
            Tuple[int, bool]: Something to return
        """
        return (1, 1.1)

    @staticmethod
    def func82() -> Tuple[int, bool]:
        """
        If no summary here, the parser will mis-parse the return section

        Returns:
            int: Integer to return
            bool: Boolean to return
        """
        return (1, 1.1)

    @staticmethod
    def func91() -> Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]:
        """
        No violation should be reported here.

        Returns:
            Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]: Something
        """
        print(1)

    @staticmethod
    def func92() -> Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]:
        """
        No violation should be reported here.

        Returns:
            Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]: Something
        """
        print(1)

    @staticmethod
    def func93() -> Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]:
        """
        No violation should be reported here.

        Returns:
            Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]: Something
        """
        print(1)

    @staticmethod
    def func94() -> Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]:
        """
        No violation should be reported here.

        Returns:
            Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]: Something
        """
        print(1)

    @staticmethod
    def func95() -> Tuple[Dict[MyClass1, 'MyClass2'], List['MyClass3']]:
        """
        No violation should be reported here.

        Returns:
            Tuple[Dict["MyClass1", MyClass2], List['MyClass3']]: Something
        """
        print(1)

    @staticmethod
    def func101(arg0: float):
        """
        Expected violations: DOC202, DOC203

        Args:
            arg0 (float): Arg 0

        Returns:
            bool: Return value
        """

        def inner101(arg1: str) -> bool:
            """
            Expected violations: DOC201, DOC203

            Args:
                arg1 (str): Arg 1
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

        Args:
            arg0 (float): Arg 0
        """

        def inner102(arg1: str) -> bool:
            """
            There should not be any violations

            Args:
                arg1 (str): Arg 1

            Returns:
                bool: Return value
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

        Args:
            list1 (List[Any]) : The first list
            list2 (List[Any]) : The second list

        Returns:
            Iterator[Tuple[Any, int]]: The zipped result
        """
        return zip(list1, list2)
