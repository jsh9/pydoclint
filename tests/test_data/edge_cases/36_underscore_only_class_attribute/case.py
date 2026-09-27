# Regression test for https://github.com/jsh9/pydoclint/issues/302
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
