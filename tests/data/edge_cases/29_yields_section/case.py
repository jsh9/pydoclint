# From https://github.com/jsh9/pydoclint/issues/254

def test_yield_with_typing_no_args() -> Generator[typing.Any]:
    """
    Testing the behaviour of pydoclint with a function which has specified the Generator via
    the typing module and has no arguments

    Yields:
        Generator123[typing.Any]: An iterable argument

    """
    yield [1]
