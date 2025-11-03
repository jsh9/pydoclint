from __future__ import annotations

import re

from docstring_parser import ParseError

from pydoclint.utils.doc import Doc

_SPHINX_KEYWORDS = (
    ':param ',
    ':type ',
    ':raises ',
    ':return:',
    ':rtype:',
    ':yield:',
    ':ytype:',
)

_GOOGLE_KEYWORDS = (
    'Args:',
    'Returns:',
    'Yields:',
    'Raises:',
    'Examples:',
    'Notes:',
)


def _containsNumpyStylePattern(docstring: str) -> bool:
    # Check if docstring contains numpy-style section headers with dashes.
    #
    # Looks for patterns like:
    # Returns
    # -------
    #
    # Args:
    # -----
    #
    # Examples
    # --------

    # Pattern to match section headers followed by dashes on the next line
    # Matches common numpy docstring sections followed by 3+ dashes
    sections = (
        r'Args?|Arguments?|Parameters?|Param|Returns?|Return|Yields?|Yield|'
        r'Raises?|Raise|Examples?|Example|Notes?|Note|See Also|References?|'
        r'Reference'
    )
    pattern = rf'^\s*({sections})\s*:?\s*\n\s*-{{3,}}\s*$'
    return bool(re.search(pattern, docstring, re.MULTILINE | re.IGNORECASE))


def _containsSphinxStylePattern(docstring: str) -> bool:
    """
    Check if docstring contains Sphinx-style field lists at base indentation.

    Only lines that have the same leading indentation as the docstring
    definition (i.e., the opening triple quotes) count as valid Sphinx
    directives. Lines with more or fewer leading spaces are ignored.
    """
    leadingIndent = _detectDocstringIndent(docstring)
    for line in docstring.splitlines():
        stripped = line.lstrip()
        if stripped == '':
            continue

        currentIndent = len(line) - len(stripped)
        if currentIndent != leadingIndent:
            continue

        for keyword in _SPHINX_KEYWORDS:
            if stripped.startswith(keyword):
                return True

    return False


def _containsGoogleStylePattern(docstring: str) -> bool:
    """
    Check if docstring contains Google-style section headers at base indent.
    """
    leadingIndent = _detectDocstringIndent(docstring)
    for line in docstring.splitlines():
        stripped = line.lstrip()
        if stripped == '':
            continue

        currentIndent = len(line) - len(stripped)
        if currentIndent != leadingIndent:
            continue

        for keyword in _GOOGLE_KEYWORDS:
            if stripped.startswith(keyword):
                return True

    return False


def _detectDocstringIndent(docstring: str) -> int:
    """
    Detect the leading indentation level of a docstring.

    This approximates the column where the opening triple quotes are placed by
    measuring the smallest indentation across non-empty lines.
    """
    indent: int | None = None
    for line in docstring.splitlines():
        stripped = line.lstrip()
        if stripped == '':
            continue

        currentIndent = len(line) - len(stripped)
        if indent is None or currentIndent < indent:
            indent = currentIndent

    return 0 if indent is None else indent


def parseDocstring(
        docstring: str,
        userSpecifiedStyle: str,
) -> tuple[Doc, ParseError | None, bool]:
    """
    Parse docstring in all 3 docstring styles and return the one that is parsed
    with the most likely style.
    """
    isLikelyNumpy: bool = _containsNumpyStylePattern(docstring)
    isLikelyGoogle: bool = _containsGoogleStylePattern(docstring)
    isLikelySphinx: bool = _containsSphinxStylePattern(docstring)

    if isLikelyNumpy:
        # Numpy-style headers with dashes are strong indicators; ignore other
        # potential matches when they appear alongside them.
        isLikelyGoogle = False
        isLikelySphinx = False

    likelyStyles = {
        'numpy': isLikelyNumpy,
        'google': isLikelyGoogle,
        'sphinx': isLikelySphinx,
    }
    matchedStyles = [
        style for style, matched in likelyStyles.items() if matched
    ]

    styleMismatch: bool

    if len(matchedStyles) == 1:
        detectedStyle = matchedStyles[0]
        if detectedStyle == userSpecifiedStyle:
            doc, exc = parseDocstringInGivenStyle(docstring, detectedStyle)
            # The Google parser raises hard errors when sections are malformed,
            # which is a strong signal the docstring is effectively written in
            # a different style. Numpy/Sphinx parsers are more permissive, so
            # we surface only the parsing error (DOC001) without flagging a
            # style mismatch in those cases.
            styleMismatch = exc is not None and detectedStyle == 'google'
            return doc, exc, styleMismatch

        doc, exc = parseDocstringInGivenStyle(docstring, detectedStyle)
        styleMismatch = True
        return doc, exc, styleMismatch

    if len(matchedStyles) == 0:
        doc, exc = parseDocstringInGivenStyle(docstring, userSpecifiedStyle)
        styleMismatch = False
        return doc, exc, styleMismatch

    doc, exc = parseDocstringInGivenStyle(docstring, userSpecifiedStyle)
    styleMismatch = True
    return doc, exc, styleMismatch


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
