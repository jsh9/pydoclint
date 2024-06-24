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
        """
        Do something.

        :param arg1: Arg 1
        :type arg1: int
        :param arg2: Arg 2
        :type arg2: float
        :return: None
        :rtype: None
        """
        self.arg1 = arg1
        self.arg2 = arg2


class C:
    """
    A class that does something

    :raises TypeError: Type error
    """

    def __init__(self, arg1: int, arg2: float) -> None:
        """
        Do something.

        :param arg1: Arg 1
        :type arg1: int
        :param arg2: Arg 2
        :type arg2: float

        :raises TypeError: Type error
        """
        self.arg1 = arg1
        self.arg2 = arg2

        if arg1 + arg2 == 0:
            raise ValueError('Something wrong')


class D:
    """
    A class that does something

    :yield: Thing to yield
    :ytype: int
    """

    def __init__(self, arg1: int, arg2: float) -> None:
        """
        Do something.

        :param arg1: Arg 1
        :type arg1: int
        :param arg2: Arg 2
        :type arg2: float

        :yield: Thing to yield
        :ytype: int
        """
        self.arg1 = arg1
        self.arg2 = arg2


class E:
    """
    A class that does something

    .. attribute :: attr1

    .. attribute :: attr2

        Arg 2
    """

    def __init__(self, arg1: int, arg2: float) -> None:
        """
        Do something.

        :param arg1: Arg 1
        :type arg1: int
        :param arg2: Arg 2
        :type arg2: float

        :raises: ValueError: When some values are invalid
        """
        self.arg1 = arg1
        self.arg2 = arg2

        if arg1 + arg2 == 0:
            raise ValueError('Something wrong')
