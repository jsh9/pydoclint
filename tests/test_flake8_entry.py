import ast
import re
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
    parser = FakeParser()
    Plugin.add_options(parser)
    parser.defaults.update(overrides)
    Plugin.parse_options(SimpleNamespace(**parser.defaults))
    return Plugin(ast.parse(src))


@pytest.mark.parametrize(
    ('overrides', 'expectedMessage'),
    [
        (
            {'ignore_underscore_args': 'True'},
            'The option `--ignore-underscore-args` no longer works; please use '
            '`--ignore-underscore-only-args=True` instead',
        ),
        (
            {'ignore_underscore_args': 'False'},
            'The option `--ignore-underscore-args` no longer works; please use '
            '`--ignore-underscore-only-args=False` instead',
        ),
        (
            {'should_document_private_class_attributes': 'True'},
            'The option `--should-document-private-class-attributes` no longer '
            'works. To preserve its previous behavior, please use both '
            '`--ignore-private-class-attributes=False` and '
            '`--ignore-underscore-only-class-attributes=False` instead',
        ),
        (
            {'should_document_private_class_attributes': 'False'},
            'The option `--should-document-private-class-attributes` no longer '
            'works. To preserve its previous behavior, please use both '
            '`--ignore-private-class-attributes=True` and '
            '`--ignore-underscore-only-class-attributes=True` instead',
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


def testNewClassAttributeOptionsPropagate() -> None:
    plugin = buildPlugin(
        '''
import dataclasses

@dataclasses.dataclass
class Result:
    """
    Class for storing stuff.

    Attributes
    ----------
    foo
        The foo.
    bar
        The bar.
    """
    _: dataclasses.KW_ONLY
    foo: int
    bar: int
''',
        style='numpy',
        arg_type_hints_in_docstring='False',
        check_class_attributes='True',
        ignore_private_class_attributes='False',
        ignore_underscore_only_class_attributes='True',
    )
    assert list(plugin.run()) == []


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
