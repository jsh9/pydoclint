class MyClass0:
    """
    My class.

    :param attr1: Attr 1
    :type attr1: int
    :param attr2: Attr 2
    :type attr2: str
    """

    attr1: int
    attr2: str

    def __init__(self, arg1: list) -> None:
        """
        Initialize an object

        :param arg1: Arg 1
        :type arg1: list
        """
        self.arg1 = arg1


class MyClass1:
    """
    My class.

    :param attr1: Attr 1
    :type attr1: int
    :param attr2: Attr 2
    :type attr2: bool
    """

    attr1: int
    attr2: str

    def __init__(self, arg1: list) -> None:
        """
        Initialize an object

        :param arg1: Arg 1
        :type arg1: dict
        """
        self.arg1 = arg1


class MyClass2:
    """
    My class.

    :param attr1: Attr 1
    :type attr1: int
    :param attr2: Attr 2
    :type attr2: bool
    :param arg1: Arg 1
    :type arg1: dict
    """

    attr1: int
    attr2: str

    def __init__(self, arg1: list) -> None:
        self.arg1 = arg1


class MyClass3:
    attr1: int
    attr2: str

    def __init__(self, arg1: list) -> None:
        """
        My class.

        :param attr1: Attr 1
        :type attr1: int
        :param attr2: Attr 2
        :type attr2: bool
        :param arg1: Arg 1
        :type arg1: dict
        """
        self.arg1 = arg1
