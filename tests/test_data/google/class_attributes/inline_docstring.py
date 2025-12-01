class MyClass1:
    """Simple class that has an inline docstring for its attributes."""

    field1: int = 5
    """int: An integer field with a default value."""

    field2: str = "default"
    """str: A string field with a default value."""

    field3: list[int]
    """list[int]: A list of integers field without a default value."""


class MyClass2:
    """Mix of documented and undocumented attributes."""

    documented_field: float = 3.14
    """float: A documented float field."""

    undocumented_field: bool = True


class MyClass3:
    """
    Mix of inline and block docstrings for attributes.

    Attributes:
        field1 (int): First field with block docstring.
        field5: Fifth field with block docstring.
    """

    field1: int = 10

    field2: str = "hello"
    """str: Second field with inline docstring."""

    field3: int = 5
    """int: Third field with inline docstring."""

    field4: bool
    """Fourth field with inline docstring, but no default value."""

    field5: bool = False
    """bool: Fifth field with inline docstring."""


class MyClass4:
    """
    Differing attribute and inline docstring types.

    Attributes:
        field1 (int): An integer field.
    """

    field1: str = "not an int"
    """str: This field is actually a string, not an int."""
