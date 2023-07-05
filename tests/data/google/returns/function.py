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

    Args:
        arg1 (int): Arg 1
    """
    return None


def func2(arg2: float, arg3: str) -> int | list[float]:
    """
    Do something.

    Args:
        arg1 (int): Arg 1

    Returns:
        int: Result
    """
    return 1


def func3() -> int:
    """
    Do something.

    Returns:
        int: Result
    """
    return 1


def func4() -> int:
    """
    Do something.

    Returns:
        float: Result
    """
    return 1.0


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


def func6():
    """
    If no summary here, the parser will mis-parse the return section

    Returns:
        int: Something to return
    """
    print(123)


def func62() -> float:
    """
    If no summary here, the parser will mis-parse the return section

    Returns:
        int: Something to return
    """
    print(123)


def func7():
    """
    If no summary here, the parser will mis-parse the return section

    Returns:
        int: Something to return
    """
    return 123


def func81() -> Tuple[int, bool]:
    """
    If no summary here, the parser will mis-parse the return section

    Returns:
        Tuple[int, bool]: Something to return
    """
    return (1, 1.1)


def func82() -> Tuple[int, bool]:
    """
    If no summary here, the parser will mis-parse the return section

    Returns:
        int: Integer to return
        bool: Boolean to return
    """
    return (1, 1.1)


def func91() -> Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]:
    """
    No violation should be reported here.

    Returns:
        Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]: Something
    """
    print(1)


def func92() -> Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]:
    """
    No violation should be reported here.

    Returns:
        Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]: Something
    """
    print(1)


def func93() -> Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]:
    """
    No violation should be reported here.

    Returns:
        Tuple[Dict['MyClass1', 'MyClass2'], List['MyClass3']]: Something
    """
    print(1)


def func94() -> Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]:
    """
    No violation should be reported here.

    Returns:
        Tuple[Dict[MyClass1, MyClass2], List[MyClass3]]: Something
    """
    print(1)


def func95() -> Tuple[Dict[MyClass1, 'MyClass2'], List['MyClass3']]:
    """
    No violation should be reported here.

    Returns:
        Tuple[Dict["MyClass1", MyClass2], List['MyClass3']]: Something
    """
    print(1)
