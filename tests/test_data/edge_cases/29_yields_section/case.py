def test_yield_with_typing_no_args() -> Generator[typing.Any]:
    """
    Testing the behaviour of pydoclint with a function which has specified the Generator via
    the typing module and has no arguments.

    From https://github.com/jsh9/pydoclint/issues/254

    Yields:
        Generator123[typing.Any]: An iterable argument

    """
    yield [1]


def yield_5() -> Generator[int]:
    """
    Testing that a single-argument Generator annotation has its yield type
    extracted correctly (instead of the whole annotation).

    From https://github.com/jsh9/pydoclint/issues/279

    Yields:
        int: 5.

    """
    yield 5


def invalid_iterator_extra_arg() -> Iterator[int, str]:
    """
    Testing that an Iterator annotation with extra args is not normalized to
    its first argument.

    PEP 696 defines defaults for Generator's SendType and ReturnType, so
    Generator[int, str] can be expanded meaningfully. Iterator has no matching
    trailing type parameters, so Iterator[int, str] must stay as written and
    trigger a yield-type mismatch.

    From https://github.com/jsh9/pydoclint/issues/279

    Yields:
        int: 1.

    """
    yield 1
