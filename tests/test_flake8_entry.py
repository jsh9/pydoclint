import ast
import os
import re
import shutil
import subprocess  # noqa: S404
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

import pydoclint
from pydoclint.flake8_entry import Plugin
from tests.helpers import (
    IGNORE_UNDERSCORE_ARGS_DEFAULT_MESSAGE,
    IGNORE_UNDERSCORE_ARGS_NONDEFAULT_MESSAGE,
    SHOULD_DOCUMENT_PRIVATE_CLASS_ATTRIBUTES_DEFAULT_MESSAGE,
    SHOULD_DOCUMENT_PRIVATE_CLASS_ATTRIBUTES_ENABLED_MESSAGE,
    extractListedNames,
)

THIS_DIR = Path(__file__).parent
DATA_DIR = THIS_DIR / 'test_data'
NAME_CATEGORY_OPTIONS_DATA_DIR = DATA_DIR / 'name_category_options'

# Where the test process imports pydoclint from; real Flake8 runs use it too
PYDOCLINT_IMPORT_ROOT = Path(pydoclint.__file__).resolve().parent.parent


class FakeParser:
    """A stand-in Flake8 option parser that records each option's default."""

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


def runRealFlake8(
        directory: Path,
        *,
        sourcePath: Path,
        configLines: list[str],
) -> subprocess.CompletedProcess[str]:
    """Run real Flake8 on a copied fixture with a temporary ``.flake8``."""
    shutil.copyfile(sourcePath, directory / 'sample.py')
    (directory / '.flake8').write_text(
        '[flake8]\nselect = DOC\n' + '\n'.join(configLines) + '\n',
        encoding='utf-8',
    )
    # Flake8 finds pydoclint through the entry point of the current
    # environment. Putting the code under test first on the path keeps an
    # older installed pydoclint from shadowing it.
    env = os.environ.copy()
    env['PYTHONPATH'] = os.pathsep.join([
        str(PYDOCLINT_IMPORT_ROOT),
        *filter(None, [env.get('PYTHONPATH')]),
    ])
    return subprocess.run(
        [sys.executable, '-m', 'flake8', 'sample.py'],
        cwd=directory,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.parametrize(
    ('optionValue', 'expected'),
    [
        ('True', True),
        ('true', True),
        ('TRUE', True),
        ('False', False),
        ('false', False),
        ('FALSE', False),
    ],
)
def testBoolParsesValuesCaseInsensitively(
        optionValue: str,
        expected: bool,
) -> None:
    """Ensure Flake8 boolean option values are parsed regardless of case."""
    assert Plugin._bool('--example-option', optionValue) is expected


@pytest.mark.parametrize('optionValue', ['yes', '1', '', 'Truee'])
def testBoolRejectsNonBooleanValues(optionValue: str) -> None:
    """Ensure non-boolean Flake8 option values still fail clearly."""
    with pytest.raises(ValueError, match=r'^Invalid argument value: ') as exc:
        Plugin._bool('--example-option', optionValue)

    assert str(exc.value) == (
        f'Invalid argument value: --example-option={optionValue}'
    )


@pytest.mark.parametrize(
    ('overrides', 'expectedMessage'),
    [
        pytest.param(
            {'ignore_underscore_args': 'True'},
            IGNORE_UNDERSCORE_ARGS_DEFAULT_MESSAGE,
            id='ignore-underscore-args-default',
        ),
        pytest.param(
            {'ignore_underscore_args': 'False'},
            IGNORE_UNDERSCORE_ARGS_NONDEFAULT_MESSAGE,
            id='ignore-underscore-args-nondefault',
        ),
        pytest.param(
            {'should_document_private_class_attributes': 'False'},
            SHOULD_DOCUMENT_PRIVATE_CLASS_ATTRIBUTES_DEFAULT_MESSAGE,
            id='should-document-private-class-attributes-default',
        ),
        pytest.param(
            {'should_document_private_class_attributes': 'True'},
            SHOULD_DOCUMENT_PRIVATE_CLASS_ATTRIBUTES_ENABLED_MESSAGE,
            id='should-document-private-class-attributes-enabled',
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
    with pytest.raises(ValueError, match=re.escape(expectedMessage)) as exc:
        list(flake8Plugin.run())

    assert str(exc.value) == expectedMessage


@pytest.mark.parametrize(
    (
        'ignorePrivateClassAttributes',
        'ignoreUnderscoreOnlyClassAttributes',
        'ignoreSpecialDunderClassAttributes',
        'expectedMissingNames',
    ),
    [
        ('True', 'True', 'True', []),
        ('True', 'True', 'False', ['__tablename__: str']),
        ('True', 'False', 'True', ['_: bool', '__: float']),
        (
            'True',
            'False',
            'False',
            ['_: bool', '__: float', '__tablename__: str'],
        ),
        ('False', 'True', 'True', ['_private: str']),
        ('False', 'True', 'False', ['_private: str', '__tablename__: str']),
        ('False', 'False', 'True', ['_private: str', '_: bool', '__: float']),
        (
            'False',
            'False',
            'False',
            ['_private: str', '_: bool', '__: float', '__tablename__: str'],
        ),
    ],
)
def testNewClassAttributeOptionsPropagate(
        ignorePrivateClassAttributes: str,
        ignoreUnderscoreOnlyClassAttributes: str,
        ignoreSpecialDunderClassAttributes: str,
        expectedMissingNames: list[str],
) -> None:
    """Ensure Flake8 forwards all three class-attribute name controls."""
    flake8Plugin = buildFlake8Plugin(
        NAME_CATEGORY_OPTIONS_DATA_DIR / 'class_attributes.py',
        style='numpy',
        arg_type_hints_in_docstring='False',
        check_class_attributes='True',
        ignore_private_class_attributes=ignorePrivateClassAttributes,
        ignore_underscore_only_class_attributes=(
            ignoreUnderscoreOnlyClassAttributes
        ),
        ignore_special_dunder_class_attributes=(
            ignoreSpecialDunderClassAttributes
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
    actualMissingNames = extractListedNames(messages[1], ': [')
    assert sorted(actualMissingNames) == sorted(expectedMissingNames)


@pytest.mark.parametrize(
    (
        'ignorePrivateArgs',
        'ignoreUnderscoreOnlyArgs',
        'ignoreSpecialDunderArgs',
        'expectedMissingNames',
    ),
    [
        ('True', 'True', 'True', []),
        ('True', 'True', 'False', ['__special__: float']),
        ('True', 'False', 'True', ['_: bool']),
        ('True', 'False', 'False', ['_: bool', '__special__: float']),
        ('False', 'True', 'True', ['_private: str']),
        ('False', 'True', 'False', ['_private: str', '__special__: float']),
        ('False', 'False', 'True', ['_private: str', '_: bool']),
        (
            'False',
            'False',
            'False',
            ['_private: str', '_: bool', '__special__: float'],
        ),
    ],
)
def testArgumentNameOptionsPropagate(
        ignorePrivateArgs: str,
        ignoreUnderscoreOnlyArgs: str,
        ignoreSpecialDunderArgs: str,
        expectedMissingNames: list[str],
) -> None:
    """Ensure Flake8 forwards all three argument name controls."""
    flake8Plugin = buildFlake8Plugin(
        NAME_CATEGORY_OPTIONS_DATA_DIR / 'argument_categories.py',
        style='google',
        arg_type_hints_in_docstring='False',
        ignore_private_args=ignorePrivateArgs,
        ignore_underscore_only_args=ignoreUnderscoreOnlyArgs,
        ignore_special_dunder_args=ignoreSpecialDunderArgs,
    )
    messages = [message for _, _, message, _ in flake8Plugin.run()]
    if not expectedMissingNames:
        assert messages == []
        return

    assert [message.split()[0] for message in messages] == [
        'DOC101',
        'DOC103',
    ]
    actualMissingNames = extractListedNames(
        messages[1],
        'but not in the docstring: [',
    )
    assert sorted(actualMissingNames) == sorted(expectedMissingNames)


@pytest.mark.parametrize(
    ('fixtureName', 'configLines', 'expectedCodes', 'expectedMissingNames'),
    [
        pytest.param(
            'underscore_only_function_argument.py',
            ['style = google', 'arg-type-hints-in-docstring = false'],
            [],
            [],
            id='ignore-underscore-args-default',
        ),
        pytest.param(
            'underscore_only_function_argument.py',
            [
                'style = google',
                'arg-type-hints-in-docstring = false',
                'ignore-underscore-only-args = false',
            ],
            ['DOC101', 'DOC103'],
            ['_: int'],
            id='ignore-underscore-args-nondefault',
        ),
        pytest.param(
            'class_attributes.py',
            ['style = numpy', 'arg-type-hints-in-docstring = false'],
            [],
            [],
            id='should-document-private-class-attributes-default',
        ),
        pytest.param(
            'class_attributes.py',
            [
                'style = numpy',
                'arg-type-hints-in-docstring = false',
                'ignore-private-class-attributes = false',
                'ignore-underscore-only-class-attributes = false',
                'ignore-special-dunder-class-attributes = false',
            ],
            ['DOC601', 'DOC603'],
            ['_private: str', '_: bool', '__: float', '__tablename__: str'],
            id='should-document-private-class-attributes-enabled',
        ),
    ],
)
def testRealFlake8AppliesLowercaseMigrationReplacements(
        tmp_path: Path,
        fixtureName: str,
        configLines: list[str],
        expectedCodes: list[str],
        expectedMissingNames: list[str],
) -> None:
    """
    Ensure lowercase replacements work in a real ``.flake8`` file.

    Each case applies the replacement recommended for a removed option and
    checks that the result matches the removed option's old behavior.
    """
    result = runRealFlake8(
        tmp_path,
        sourcePath=NAME_CATEGORY_OPTIONS_DATA_DIR / fixtureName,
        configLines=configLines,
    )
    output = result.stdout + result.stderr
    assert 'ValueError' not in output
    assert 'Invalid argument value' not in output

    violationLines = [
        line
        for line in result.stdout.splitlines()
        if line.startswith('sample')
    ]
    assert [line.split()[1] for line in violationLines] == expectedCodes
    assert result.returncode == (1 if expectedCodes else 0), output
    if expectedMissingNames:
        actualMissingNames = extractListedNames(
            violationLines[1],
            'but not in the docstring: [',
        )
        assert sorted(actualMissingNames) == sorted(expectedMissingNames)
