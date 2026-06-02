class A:
    """
    Some class.
    """

    def __init__(self):
        """
        Do something

        :param: This has no parameter name.
        """
        pass

    def method1(self, arg3: int) -> int:
        """
        Do something

        :param arg3: arg3
        :type arg3: int
        :return: The return value
        :rtype: int
        """
        return 2


def emptyParamName(param: str) -> str:
    """A test function.

    :param : This has no parameter name.
    :return: A string.
    :rtype: str
    """

    pass


def missingParamDirectiveArgument(param: str) -> str:
    """A test function.

    :param: This has no parameter name.
    :return: A string.
    :rtype: str
    """

    pass


class BadClassDoc:
    """A test class.

    :param : This class docstring has no parameter name.
    """

    def __init__(self, value: str) -> None:
        """Initialize the class.

        :param value: A value.
        :type value: str
        """

        self.value = value


class BadInitDoc:
    """A test class."""

    def __init__(self, value: str) -> None:
        """Initialize the class.

        :param: This constructor docstring has no parameter name.
        """

        self.value = value
