import dataclasses


@dataclasses.dataclass
class Result:
    """
    Class for storing stuff.

    Attributes
    ----------
    foo
        The foo.
    bar
        The bar.
    """

    _: dataclasses.KW_ONLY
    foo: int
    bar: int
