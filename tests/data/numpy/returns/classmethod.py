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
        int
            Result
        """
        return 1

    @classmethod
    def func3(cls) -> int:
        """
        Do something.

        Returns
        -------
        int
            Result
        """
        return 1

    @classmethod
    def func4(cls) -> int:
        """
        Do something.

        Returns
        -------
        float
            Result
        """
        return 1.0

    @classmethod
    def func5(cls) -> int:
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

    @classmethod
    def func6(cls):
        """
        Returns
        -------
        int
            Something to return
        """
        print(123)

    @classmethod
    def func62(cls) -> float:
        """
        Returns
        -------
        int
            Something to return
        """
        print(123)

    @classmethod
    def func7(cls):
        """
        Returns
        -------
        int
            Something to return
        """
        return 123

    @classmethod
    def func81(cls) -> Tuple[int, bool]:
        """
        If no summary here, the parser will mis-parse the return section

        Returns
        -------
        Tuple[int, bool]
            Something to return
        """
        return (1, 1.1)

    @classmethod
    def func82(cls) -> Tuple[int, bool]:
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

    @classmethod
    def func91(cls) -> Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]:
        """
        No violation should be reported here.

        Returns
        -------
        Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]
            The return value
        """
        print(1)

    @classmethod
    def func92(cls) -> Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]:
        """
        No violation should be reported here.

        Returns
        -------
        Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]
            The return value
        """
        print(1)

    @classmethod
    def func93(cls) -> Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]:
        """
        No violation should be reported here.

        Returns
        -------
        Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]
            The return value
        """
        print(1)

    @classmethod
    def func94(cls) -> Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]:
        """
        No violation should be reported here.

        Returns
        -------
        Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]
            The return value
        """
        print(1)

    @classmethod
    def func95(cls) -> Tuple[Dict[MyClass1, 'MyClass2'], List['MyClass3']]:
        """
        No violation should be reported here.

        Returns
        -------
        Tuple[Dict["MyClass1", MyClass2], List['MyClass3']]
            The return value
        """
        print(1)

    @classmethod
    def func101(cls, arg0: float):
        """
        Expected violations: DOC202, DOC203

        Parameters
        ----------
        arg0 : float
            Arg 0

        Returns
        -------
        bool
            Return value
        """

        def inner101(arg1: str) -> bool:
            """
            Expected violations: DOC201, DOC203

            Parameters
            ----------
            arg1 : str
                Arg 1
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

        Parameters
        ----------
        arg0 : float
            Arg 0
        """

        def inner102(arg1: str) -> bool:
            """
            There should not be any violations

            Parameters
            ----------
            arg1 : str
                Arg 1

            Returns
            -------
            bool
                Return value
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

        Parameters
        ----------
        list1 : List[Any]
            The first list
        list2 : List[Any]
            The second list

        Returns
        -------
        Iterator[Tuple[Any, int]]
            The zipped result
        """
        return zip(list1, list2)
