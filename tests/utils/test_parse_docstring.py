import pytest

from pydoclint.utils.parse_docstring import _containsNumpyStylePattern


@pytest.mark.parametrize(
    'docstring, expected',
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
