def func1(arg1: int = 5, arg2: str = 'hello') -> None:
    """Function with default arguments and no defaults in docstring
    (correct when check-arg-defaults=False)

    Args:
        arg1 (int): First argument
        arg2 (str): Second argument
    """
    pass
    """Function with default arguments and no defaults in docstring
    (correct when check-arg-defaults=False)

    Args:
        arg1 (int): First argument
        arg2 (str): Second argument
    """
    pass


def func2(arg1: int = 5, arg2: str = 'hello') -> None:
    """Function with default arguments and defaults in docstring (incorrect
    when check-arg-defaults=False)

    Args:
        arg1 (int, default=5): First argument
        arg2 (str, default="hello"): Second argument
    """
    pass


def func3(arg1: int = 10, arg2: str = 'world') -> None:
    """Function with default arguments and correct defaults in docstring
    (correct when check-arg-defaults=True)

    Args:
        arg1 (int, default=10): First argument
        arg2 (str, default="world"): Second argument
    """
    pass


def func4(arg1: int = 10, arg2: str = 'world') -> None:
    """Function with default arguments and wrong defaults in docstring
    (incorrect when check-arg-defaults=True)

    Args:
        arg1 (int, default=5): First argument with wrong default
        arg2 (str, default="hello"): Second argument with wrong default
    """
    pass


def func5(arg1: int = 42, arg2: str = 'test', arg3: bool = True) -> None:
    """Function with mixed default scenarios (some correct, some wrong when
    check-arg-defaults=True)

    Args:
        arg1 (int, default=42): Correct default
        arg2 (str, default="wrong"): Wrong default value
        arg3 (bool): Missing default value
    """
    pass


def func6(arg1: int, arg2: str = 'default') -> None:
    """Function with mix of args with and without defaults

    Args:
        arg1 (int): No default argument
        arg2 (str, default="default"): Argument with default (incorrect when check-arg-defaults=False)
    """
    pass


def func7(arg1: int, arg2: str = 'default') -> None:
    """Function with mix of args with and without defaults (correct when
    check-arg-defaults=False)

    Args:
        arg1 (int): No default argument
        arg2 (str): Argument with default but not shown in docstring
    """
    pass


class MyClass:
    def method1(self, arg1: int = 5, arg2: str = 'hello') -> None:
        """Method with default arguments and no defaults in docstring

        Args:
            arg1 (int): First argument
            arg2 (str): Second argument
        """
        pass

    def method2(self, arg1: int = 5, arg2: str = 'hello') -> None:
        """Method with default arguments and defaults in docstring

        Args:
            arg1 (int, default=5): First argument
            arg2 (str, default="hello"): Second argument
        """
        pass

    def method3(self, arg1: int = 10, arg2: str = 'world') -> None:
        """Method with default arguments and wrong defaults in docstring

        Args:
            arg1 (int, default=5): First argument with wrong default
            arg2 (str, default="hello"): Second argument with wrong default
        """
        pass


def func_with_complex_defaults(
        arg1: int,
        arg2: list = None,
        arg3: dict = None,
        arg4: str = 'complex_string',
) -> None:
    """Function with complex default values

    Args:
        arg1 (int): Integer with default
        arg2 (list, default=None): List with None default
        arg3 (dict, default=None): Dict with None default
        arg4 (str, default="complex_string"): String with complex default
    """
    if arg2 is None:
        arg2 = []
    if arg3 is None:
        arg3 = {}
    pass


def func_no_defaults(arg1: int, arg2: str) -> None:
    """Function with no default arguments

    Args:
        arg1 (int): First argument
        arg2 (str): Second argument
    """
    pass


def func_all_defaults(
        arg1: int = 1, arg2: str = 'test', arg3: bool = False
) -> None:
    """Function where all arguments have defaults

    Args:
        arg1 (int, default=1): First argument
        arg2 (str, default="test"): Second argument
        arg3 (bool, default=False): Third argument
    """
    pass


def func_single_quote_or_double_quote_dont_matter(
        arg1: str = 'hello',
        arg2: str = "world",
) -> None:
    """There should be no violation if checkArgDefaults is True.

    Args:
        arg1 (str, default="hello"): First argument
        arg2 (str, default='world'): Second argument
    """
    pass


def wrong_default_style(
    arg1: int = 1,
    arg2: str = 'test',
    arg3: bool = False,
    arg4: str = 'test',
) -> None:
    """Wrong default style

    Args:
        arg1 (int, default=1): First argument
        arg2 (str = "test"): Second argument
        arg3 (bool, defaults to False): Third argument
        arg4 (str, default 'test'): Fourth argument
    """
    pass


def space_does_not_matter(
    arg1: int = 1,
) -> None:
    """Extra space in docstring's default does not matter

    Args:
        arg1 (int, default      =   1): First argument
    """
    pass


def default_string_double_quote(
        arg1: str = "hello",
        arg2: str = "world",
        arg3: str = "morning",
) -> None:
    """
    Default string

    Args:
        arg1 (str, default=hello): This will trigger a violation
        arg2 (str, default="world"): This will be fine
        arg3 (str, default='morning'): This is also be fine
    """
    pass


def default_string_single_quote(
        arg1: str = 'hello',
        arg2: str = 'world',
        arg3: str = 'morning',
) -> None:
    """
    Default string

    Args:
        arg1 (str, default=hello): This will trigger a violation
        arg2 (str, default="world"): This will be fine
        arg3 (str, default='morning'): This is also be fine
    """
    pass
