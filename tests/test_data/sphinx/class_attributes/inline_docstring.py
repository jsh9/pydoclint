class MyClass1:
    """Simple class that has an inline docstring for its attributes."""

    field1: int = 5
    """An integer field with a default value."""

    field2: str = "default"
    """A string field with a default value."""

    field3: list[int]
    """A list of integers field without a default value."""


class MyClass2:
    """Mix of documented and undocumented attributes."""

    documented_field: float = 3.14
    """A documented float field."""

    undocumented_field: bool = True


class MyClass3:
    """
    Mix of inline and block docstrings for attributes.

    .. attribute :: field1
        :type: int
        First field with block docstring.
    .. attribute :: field5
        Fifth field with block docstring.
    """

    field1: int = 10

    field2: str = "hello"
    """Second field with inline docstring."""

    field3: int = 5
    """Third field with inline docstring."""

    field4: bool
    """Fourth field with inline docstring, but no default value."""

    field5: bool = False
    """Fifth field with inline docstring."""


class MyClass4:
    """
    Differing attribute and inline docstring types.

    .. attribute :: field1
        :type: int
        An integer field.
    """

    field1: str = "not an int"
    """This field is actually a string, not an int."""
