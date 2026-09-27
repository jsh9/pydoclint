import ast
import re
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from pydoclint.flake8_entry import Plugin

THIS_DIR = Path(__file__).parent
DATA_DIR = THIS_DIR / 'test_data'


class FakeParser:
    """Collect option defaults for pydoclint's Flake8 entry-point tests."""

    def __init__(self) -> None:
        self.defaults: dict[str, Any] = {}

    def add_option(self, *names: str, **kwargs: Any) -> None:
        longName = next(name for name in names if name.startswith('--'))
        destination = longName[2:].replace('-', '_')
        self.defaults[destination] = kwargs.get('default')


def buildFlake8Plugin(sourcePath: Path, **overrides: Any) -> Plugin:
    """Build a Flake8 plugin with real option defaults and overrides."""

    class IsolatedFlake8Plugin(Plugin):
        pass

    parser = FakeParser()
    IsolatedFlake8Plugin.add_options(parser)
    parser.defaults.update(overrides)
    IsolatedFlake8Plugin.parse_options(SimpleNamespace(**parser.defaults))
    sourceCode = sourcePath.read_text(encoding='utf-8')
    return IsolatedFlake8Plugin(ast.parse(sourceCode))


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
    """Ensure Flake8 rejects removed options with migration guidance."""
    flake8Plugin = buildFlake8Plugin(
        DATA_DIR / 'common/minimal.py',
        **overrides,
    )
    with pytest.raises(ValueError, match=re.escape(expectedMessage)):
        list(flake8Plugin.run())


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
    """Ensure Flake8 forwards both class-attribute name controls."""
    flake8Plugin = buildFlake8Plugin(
        DATA_DIR / 'private_and_underscore_only_options/class_attributes.py',
        style='numpy',
        arg_type_hints_in_docstring='False',
        check_class_attributes='True',
        ignore_private_class_attributes=ignorePrivateClassAttributes,
        ignore_underscore_only_class_attributes=(
            ignoreUnderscoreOnlyClassAttributes
        ),
    )
    messages = [message for _, _, message, _ in flake8Plugin.run()]
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
    """Ensure Flake8 forwards the underscore-only argument control."""
    flake8Plugin = buildFlake8Plugin(
        DATA_DIR
        / 'private_and_underscore_only_options'
        / 'underscore_only_function_argument.py',
        style='google',
        arg_type_hints_in_docstring='False',
        ignore_underscore_only_args=ignoreUnderscoreOnlyArgs,
    )
    codes = [message.split()[0] for _, _, message, _ in flake8Plugin.run()]
    assert codes == expectedCodes
