class MyClass1:
    """
    A class that holds some things.

    Attributes
    ----------
    name : str
        The name
    indices : int
        The indices

    Parameters
    ----------
    arg1 : float
        The information
    """

    name: str
    index: int

    hello: int = 1
    world: dict

    def __init__(self, arg1: int) -> None:
        self.arg1 = arg1

    def do_something(self, arg2: bool) -> int:
        """
        Do something.

        Parameters
        ----------
        arg2 : str
            Arg 2

        Returns
        -------
        int
            Result
        """
        return 2


class MyClass2:
    """
    A class that holds some things.

    In this class, the class attributes and the instance attribute (self.arg1)
    are mixed together in the "Attributes" section of the docstring.

    Attributes
    ----------
    name : str
        The name
    indices : int
        The indices
    arg1 : float
        The information
    """

    name: str
    index: int

    hello: int = 1
    world: dict

    def __init__(self, arg1: int) -> None:
        self.arg1 = arg1

    def do_something(self, arg2: bool) -> int:
        """
        Do something.

        Parameters
        ----------
        arg2 : str
            Arg 2

        Returns
        -------
        int
            Result
        """
        return 2


class MyClass3:
    """
    A class that holds some things.

    In this class, the class attributes and the instance attribute (self.arg1)
    are mixed together in the "Parameters" section of the docstring.

    Parameters
    ----------
    name : str
        The name
    indices : int
        The indices
    arg1 : float
        The information
    """

    name: str
    index: int

    hello: int = 1
    world: dict

    def __init__(self, arg1: int) -> None:
        self.arg1 = arg1

    def do_something(self, arg2: bool) -> int:
        """
        Do something.

        Parameters
        ----------
        arg2 : str
            Arg 2

        Returns
        -------
        int
            Result
        """
        return 2
