# fmt: off

# The edge cases comes from:
# https://github.com/jsh9/pydoclint/issues/105
# https://github.com/jsh9/pydoclint/issues/231

from __future__ import annotations

from typing import Literal


def func_1(arg1: Literal["foo"]) -> Literal["foo"]:
    """
    Test literal.

    Args:
        arg1 (Literal["foo"]): Arg 1

    Returns:
        Literal["foo"]: The literal string "foo".
    """
    return "foo"


def func_2(arg1: Literal['foo']) -> Literal['foo']:
    """
    Test literal.

    Args:
        arg1 (Literal['foo']): Arg 1

    Returns:
        Literal['foo']: The literal string "foo".
    """
    return "foo"


def func_3(arg1: Literal['foo']) -> tuple[Literal['foo'], Literal["bar"]]:
    """
    Test literal.

    Args:
        arg1 (Literal['foo']): Arg 1

    Returns:
        tuple[Literal['foo'], Literal["bar"]]: The literal strings 'foo' & "bar"
    """
    return 'foo', "bar"


async def upload_tickets(
    file: Annotated[UploadFile, File(description="Excel file with tickets")],
) -> dict:
    """
    Upload and process tickets from an Excel file.

    Args:
        file (Annotated[UploadFile, File(description="Excel file with tickets")]): The file

    Returns:
        dict: Processed ticket data.
    """
    pass
