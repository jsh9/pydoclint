class MyClass1:
    """
    A class that holds some things.

    :attr name: The name
    :type name: str | bool | None
    :attr indices: The indices
    :type indices: pd.DataFrame
    :param arg1: The information
    :type arg1: float
    """

    name: str | bool | None
    index: pd.DataFrame

    hello: int = 1
    world: dict

    def __init__(self, arg1: int) -> None:
        self.arg1 = arg1

    def do_something(self, arg2: bool) -> int:
        """
        Do something.

        :param arg2: Arg 2
        :type arg2: str
        :return: Result
        :rtype: int
        """
        return 2


class MyClass2:
    """
    A class that holds some things.

    In this class, the class attributes and the instance attribute (self.arg1)
    are mixed together as attributes.

    :attr name: The name
    :type name: str
    :attr indices: The indices
    :type indices: int
    :attr arg1: The information
    :type arg1: float
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

        :param arg2: Arg 2
        :type arg2: str
        :return: Result
        :rtype: int
        """
        return 2


class MyClass3:
    """
    A class that holds some things.

    In this class, the class attributes and the instance attribute (self.arg1)
    are mixed together as parameters.

    :param name: The name
    :type name: str
    :param indices: The indices
    :type indices: int
    :param arg1: The information
    :type arg1: float
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

        :param arg2: Arg 2
        :type arg2: str
        :return: Result
        :rtype: int
        """
        return 2
