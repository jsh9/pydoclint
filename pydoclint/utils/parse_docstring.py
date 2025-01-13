from __future__ import annotations

from docstring_parser import ParseError

from pydoclint.utils.doc import Doc


def parseDocstring(
        docstring: str,
        userSpecifiedStyle: str,
) -> tuple[Doc, ParseError | None, bool]:
    """
    Parse docstring in all 3 docstring styles and return the one that
    is parsed with the most likely style.
    """
    docNumpy, excNumpy = parseDocstringInGivenStyle(docstring, 'numpy')
    docGoogle, excGoogle = parseDocstringInGivenStyle(docstring, 'google')
    docSphinx, excSphinx = parseDocstringInGivenStyle(docstring, 'sphinx')

    docstrings: dict[str, Doc] = {
        'numpy': docNumpy,
        'google': docGoogle,
        'sphinx': docSphinx,
    }
    docstringSizes: dict[str, int] = {
        'numpy': docNumpy.docstringSize,
        'google': docGoogle.docstringSize,
        'sphinx': docSphinx.docstringSize,
    }
    parsingExceptions: dict[str, ParseError | None] = {
        'numpy': excNumpy,
        'google': excGoogle,
        'sphinx': excSphinx,
    }
    # Whichever style has the largest docstring size, we think that it is
    # the actual style that the docstring is written in.
    maxDocstringSize = max(docstringSizes.values())
    styleMismatch: bool = docstringSizes[userSpecifiedStyle] < maxDocstringSize
    return (
        docstrings[userSpecifiedStyle],
        parsingExceptions[userSpecifiedStyle],
        styleMismatch,
    )


def parseDocstringInGivenStyle(
        docstring: str,
        style: str,
) -> tuple[Doc, ParseError | None]:
    """Parse the docstring and return the content of the doc."""
    exception: ParseError | None = None
    try:
        doc: Doc = Doc(docstring=docstring, style=style)
    except ParseError as exc:
        doc = Doc(docstring='', style=style)
        exception = exc

    return doc, exception
