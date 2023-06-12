class MyClass:
    def __init__(self):
        pass

    def func1(self, arg1, arg2) -> int:
        """
        Do something

        Args:
            arg1: Arg 1
            arg2: Arg 2

        Returns:
            int: The return value
        """
        return 1

    def func2(self, arg1: int, arg2: float) -> int:
        """
        Do something

        Args:
            arg1: Arg 1
            arg2: Arg 2

        Returns:
            int: The return value
        """
        return 1

    def func3(self, arg1, arg2) -> int:
        """
        Do something

        Args:
            arg1 (int): Arg 1
            arg2 (float): Arg 2

        Returns:
            int: The return value
        """
        return 1

    def func4(self, arg1: int, arg2: float) -> int:
        """
        Do something

        Args:
            arg1 (int): Arg 1
            arg2 (float): Arg 2

        Returns:
            int: The return value
        """
        return 1

    def func5(self, arg1, arg2: float) -> int:
        """
        Do something

        Args:
            arg1 (int): Arg 1
            arg2: Arg 2

        Returns:
            int: The return value
        """
        return 1

    def func6(self, arg1: bool, arg2: float) -> int:
        """
        Do something

        Args:
            arg1 (int): Arg 1
            arg2 (float): Arg 2

        Returns:
            int: The return value
        """
        return 1

    def func7(self, arg1, arg2: float) -> int:
        """
        Do something

        Args:
            arg1: Arg 1
            arg2 (float): Arg 2

        Returns:
            int: The return value
        """
        return 1
