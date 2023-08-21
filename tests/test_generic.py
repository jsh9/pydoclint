import pytest

from pydoclint.utils.generic import stripQuotes


@pytest.mark.parametrize(
    'inputStr, expected',
    [
        (None, None),
        ('something', 'something'),
        ('something else', 'something else'),
        ('"good morning"', 'good morning'),
        ('"yes\' good', 'yes good'),
        ('"""""""""', ''),
        ("''''''''''''''''", ''),
        ('""" """  """', '   '),
        ('List["Something", \'Else\']', 'List[Something, Else]'),
        ('`something`', 'something'),
        ('``something``', 'something'),
        ('`List["Something", \'Else\']`', 'List[Something, Else]'),
        ('``List["Something", \'Else\']``', 'List[Something, Else]'),
        ('`""" """  """`', '   '),
        ('``""" """  """``', '   '),
    ],
)
def testStripQuotes(inputStr: str, expected: str) -> None:
    output = stripQuotes(inputStr)
    assert output == expected
