import pytest

from pydoclint.utils.generic import (
    doList1ItemsStartWithList2Items,
    stripQuotes,
)


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


@pytest.mark.parametrize(
    'list1, list2, expected',
    [
        ([], [], True),
        (
            ['abc', 'def', 'ghi'],
            ['abc', 'def', 'ghi'],
            True,
        ),
        (
            ['abc', 'def', 'ghi'],
            ['abc', 'def', 'ghi', 'jkl'],
            False,
        ),
        (
            ['abc123', 'def456', 'ghi789'],
            ['abc', 'def', 'ghi'],
            True,
        ),
        (
            ['abc', 'def', 'ghi'],
            ['abc123', 'def456', 'ghi789'],
            False,
        ),
    ],
)
def testDoList1ItemsStartWithList2Items(
        list1: list[str],
        list2: list[str],
        expected: bool,
) -> None:
    output = doList1ItemsStartWithList2Items(list1, list2)
    assert output == expected
