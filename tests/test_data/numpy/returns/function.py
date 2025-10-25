def func0():
    pass


def func1_1() -> None:
    pass


def func1_2() -> None:
    """"""
    pass


def func1_3() -> bool:
    """Something"""
    return True


def func1_4() -> bool:
    return False


def func1_5() -> None:
    """Something"""
    return None


def func1_6(arg1: int) -> None:
    """
    Something

    Parameters
    ----------
    arg1 : int
        Arg 1
    """
    return None


def func2(arg2: float, arg3: str) -> int | list[float]:
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


def func3() -> int:
    """
    Do something.

    Returns
    -------
    int
        Result
    """
    return 1


def func4() -> int:
    """
    Do something.

    Returns
    -------
    float
        Result
    """
    return 1.0


def func5() -> int:
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


def func6():
    """
    Returns
    -------
    int
        Something to return
    """
    print(123)


def func62() -> float:
    """
    Returns
    -------
    int
        Something to return
    """
    print(123)


def func7():
    """
    Returns
    -------
    int
        Something to return
    """
    return 123


def func81() -> Tuple[int, bool]:
    """
    If no summary here, the parser will mis-parse the return section

    Returns
    -------
    Tuple[int, bool]
        Something to return
    """
    return (1, 1.1)


def func82() -> Tuple[int, bool]:
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


def func91() -> Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]:
    """
    No violation should be reported here.

    Returns
    -------
    Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]
        The return value
    """
    print(1)


def func92() -> Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]:
    """
    No violation should be reported here.

    Returns
    -------
    Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]
        The return value
    """
    print(1)


def func93() -> Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]:
    """
    No violation should be reported here.

    Returns
    -------
    Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]
        The return value
    """
    print(1)


def func94() -> Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]:
    """
    No violation should be reported here.

    Returns
    -------
    Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]
        The return value
    """
    print(1)


def func95() -> Tuple[Dict[MyClass1, 'MyClass2'], List['MyClass3']]:
    """
    No violation should be reported here.

    Returns
    -------
    Tuple[Dict["MyClass1", MyClass2], List['MyClass3']]
        The return value
    """
    print(1)


def func101(arg0: float):
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


def func102(arg0: float):
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


def zipLists1(
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
