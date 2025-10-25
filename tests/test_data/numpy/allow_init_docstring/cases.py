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
        """
        Do something.

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
        self.arg1 = arg1
        self.arg2 = arg2


class C:
    """
    A class that does something

    Raises
    ------
    TypeError
        Type error
    """

    def __init__(self, arg1: int, arg2: float) -> None:
        """
        Do something.

        Parameters
        ----------
        arg1 : int
            Arg 1
        arg2 : float
            Arg 2

        Raises
        ------
        TypeError
            Type error
        """
        self.arg1 = arg1
        self.arg2 = arg2

        if arg1 + arg2 == 0:
            raise ValueError('Something wrong')


class D:
    """
    A class that does something

    Yields
    ------
    int
    """

    def __init__(self, arg1: int, arg2: float) -> None:
        """
        Do something.

        Parameters
        ----------
        arg1 : int
            Arg 1
        arg2 : float
            Arg 2

        Yields
        ------
        int
        """
        self.arg1 = arg1
        self.arg2 = arg2


class E:
    """
    A class that does something

    Attributes
    ----------
    attr1
    attr2
    """

    def __init__(self, arg1: int, arg2: float) -> None:
        """
        Do something.

        Parameters
        ----------
        arg1 : int
            Arg 1
        arg2 : float
            Arg 2

        Raises
        ------
        ValueError
            When some values are invalid
        """
        self.arg1 = arg1
        self.arg2 = arg2

        if arg1 + arg2 == 0:
            raise ValueError('Something wrong')
