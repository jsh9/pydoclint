class A:
    """
    A class that does something

    :param arg1: Arg 1
    :type arg1: int
    :param arg2: Arg 2
    :type arg2: float
    """

    def __init__(self, arg1: int, arg2: float) -> None:
        """Initialize the class"""
        self.arg1 = arg1
        self.arg2 = arg2


class B:
    """
    A class that does something

    :param arg1: Arg 1
    :type arg1: int
    :param arg2: Arg 2
    :type arg2: float
    :return: None
    :rtype: None
    """

    def __init__(self, arg1: int, arg2: float) -> None:
        self.arg1 = arg1
        self.arg2 = arg2


class C:
    """
    A class that does something

    :param arg1: Arg 1
    :type arg1: int
    :param arg2: Arg 2
    :type arg2: float
    :return: None
    :rtype: None
    """

    def __init__(self, arg1: int, arg2: str) -> None:
        self.arg1 = arg1
        self.arg2 = arg2


class D:
    """
    A class that does something

    :param var1: Var 1
    :type var1: list
    :param var2: Var 2
    :type var2: dict
    :return: None
    :rtype: None
    """

    def __init__(self, arg1: int, arg2: float) -> None:
        self.arg1 = arg1
        self.arg2 = arg2


class E:
    def __init__(self, arg1) -> None:
        self.arg1 = arg1
