class A:
    """
    Some class

    Args:
        arg1
        arg2
    """

    def __init__(self):
        pass

    def method1(self, arg3: int) -> int:
        """
        Do something

        Args:
            arg3 (int): arg3

        Returns:
            int: The return value
        """
        return 2


def test(param: str | None = None,) -> str:
    """A test function

    Args:
        :param param: This is just a test

    Returns:
        str: A string
    """

    pass


def sphinx_type_directive(param: str) -> str:
    """A test function

    Args:
        :type param: str

    Returns:
        str: A string
    """

    pass


def sphinx_param_with_type(param: str) -> str:
    """A test function

    Args:
        :param str param: This is just a test

    Returns:
        str: A string
    """

    pass


def empty_google_arg_name(param: str) -> str:
    """A test function

    Args:
        : This is just a test

    Returns:
        str: A string
    """

    pass


class BadClassDoc:
    """A test class.

    Args:
        :param value: This class docstring is malformed.
    """

    def __init__(self, value: str) -> None:
        """Initialize the class.

        Args:
            value (str): A value.
        """

        self.value = value


class BadInitDoc:
    """A test class."""

    def __init__(self, value: str) -> None:
        """Initialize the class.

        Args:
            :param value: This constructor docstring is malformed.
        """

        self.value = value
