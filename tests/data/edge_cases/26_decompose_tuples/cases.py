# From: https://github.com/jsh9/pydoclint/issues/223

import datetime


def example_1() -> tuple[datetime.datetime]:
    """Return a singleton tuple of a datetime

    Returns
    -------
    tuple[datetime.datetime]
        A tuple of one datetime
    """

    return (datetime.datetime.now(),)


def example_2() -> tuple[datetime.datetime, ...]:
    """Return a singleton tuple of a datetime

    Returns
    -------
    tuple[datetime.datetime, ...]
        A tuple of one datetime
    """

    return (datetime.datetime.now(),)


def example_3() -> tuple[datetime.datetime,]:
    """Return a singleton tuple of a datetime

    Returns
    -------
    tuple[datetime.datetime,]
        A tuple of one datetime
    """

    return (datetime.datetime.now(),)


def example_4() -> tuple[datetime]:
    """Return a singleton tuple of a datetime

    Returns
    -------
    tuple[datetime]
        A tuple of one datetime
    """

    return (datetime.now(),)
