from typing import Any, List, Set

import pytest

from pydoclint.utils.arg import Arg, ArgList


def testArg_initializationCheck():
    with pytest.raises(ValueError, match='`name` cannot be an empty string'):
        Arg(name='', typeHint='int')


@pytest.mark.parametrize(
    'arg, string_repr',
    [
        (Arg(name='1', typeHint='2'), '1: 2'),
        (Arg(name='arg1', typeHint='str'), 'arg1: str'),
        (Arg(name='obj', typeHint='int | float'), 'obj: int | float'),
        (Arg(name='arg1\\_\\_', typeHint='Any'), 'arg1__: Any'),  # noqa: W605
        (Arg(name='**kwargs', typeHint='Any'), '**kwargs: Any'),
        (Arg(name='\\**kwargs', typeHint='Any'), '**kwargs: Any'),
    ],
)
def testArg_str(arg: Arg, string_repr: str) -> None:
    assert str(arg) == string_repr


@pytest.mark.parametrize(
    'arg1, arg2',
    [
        (Arg(name='1', typeHint='2'), Arg(name='1', typeHint='2')),
        (Arg(name='abc', typeHint='12345'), Arg(name='abc', typeHint='12345')),
        (Arg(name='aa', typeHint=''), Arg(name='aa', typeHint='')),
        (Arg(name='\\**kw', typeHint=''), Arg(name='**kw', typeHint='')),
        (Arg(name='**kw', typeHint=''), Arg(name='\\**kw', typeHint='')),
        (Arg(name='\\*args', typeHint=''), Arg(name='*args', typeHint='')),
        (Arg(name='*args', typeHint=''), Arg(name='\\*args', typeHint='')),
    ],
)
def testArg_equal(arg1: Arg, arg2: Arg) -> None:
    assert arg1 == arg2
    assert arg1 in {arg1}
    assert arg1 in {arg2}
    assert arg2 in {arg1}
    assert arg2 in {arg2}


@pytest.mark.parametrize(
    'obj1, obj2',
    [
        (Arg(name='1', typeHint='3'), 2),
        (Arg(name='1', typeHint='3'), 'thing'),
        (Arg(name='1', typeHint='2'), Arg(name='1', typeHint='3')),
        (Arg(name='1', typeHint='2'), Arg(name='2', typeHint='2')),
    ],
)
def testArg_notEqual(obj1: Any, obj2: Any) -> None:
    assert obj1 != obj2
    assert obj1 not in {obj2}
    assert obj2 not in {obj1}


@pytest.mark.parametrize(
    'arg1, arg2',
    [
        (Arg(name='abc', typeHint=''), Arg(name='abcd', typeHint='')),
        (Arg(name='abc', typeHint='12345'), Arg(name='abcd', typeHint='')),
        (Arg(name='abc', typeHint='123'), Arg(name='abc', typeHint='1234')),
    ],
)
def testArg_lessThan(arg1: Arg, arg2: Arg) -> None:
    assert arg1 < arg2


@pytest.mark.parametrize(
    'arg1, arg2',
    [
        (Arg(name='abc', typeHint=''), Arg(name='abcd', typeHint='')),
        (Arg(name='abc', typeHint='12345'), Arg(name='abcd', typeHint='')),
        (Arg(name='abc', typeHint='123'), Arg(name='abc', typeHint='1234')),
        (Arg(name='abc', typeHint='123'), Arg(name='abc', typeHint='123')),
        (Arg(name='abc', typeHint=''), Arg(name='abc', typeHint='')),
    ],
)
def testArg_lessThanOrEqualTo(arg1: Arg, arg2: Arg) -> None:
    assert arg1 <= arg2


@pytest.mark.parametrize(
    'arg1, arg2',
    [
        (Arg(name='abc', typeHint=''), Arg(name='abcd', typeHint='')),
        (Arg(name='abc', typeHint='12345'), Arg(name='abcd', typeHint='')),
        (Arg(name='abc', typeHint='123'), Arg(name='abc', typeHint='1234')),
    ],
)
def testArg_greaterThan(arg1: Arg, arg2: Arg) -> None:
    assert arg2 > arg1


@pytest.mark.parametrize(
    'arg1, arg2',
    [
        (Arg(name='abc', typeHint=''), Arg(name='abcd', typeHint='')),
        (Arg(name='abc', typeHint='12345'), Arg(name='abcd', typeHint='')),
        (Arg(name='abc', typeHint='123'), Arg(name='abc', typeHint='1234')),
        (Arg(name='abc', typeHint='123'), Arg(name='abc', typeHint='123')),
        (Arg(name='abc', typeHint=''), Arg(name='abc', typeHint='')),
    ],
)
def testArg_greaterThanOrEqualTo(arg1: Arg, arg2: Arg) -> None:
    assert arg2 >= arg1


@pytest.mark.parametrize(
    'original, after',
    [
        (
            {Arg('xyz', 'a'), Arg('opq', 'b'), Arg('abc', 'c')},
            [Arg('abc', 'c'), Arg('opq', 'b'), Arg('xyz', 'a')],
        ),
        (
            {Arg('xyz', 'a'), Arg('xyz', 'b'), Arg('abc', 'c')},
            [Arg('abc', 'c'), Arg('xyz', 'a'), Arg('xyz', 'b')],
        ),
        (
            {Arg('xyz', 'a'), Arg('xyz', ''), Arg('abc', 'c')},
            [Arg('abc', 'c'), Arg('xyz', ''), Arg('xyz', 'a')],
        ),
    ],
)
def testArg_sorting(original: Set[Arg], after: List[Arg]) -> None:
    assert sorted(original) == after


@pytest.mark.parametrize(
    'str1, str2, expected',
    [
        ('int', 'int', True),
        ('int', 'float', False),
        ('List[int]', 'list[int]', False),
        ('Tuple[int, ...]', 'Tuple[int,...]', True),
        ('Optional[int]', 'int | None', False),
        ('Literal["abc", "def"]', "Literal[\n  'abc',\n  'def',\n]", True),
    ],
)
def testArg_typeHintsEq(str1: str, str2: str, expected: bool) -> None:
    assert Arg._typeHintsEq(str1, str2) == expected


@pytest.mark.parametrize(
    'input_, expected',
    [
        (ArgList([]), '[]'),
        (
            ArgList([Arg('1', '2'), Arg('2', '3')]),
            '[1: 2, 2: 3]',
        ),
        (
            ArgList(
                [
                    Arg('1', '2'),
                    Arg('2', '3'),
                    Arg('3', '456789'),
                ]
            ),
            '[1: 2, 2: 3, 3: 456789]',
        ),
        (
            ArgList(
                [
                    Arg('var1', 'str'),
                    Arg(
                        'myValue', 'Union[int, str, Optional[Dict[str, str]]]'
                    ),
                ]
            ),
            '[var1: str, myValue: Union[int, str, Optional[Dict[str, str]]]]',
        ),
    ],
)
def testArgList_str(input_: ArgList, expected: str) -> None:
    assert str(input_) == expected


@pytest.mark.parametrize(
    'input_, expected',
    [
        (ArgList([]), 0),
        (ArgList([Arg('1', '2'), Arg('2', '3')]), 2),
    ],
)
def testArgList_length(input_: ArgList, expected: int) -> None:
    assert input_.length == expected


@pytest.mark.parametrize(
    'list1, list2',
    [
        (ArgList([]), ArgList([])),
        (
            ArgList([Arg('1', '2'), Arg('2', '3')]),
            ArgList([Arg('1', '2'), Arg('2', '3')]),
        ),
        (
            ArgList([Arg('1', '2'), Arg('2', '3'), Arg('3', '4')]),
            ArgList([Arg('1', '2'), Arg('2', '3'), Arg('3', '4')]),
        ),
        (
            ArgList([Arg('*args', '1'), Arg('\\**kwargs', '2')]),
            ArgList([Arg('\\*args', '1'), Arg('**kwargs', '2')]),
        ),
        (
            ArgList([Arg('arg1\\_', '1'), Arg('arg2__', '2')]),  # noqa: W605
            ArgList([Arg('arg1_', '1'), Arg('arg2\\_\\_', '2')]),  # noqa: W605
        ),
    ],
)
def testArgList_equality(list1: ArgList, list2: ArgList) -> None:
    assert list1 == list2


@pytest.mark.parametrize(
    'list1, list2',
    [
        (
            ArgList([]),
            ArgList([Arg('1', '2'), Arg('2', '3')]),
        ),
        (
            ArgList([Arg('1', '2')]),
            ArgList([Arg('1', '2'), Arg('2', '3')]),
        ),
        (
            ArgList([Arg('1', '2'), Arg('2', 'a')]),
            ArgList([Arg('1', '2'), Arg('2', '3')]),
        ),
        (
            ArgList([Arg('1', '2'), Arg('2', '3'), Arg('a', '4')]),
            ArgList([Arg('1', '2'), Arg('2', '3'), Arg('3', '4')]),
        ),
    ],
)
def testArgList_inequality(list1: ArgList, list2: ArgList) -> None:
    assert list1 != list2


@pytest.mark.parametrize(
    'argInfo, argInfoList, expected',
    [
        (
            Arg('a', 'b'),
            ArgList([Arg('a', 'b'), Arg('1', '2')]),
            True,
        ),
        (
            Arg('a', 'b'),
            ArgList([]),
            False,
        ),
        (
            Arg('a', 'b'),
            ArgList([Arg('a', 'c'), Arg('1', '2')]),
            True,
        ),
    ],
)
def testArgList_contains(
        argInfo: Arg,
        argInfoList: ArgList,
        expected: bool,
) -> None:
    if expected:
        assert argInfoList.contains(argInfo)
    else:
        assert not argInfoList.contains(argInfo)


@pytest.mark.parametrize(
    'obj1, obj2, expected',
    [
        (
            ArgList(
                [Arg('a', '1'), Arg('b', '2'), Arg('c', '3'), Arg('d', '4')]
            ),
            ArgList(
                [Arg('a', '1'), Arg('b', '2'), Arg('c', '3'), Arg('d', '4')]
            ),
            set(),
        ),
        (
            ArgList([Arg('a', '1'), Arg('b', '2'), Arg('c', '3')]),
            ArgList(
                [Arg('a', '1'), Arg('b', '2'), Arg('c', '3'), Arg('d', '4')]
            ),
            set(),
        ),
        (
            ArgList(
                [Arg('a', '1'), Arg('b', '2'), Arg('c', '3'), Arg('d', '4')]
            ),
            ArgList([Arg('c', '3'), Arg('d', '4'), Arg('e', '5')]),
            {Arg('a', '1'), Arg('b', '2')},
        ),
        (
            ArgList(
                [Arg('a', '1'), Arg('b', '2'), Arg('c', '3'), Arg('d', '4')]
            ),
            ArgList([Arg('e', '5'), Arg('f', '6'), Arg('g', '7')]),
            {Arg('a', '1'), Arg('b', '2'), Arg('c', '3'), Arg('d', '4')},
        ),
        (
            ArgList([]),
            ArgList([Arg('e', '5'), Arg('f', '6'), Arg('g', '7')]),
            set(),
        ),
        (
            ArgList([Arg('a', '1'), Arg('b', '2'), Arg('c', '3')]),
            ArgList([]),
            {Arg('a', '1'), Arg('b', '2'), Arg('c', '3')},
        ),
        (
            ArgList([Arg('*args', '1'), Arg('\\**kwargs', '2')]),
            ArgList([Arg('\\*args', '1')]),
            {Arg('**kwargs', '2')},
        ),
        (
            ArgList([Arg('arg1\\_', '1'), Arg('arg2__', '2')]),  # noqa: W605
            ArgList([Arg('arg2\\_\\_', '2')]),  # noqa: W605
            {Arg('arg1_', '1')},
        ),
    ],
)
def testArgList_subtract(
        obj1: ArgList,
        obj2: ArgList,
        expected: Set[Arg],
) -> None:
    assert obj1.subtract(obj2) == expected
