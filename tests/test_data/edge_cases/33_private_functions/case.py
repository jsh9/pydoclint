
def _test_private_function() -> int:
    """test function

    Returns:
        bool: With incorrect argument
    """
    return 2

class TestClass:
    """
    Docstring for TestClass, this will still be checked if
    skip-checking-short-docstrings is False.
    """

    def __init__(self) -> None:
        """This init will still be checked if
        skip-checking-short-docstrings is False.
        """

    def _private_method(self, i: int) -> bool:
        """Test method

        Args:
            i (bool): With incorrect argument type

        Returns:
            bool: Always returns False
        """

        def inner_method() -> bool:
            """inner method should also be skipped as it is inside a
            private method.

            Returns:
                int: An incorrect return type.
            """
            return False
        return inner_method()

    def __private_name_mangled_method(self, i: int) -> bool:
        """Name mangled test method

        Args:
            i (bool): With incorrect argument type

        Returns:
            bool: Always returns False
        """
        return False
