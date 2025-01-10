# From: https://github.com/jsh9/pydoclint/issues/198

@pytest.fixture
def setup_custom_logger(caplog: pytest.LogCaptureFixture) -> Generator[None]:
    """
    Set up a custom logger.

    Parameters
    ----------
    caplog : pytest.LogCaptureFixture
        Pytest logging capture fixture.

    Yields
    ------
    None
        Yield to run test before cleanup.
    """
    # Set class
    logging.setLoggerClass(CustomLogger)
    # Set new format
    format_copy = caplog.handler.formatter._fmt  # type: ignore[union-attr]
    caplog.handler.setFormatter(logging.Formatter('%(id_string)s : %(message)s'))

    yield

    caplog.handler.setFormatter(logging.Formatter(format_copy))
    # Reset logger class
    logging.setLoggerClass(logging.Logger)



@pytest.fixture
def setup_custom_logger2(caplog: pytest.LogCaptureFixture) -> Generator[None, None, None]:
    """
    Set up a custom logger.

    Parameters
    ----------
    caplog : pytest.LogCaptureFixture
        Pytest logging capture fixture.

    Yields
    ------
    None
        Yield to run test before cleanup.
    """
    # Set class
    logging.setLoggerClass(CustomLogger)
    # Set new format
    format_copy = caplog.handler.formatter._fmt  # type: ignore[union-attr]
    caplog.handler.setFormatter(logging.Formatter('%(id_string)s : %(message)s'))

    yield

    caplog.handler.setFormatter(logging.Formatter(format_copy))
    # Reset logger class
    logging.setLoggerClass(logging.Logger)
