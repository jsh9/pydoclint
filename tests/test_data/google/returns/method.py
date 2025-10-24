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

        Args:
            arg1 (int): Arg 1
        """
        return None

    def func2(self, arg2: float, arg3: str) -> int | list[float]:
        """
        Do something.

        Args:
            arg1 (int): Arg 1

        Returns:
            int: Result
        """
        return 1

    def func3(self) -> int:
        """
        Do something.

        Returns:
            int: Result
        """
        return 1

    def func4(self) -> int:
        """
        Do something.

        Returns:
            float: Result
        """
        return 1.0

    def func5(self) -> int:
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

    def func6(self):
        """
        If no summary here, the parser will mis-parse the return section

        Returns:
            int: Something to return
        """
        print(123)

    def func62(self) -> float:
        """
        If no summary here, the parser will mis-parse the return section

        Returns:
            int: Something to return
        """
        print(123)

    def func7(self):
        """
        If no summary here, the parser will mis-parse the return section

        Returns:
            int: Something to return
        """
        return 123

    def func81(self) -> Tuple[int, bool]:
        """
        If no summary here, the parser will mis-parse the return section

        Returns:
            Tuple[int, bool]: Something to return
        """
        return (1, 1.1)

    def func82(self) -> Tuple[int, bool]:
        """
        If no summary here, the parser will mis-parse the return section

        Returns:
            int: Integer to return
            bool: Boolean to return
        """
        return (1, 1.1)

    def func91(self) -> Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]:
        """
        No violation should be reported here.

        Returns:
            Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]: Something
        """
        print(1)

    def func92(self) -> Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]:
        """
        No violation should be reported here.

        Returns:
            Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]: Something
        """
        print(1)

    def func93(self) -> Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]:
        """
        No violation should be reported here.

        Returns:
            Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]: Something
        """
        print(1)

    def func94(self) -> Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]:
        """
        No violation should be reported here.

        Returns:
            Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]: Something
        """
        print(1)

    def func95(self) -> Tuple[Dict[MyClass1, 'MyClass2'], List['MyClass3']]:
        """
        No violation should be reported here.

        Returns:
            Tuple[Dict["MyClass1", MyClass2], List['MyClass3']]: Something
        """
        print(1)

    def func101(self, arg0: float):
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

    def func102(self, arg0: float):
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

    def zipLists1(
            self,
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
