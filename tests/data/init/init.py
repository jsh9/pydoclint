class A:
    """
    A class that does something

    Parameters
    ----------
    arg1 : int
        Arg 1
    arg2 : float
        Arg 2
    """

    def __init__(self, arg1: int, arg2: float) -> None:
        """Initialize the class"""
        self.arg1 = arg1
        self.arg2 = arg2


class B:
    """
    A class that does something

    Parameters
    ----------
    arg1 : int
        Arg 1
    arg2 : float
        Arg 2

    Returns
    -------
    None
    """

    def __init__(self, arg1: int, arg2: float) -> None:
        self.arg1 = arg1
        self.arg2 = arg2


class C:
    """
    A class that does something

    Parameters
    ----------
    arg1 : int
        Arg 1
    arg2 : float
        Arg 2

    Returns
    -------
    None
    """

    def __init__(self, arg1: int, arg2: str) -> None:
        self.arg1 = arg1
        self.arg2 = arg2


class D:
    """
    A class that does something

    Parameters
    ----------
    var1 : list
        Var 1
    var2 : dict
        Var 2

    Returns
    -------
    None
    """

    def __init__(self, arg1: int, arg2: float) -> None:
        self.arg1 = arg1
        self.arg2 = arg2


class E:
    def __init__(self, arg1) -> None:
        self.arg1 = arg1
