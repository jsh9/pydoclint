import ast
import re
from textwrap import dedent
from types import SimpleNamespace
from typing import Any

import pytest

from pydoclint.flake8_entry import Plugin


class FakeParser:
    """Collect Flake8 option defaults for plugin tests."""

    def __init__(self) -> None:
        self.defaults: dict[str, Any] = {}

    def add_option(self, *names: str, **kwargs: Any) -> None:
        longName = next(name for name in names if name.startswith('--'))
        destination = longName[2:].replace('-', '_')
        self.defaults[destination] = kwargs.get('default')


def buildPlugin(src: str, **overrides: Any) -> Plugin:
    """Build a plugin instance with real option defaults and overrides."""

    class TestPlugin(Plugin):
        pass

    parser = FakeParser()
    TestPlugin.add_options(parser)
    parser.defaults.update(overrides)
    TestPlugin.parse_options(SimpleNamespace(**parser.defaults))
    return TestPlugin(ast.parse(dedent(src)))


@pytest.mark.parametrize(
    ('overrides', 'expectedMessage'),
    [
        (
            {'ignore_underscore_args': 'True'},
            'The option `--ignore-underscore-args` no longer works; remove it.'
            ' Its replacement, `--ignore-underscore-only-args`, defaults to'
            ' `True` (`ignore-underscore-only-args = true` in TOML/Flake8),'
            ' which preserves this behavior.',
        ),
        (
            {'ignore_underscore_args': 'False'},
            'The option `--ignore-underscore-args` no longer works. Replace it'
            ' with `--ignore-underscore-only-args=False` on the command line or'
            ' `ignore-underscore-only-args = false` in TOML/Flake8 config.',
        ),
        (
            {'should_document_private_class_attributes': 'True'},
            'The option `--should-document-private-class-attributes` no longer'
            ' works. Use `--ignore-private-class-attributes=False` and'
            ' `--ignore-underscore-only-class-attributes=False` on the command'
            ' line, or `ignore-private-class-attributes = false` and'
            ' `ignore-underscore-only-class-attributes = false` in TOML/Flake8'
            ' config. Special dunder class attributes are always excluded.',
        ),
        (
            {'should_document_private_class_attributes': 'False'},
            'The option `--should-document-private-class-attributes` no longer'
            ' works; remove it. Its replacements,'
            ' `--ignore-private-class-attributes` and'
            ' `--ignore-underscore-only-class-attributes`, both default to'
            ' `True` (`ignore-private-class-attributes = true` and'
            ' `ignore-underscore-only-class-attributes = true` in'
            ' TOML/Flake8), which preserves this behavior.',
        ),
    ],
)
def testRemovedOptionsShowMigrationError(
        overrides: dict[str, str],
        expectedMessage: str,
) -> None:
    plugin = buildPlugin('def func(): pass', **overrides)
    with pytest.raises(ValueError, match=re.escape(expectedMessage)):
        list(plugin.run())


@pytest.mark.parametrize(
    (
        'ignorePrivateClassAttributes',
        'ignoreUnderscoreOnlyClassAttributes',
        'expectedMissingNames',
    ),
    [
        ('True', 'True', []),
        ('True', 'False', ['_: bool', '__: float']),
        ('False', 'True', ['_private: str']),
        (
            'False',
            'False',
            ['_private: str', '_: bool', '__: float'],
        ),
    ],
)
def testNewClassAttributeOptionsPropagate(
        ignorePrivateClassAttributes: str,
        ignoreUnderscoreOnlyClassAttributes: str,
        expectedMissingNames: list[str],
) -> None:
    plugin = buildPlugin(
        '''
class Example:
    """
    Class with attributes from every name category.

    Attributes
    ----------
    public
        A public attribute.
    """
    public: int
    _private: str
    _: bool
    __: float
    __slots__: tuple[str, ...]
    __hash__ = None
    __match_args__: tuple[str, ...]
''',
        style='numpy',
        arg_type_hints_in_docstring='False',
        check_class_attributes='True',
        ignore_private_class_attributes=ignorePrivateClassAttributes,
        ignore_underscore_only_class_attributes=(
            ignoreUnderscoreOnlyClassAttributes
        ),
    )
    messages = [message for _, _, message, _ in plugin.run()]
    if not expectedMissingNames:
        assert messages == []
        return

    assert [message.split()[0] for message in messages] == [
        'DOC601',
        'DOC603',
    ]
    actualMissingNames = (
        messages[1]
        .split(': [', maxsplit=1)[1]
        .split('].', maxsplit=1)[0]
        .split(', ')
    )
    assert sorted(actualMissingNames) == sorted(expectedMissingNames)


@pytest.mark.parametrize(
    ('ignoreUnderscoreOnlyArgs', 'expectedCodes'),
    [
        ('True', []),
        ('False', ['DOC101', 'DOC103']),
    ],
)
def testIgnoreUnderscoreOnlyArgsPropagates(
        ignoreUnderscoreOnlyArgs: str,
        expectedCodes: list[str],
) -> None:
    plugin = buildPlugin(
        '''
def func(_: int, value: int) -> None:
    """Do something.

    Args:
        value (int): Value to process.
    """
''',
        style='google',
        ignore_underscore_only_args=ignoreUnderscoreOnlyArgs,
    )
    codes = [message.split()[0] for _, _, message, _ in plugin.run()]
    assert codes == expectedCodes
