import pytest
from docstring_parser import ParseError

from pydoclint.utils.parse_docstring import (
    _NUMPY_SECTION_HEADER_PATTERN,
    _containsNumpyStylePattern,
    _validateNumpySectionHeaders,
)


@pytest.mark.parametrize(
    ('docstring', 'expected'),
    [
        # Test cases that should detect numpy style patterns
        (
            """
            This is a function.

            Returns
            -------
            str
                The return value
            """,
            True,
        ),
        (
            """
            This is a function.

            Args:
            -----
            arg1 : str
                The input argument
            """,
            True,
        ),
        (
            """
            This is a function.

            Parameters
            ----------
            arg1 : str
                The input argument
            """,
            True,
        ),
        (
            """
            This is a function.

            Examples
            --------
            >>> func("test")
            "test"
            """,
            True,
        ),
        (
            """
            This is a function.

            Raises
            ------
            ValueError
                If input is invalid
            """,
            True,
        ),
        (
            """
            This is a function.

            Notes
            -----
            This is a note.
            """,
            True,
        ),
        (
            """
            This is a function.

            See Also
            --------
            other_function : Related function
            """,
            True,
        ),
        (
            """
            This is a function.

            returns
            -------
            str
                The return value
            """,
            True,
        ),
        (
            """
            This is a function.

                Returns
                -------
            str
                The return value
            """,
            True,
        ),
        (
            """
            This is a function.

            Parameters
            ----------
            arg1 : str
                The input argument

            Returns
            -------
            str
                The return value
            """,
            True,
        ),
        (
            """
            This is a function.

            Args:
                arg1 (str): Google style arg

            Returns
            -------
            str
                Numpy style return
            """,
            True,
        ),
        # Test cases that should NOT detect numpy style patterns
        (
            """
            This is a function.

            Args:
                arg1 (str): The input argument

            Returns:
                str: The return value
            """,
            False,
        ),
        (
            """
            This is a function.

            Returns
            --
            str
                The return value
            """,
            False,
        ),
        (
            """
            This is a function.

            Returns
            str
                The return value
            """,
            False,
        ),
        ('', False),
    ],
)
def testContainsNumpyStylePattern(docstring: str, expected: bool) -> None:
    """Test detection of numpy-style docstring patterns."""
    assert _containsNumpyStylePattern(docstring) is expected


def testNumpySectionHeaderPattern() -> None:
    """Test numpy section-header regex captures arbitrary section titles."""
    docstring = """
    This is a function.

    Parameters
    ----------
    x
        input content

      Side Effects
      ------------
    side effect content

    ⛲️🚖🏟🏕🏝🚲
    ----------
    emoji content

    Not A Section
    --
    short underline content

    Args:
    -----
    colon-suffixed Google-style heading; should be ignored
    """

    sectionNames = [
        match.group(1)
        for match in _NUMPY_SECTION_HEADER_PATTERN.finditer(docstring)
    ]

    assert sectionNames == [
        'Parameters',
        'Side Effects',
        '⛲️🚖🏟🏕🏝🚲',
    ]


@pytest.mark.parametrize(
    'sectionName',
    [
        'Parameters',
        'Other Parameters',
        'Raises',
        'Attributes',
        'Returns',
        'Yields',
        'Examples',
        'Warnings',
        'See Also',
        'deprecated',  # This is lowercase in DEFAULT_SECTIONS.
    ],
)
def testValidateNumpySectionHeaders_allowsDefaultSections(
        sectionName: str,
) -> None:
    """Test numpy section validation allows parser-supported sections."""
    docstring = f"""
    This is a function.

    {sectionName}
    {'-' * max(3, len(sectionName))}
    section content
    """

    _validateNumpySectionHeaders(docstring)


@pytest.mark.parametrize('sectionName', ['Inputs', 'Outputs', 'Properties'])
def testValidateNumpySectionHeaders_rejectsUnsupportedSections(
        sectionName: str,
) -> None:
    """Test numpy section validation rejects unsupported custom sections."""
    docstring = f"""
    This is a function.

    {sectionName}
    {'-' * max(3, len(sectionName))}
    section content
    """

    with pytest.raises(
        ParseError,
        match=f'Unsupported numpy docstring section: "{sectionName}"',
    ):
        _validateNumpySectionHeaders(docstring)


def testValidateNumpySectionHeaders_rejectsAllUnsupportedSections() -> None:
    """Test numpy section validation reports all custom sections."""
    docstring = """
    This is a function.

    Inputs
    ------
    input content

    Outputs
    -------
    output content

    Properties
    ----------
    property content

    🍔🥟🍕🌮🥦🍎🍊🌽🥭
    ---------------
    transformation content

    Side Effects
    ------------
    side effect content
    """
    errMsg = (
        'Unsupported numpy docstring sections: "Inputs", "Outputs", '
        '"Properties", "🍔🥟🍕🌮🥦🍎🍊🌽🥭", "Side Effects"'
    )
    with pytest.raises(ParseError, match=errMsg):
        _validateNumpySectionHeaders(docstring)


def testValidateNumpySectionHeaders_rejectsUnsupportedSectionAfterAllowed() -> (
    None
):
    """
    Test numpy section validation rejects custom sections after valid ones.
    """
    docstring = """
    This is a function.

    Parameters
    ----------
    x
        input content

    Outputs
    -------
    output content

    Properties
    ----------
    property content
    """
    errMsg = 'Unsupported numpy docstring sections: "Outputs", "Properties"'
    with pytest.raises(ParseError, match=errMsg):
        _validateNumpySectionHeaders(docstring)


def testValidateNumpySectionHeaders_ignoresNonSectionUnderlines() -> None:
    """Test numpy section validation ignores text that is not a section."""
    docstring = """
    This is a function.

    Inputs
    --
    not a numpy section because the underline is too short
    """

    _validateNumpySectionHeaders(docstring)
