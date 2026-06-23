# From https://github.com/jsh9/pydoclint/issues/254

def test_yield_with_typing_no_args() -> Generator[typing.Any]:
    """
    Testing the behaviour of pydoclint with a function which has specified the Generator via
    the typing module and has no arguments

    Yields:
        Generator123[typing.Any]: An iterable argument

    """
    yield [1]


# From https://github.com/jsh9/pydoclint/issues/279

def yield_5() -> Generator[int]:
    """
    Testing that a single-argument Generator annotation has its yield type
    extracted correctly (instead of the whole annotation).

    Yields:
        int: 5.

    """
    yield 5
