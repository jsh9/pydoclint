import shutil
from pathlib import Path
from typing import Any

import pytest
from click.testing import CliRunner, Result

from pydoclint.main import main as cli_main
from pydoclint.parse_config import (
    MissingPydoclintSectionError,
    findCommonParentFolder,
    parseOneTomlFile,
)
from tests.helpers import (
    IGNORE_UNDERSCORE_ARGS_DEFAULT_MESSAGE,
    IGNORE_UNDERSCORE_ARGS_NONDEFAULT_MESSAGE,
    SHOULD_DOCUMENT_PRIVATE_CLASS_ATTRIBUTES_DEFAULT_MESSAGE,
    SHOULD_DOCUMENT_PRIVATE_CLASS_ATTRIBUTES_ENABLED_MESSAGE,
    extractListedNames,
)

THIS_DIR = Path(__file__).parent
DATA_DIR = THIS_DIR / 'test_data'
CONFIG_DATA_DIR: Path = DATA_DIR / 'config_files'
minimalFixture = DATA_DIR / 'common/minimal.py'
classAttributeNameKindsFixture = (
    DATA_DIR / 'name_category_options/class_attributes.py'
)
documentedClassAttributesFixture = (
    DATA_DIR / 'name_category_options' / 'documented_class_attributes.py'
)
underscoreArgumentFixture = (
    DATA_DIR / 'name_category_options' / 'underscore_only_function_argument.py'
)
argumentNameKindsFixture = (
    DATA_DIR / 'name_category_options' / 'argument_categories.py'
)


@pytest.mark.parametrize(
    ('paths', 'expected'),
    [
        (['/a/b/c', '/a/b/d', '/a/b/e/f/g'], '/a/b'),
        (['a/b/c', 'a/b/d', 'a/b/e/f/g'], 'a/b'),
        (['/a/b/c', '/a/b/d', '/a/b/e/f/g/file.txt'], '/a/b'),
        (['/a/b/c', '/e/f/g', '/a/b/e/f/g'], '/'),
        (['~/a/b/c', '~/e/f/g', '~/a/b/e/f/g'], '~'),
        (['a/b/c', 'e/f/g', 'a/b/e/f/g'], '.'),
        (['a/b', 'a/b/d', 'a/b/e/f/g'], 'a/b'),
        (['./a/b/c', './a/b/d', './a/b/e/f/g'], 'a/b'),
        (['./a/b/c', './e/f/g', './a/b/e/f/g'], '.'),
    ],
)
def testFindCommonParentFolder(paths: list[str], expected: str) -> None:
    result = findCommonParentFolder(paths, makeAbsolute=False).as_posix()
    assert result == expected


@pytest.mark.parametrize(
    ('filename', 'enforce', 'expected'),
    [
        (Path('a_path_that_doesnt_exist.toml'), False, {}),
        (
            CONFIG_DATA_DIR / 'example_config.toml',
            False,
            {'style': 'google', 'check_arg_order': False},
        ),
    ],
)
def testParseOneTomlFile(
        filename: Path,
        enforce: bool,
        expected: dict[str, Any],
) -> None:
    tomlConfig = parseOneTomlFile(filename, enforcePydoclintSection=enforce)
    assert tomlConfig == expected


@pytest.mark.parametrize(
    ('filename', 'expectedException'),
    [
        (Path('a_path_that_doesnt_exist.toml'), FileNotFoundError),
        (
            CONFIG_DATA_DIR / 'no_pydoclint_section.toml',
            MissingPydoclintSectionError,
        ),
    ],
)
def testParseOneTomlFileEnforceErrors(
        filename: Path,
        expectedException: type[Exception],
) -> None:
    with pytest.raises(expectedException):
        parseOneTomlFile(filename, enforcePydoclintSection=True)


def _copyPythonFixture(directory: Path, fixturePath: Path) -> Path:
    """Copy a Python source fixture into ``directory``."""
    samplePath = directory / 'sample.py'
    shutil.copyfile(fixturePath, samplePath)
    return samplePath


def _getConfigArguments(
        *,
        source: str,
        samplePath: Path,
        cliOptions: list[str],
        tomlOptions: list[str],
) -> list[str]:
    """Build CLI arguments and any requested TOML configuration file."""
    if source == 'cli':
        return [*cliOptions, str(samplePath)]

    configPath = Path(
        'pyproject.toml' if source == 'inferred_toml' else 'custom.toml'
    )
    configPath.write_text(
        '[tool.pydoclint]\n' + '\n'.join(tomlOptions) + '\n',
        encoding='utf-8',
    )
    if source == 'explicit_toml':
        return ['--config', str(configPath), str(samplePath)]

    return [str(samplePath)]


def testCliDefaultConfigMissingFileIsAllowed() -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        samplePath = _copyPythonFixture(Path(), minimalFixture)
        result = runner.invoke(cli_main, [str(samplePath)])
        assert result.exit_code == 0
        assert 'No violations' in result.output


def testCliConfigMissingFileRaisesError() -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        samplePath = _copyPythonFixture(Path(), minimalFixture)
        result = runner.invoke(
            cli_main,
            ['--config', 'custom.toml', str(samplePath)],
        )
        assert result.exit_code == 2
        assert 'Config file "custom.toml" does not exist.' in result.output


def testCliConfigMissingSectionRaisesError() -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        samplePath = _copyPythonFixture(Path(), minimalFixture)
        badConfig = Path('bad.toml')
        badConfig.write_text('[tool.other]\nflag = true\n', encoding='utf-8')
        result = runner.invoke(
            cli_main,
            ['--config', str(badConfig), str(samplePath)],
        )
        assert result.exit_code == 2
        assert (
            'Config file "bad.toml" does not have a [tool.pydoclint] section.'
            in result.output
        )


def _invokeNativeCli(
        *,
        source: str,
        fixturePath: Path,
        cliOptions: list[str],
        tomlOptions: list[str],
) -> Result:
    """Lint a copied fixture in the current directory through the CLI."""
    samplePath = _copyPythonFixture(Path(), fixturePath)
    arguments = _getConfigArguments(
        source=source,
        samplePath=samplePath,
        cliOptions=cliOptions,
        tomlOptions=tomlOptions,
    )
    return CliRunner().invoke(cli_main, arguments)


@pytest.mark.parametrize(
    'source',
    ['cli', 'inferred_toml', 'explicit_toml'],
)
@pytest.mark.parametrize(
    (
        'ignorePrivateClassAttributes',
        'ignoreUnderscoreOnlyClassAttributes',
        'ignoreSpecialDunderClassAttributes',
        'expectedMissingNames',
    ),
    [
        (True, True, True, []),
        (True, True, False, ['__tablename__: str']),
        (True, False, True, ['_: bool', '__: float']),
        (True, False, False, ['_: bool', '__: float', '__tablename__: str']),
        (False, True, True, ['_private: str']),
        (False, True, False, ['_private: str', '__tablename__: str']),
        (False, False, True, ['_private: str', '_: bool', '__: float']),
        (
            False,
            False,
            False,
            ['_private: str', '_: bool', '__: float', '__tablename__: str'],
        ),
    ],
)
def testClassAttributeNameOptionsPropagateThroughNativeConfig(
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        source: str,
        ignorePrivateClassAttributes: bool,
        ignoreUnderscoreOnlyClassAttributes: bool,
        ignoreSpecialDunderClassAttributes: bool,
        expectedMissingNames: list[str],
) -> None:
    """Ensure CLI and TOML sources propagate all class name controls."""
    monkeypatch.chdir(tmp_path)
    result = _invokeNativeCli(
        source=source,
        fixturePath=classAttributeNameKindsFixture,
        cliOptions=[
            '--style=numpy',
            '--arg-type-hints-in-docstring=False',
            '--ignore-private-class-attributes='
            f'{ignorePrivateClassAttributes}',
            '--ignore-underscore-only-class-attributes='
            f'{ignoreUnderscoreOnlyClassAttributes}',
            '--ignore-special-dunder-class-attributes='
            f'{ignoreSpecialDunderClassAttributes}',
        ],
        tomlOptions=[
            "style = 'numpy'",
            'arg-type-hints-in-docstring = false',
            'ignore-private-class-attributes ='
            f' {str(ignorePrivateClassAttributes).lower()}',
            'ignore-underscore-only-class-attributes ='
            f' {str(ignoreUnderscoreOnlyClassAttributes).lower()}',
            'ignore-special-dunder-class-attributes ='
            f' {str(ignoreSpecialDunderClassAttributes).lower()}',
        ],
    )

    if not expectedMissingNames:
        assert result.exit_code == 0
        assert 'No violations' in result.output
        return

    assert result.exit_code == 1
    assert result.output.count('DOC601') == 1
    assert result.output.count('DOC603') == 1
    actualMissingNames = extractListedNames(
        result.output,
        'Attributes in the class definition but not in the docstring: [',
    )
    assert sorted(actualMissingNames) == sorted(expectedMissingNames)


@pytest.mark.parametrize(
    'source',
    ['cli', 'inferred_toml', 'explicit_toml'],
)
@pytest.mark.parametrize(
    (
        'ignorePrivateArgs',
        'ignoreUnderscoreOnlyArgs',
        'ignoreSpecialDunderArgs',
        'expectedMissingNames',
    ),
    [
        (True, True, True, []),
        (True, True, False, ['__special__: float']),
        (True, False, True, ['_: bool']),
        (True, False, False, ['_: bool', '__special__: float']),
        (False, True, True, ['_private: str']),
        (False, True, False, ['_private: str', '__special__: float']),
        (False, False, True, ['_private: str', '_: bool']),
        (
            False,
            False,
            False,
            ['_private: str', '_: bool', '__special__: float'],
        ),
    ],
)
def testArgumentNameOptionsPropagateThroughNativeConfig(
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        source: str,
        ignorePrivateArgs: bool,
        ignoreUnderscoreOnlyArgs: bool,
        ignoreSpecialDunderArgs: bool,
        expectedMissingNames: list[str],
) -> None:
    """Ensure CLI and TOML sources propagate all argument name controls."""
    monkeypatch.chdir(tmp_path)
    result = _invokeNativeCli(
        source=source,
        fixturePath=argumentNameKindsFixture,
        cliOptions=[
            '--style=google',
            '--arg-type-hints-in-docstring=False',
            f'--ignore-private-args={ignorePrivateArgs}',
            f'--ignore-underscore-only-args={ignoreUnderscoreOnlyArgs}',
            f'--ignore-special-dunder-args={ignoreSpecialDunderArgs}',
        ],
        tomlOptions=[
            "style = 'google'",
            'arg-type-hints-in-docstring = false',
            f'ignore-private-args = {str(ignorePrivateArgs).lower()}',
            'ignore-underscore-only-args ='
            f' {str(ignoreUnderscoreOnlyArgs).lower()}',
            'ignore-special-dunder-args ='
            f' {str(ignoreSpecialDunderArgs).lower()}',
        ],
    )

    if not expectedMissingNames:
        assert result.exit_code == 0
        assert 'No violations' in result.output
        return

    assert result.exit_code == 1
    assert result.output.count('DOC101') == 1
    assert result.output.count('DOC103') == 1
    actualMissingNames = extractListedNames(
        result.output,
        'Arguments in the function signature but not in the docstring: [',
    )
    assert sorted(actualMissingNames) == sorted(expectedMissingNames)


@pytest.mark.parametrize(
    'source',
    ['cli', 'inferred_toml', 'explicit_toml'],
)
@pytest.mark.parametrize(
    ('optionName', 'value', 'expectedMessage'),
    [
        pytest.param(
            'ignore-underscore-args',
            True,
            IGNORE_UNDERSCORE_ARGS_DEFAULT_MESSAGE,
            id='ignore-underscore-args-default',
        ),
        pytest.param(
            'ignore-underscore-args',
            False,
            IGNORE_UNDERSCORE_ARGS_NONDEFAULT_MESSAGE,
            id='ignore-underscore-args-nondefault',
        ),
        pytest.param(
            'should-document-private-class-attributes',
            False,
            SHOULD_DOCUMENT_PRIVATE_CLASS_ATTRIBUTES_DEFAULT_MESSAGE,
            id='should-document-private-class-attributes-default',
        ),
        pytest.param(
            'should-document-private-class-attributes',
            True,
            SHOULD_DOCUMENT_PRIVATE_CLASS_ATTRIBUTES_ENABLED_MESSAGE,
            id='should-document-private-class-attributes-enabled',
        ),
    ],
)
def testRemovedOptionsShowMigrationError(
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        source: str,
        optionName: str,
        value: bool,
        expectedMessage: str,
) -> None:
    """Ensure native config sources reject removed options with guidance."""
    monkeypatch.chdir(tmp_path)
    result = _invokeNativeCli(
        source=source,
        fixturePath=minimalFixture,
        cliOptions=[f'--{optionName}={value}'],
        tomlOptions=[f'{optionName} = {str(value).lower()}'],
    )

    assert result.exit_code == 1
    assert result.output.strip() == expectedMessage


@pytest.mark.parametrize(
    'source',
    ['cli', 'inferred_toml', 'explicit_toml'],
)
@pytest.mark.parametrize(
    (
        'replacementCliOptions',
        'replacementTomlOptions',
        'expectedMissingNames',
    ),
    [
        # The old `True` ignored `_`; delete it and rely on the default
        pytest.param([], [], [], id='ignore-underscore-args-default'),
        # The old `False` required `_` to be documented
        pytest.param(
            ['--ignore-underscore-only-args=False'],
            ['ignore-underscore-only-args = false'],
            ['_: int'],
            id='ignore-underscore-args-nondefault',
        ),
    ],
)
def testIgnoreUnderscoreArgsReplacementPreservesOldBehavior(
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        source: str,
        replacementCliOptions: list[str],
        replacementTomlOptions: list[str],
        expectedMissingNames: list[str],
) -> None:
    """Ensure the recommended replacement keeps the removed behavior."""
    monkeypatch.chdir(tmp_path)
    result = _invokeNativeCli(
        source=source,
        fixturePath=underscoreArgumentFixture,
        cliOptions=[
            '--style=google',
            '--arg-type-hints-in-docstring=False',
            *replacementCliOptions,
        ],
        tomlOptions=[
            "style = 'google'",
            'arg-type-hints-in-docstring = false',
            *replacementTomlOptions,
        ],
    )

    if not expectedMissingNames:
        assert result.exit_code == 0
        assert 'No violations' in result.output
        return

    assert result.exit_code == 1
    assert result.output.count('DOC101') == 1
    assert result.output.count('DOC103') == 1
    actualMissingNames = extractListedNames(
        result.output,
        'Arguments in the function signature but not in the docstring: [',
    )
    assert actualMissingNames == expectedMissingNames


@pytest.mark.parametrize(
    'source',
    ['cli', 'inferred_toml', 'explicit_toml'],
)
@pytest.mark.parametrize(
    (
        'replacementCliOptions',
        'replacementTomlOptions',
        'expectedMissingNames',
        'expectedExtraNames',
    ),
    [
        # The old `False` excluded every underscore-prefixed attribute, so
        # documenting one was an error; delete it and rely on the defaults
        pytest.param(
            [],
            [],
            [],
            ['_private', '_', '__', '__tablename__'],
            id='should-document-private-class-attributes-default',
        ),
        # The old `True` required every underscore-prefixed attribute,
        # including special dunder attributes such as `__tablename__`
        pytest.param(
            [
                '--ignore-private-class-attributes=False',
                '--ignore-underscore-only-class-attributes=False',
                '--ignore-special-dunder-class-attributes=False',
            ],
            [
                'ignore-private-class-attributes = false',
                'ignore-underscore-only-class-attributes = false',
                'ignore-special-dunder-class-attributes = false',
            ],
            ['_private: str', '_: bool', '__: float', '__tablename__: str'],
            [],
            id='should-document-private-class-attributes-enabled',
        ),
    ],
)
def testShouldDocumentPrivateClassAttributesReplacementPreservesOldBehavior(
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        source: str,
        replacementCliOptions: list[str],
        replacementTomlOptions: list[str],
        expectedMissingNames: list[str],
        expectedExtraNames: list[str],
) -> None:
    """Ensure the recommended replacements keep the removed behavior."""
    monkeypatch.chdir(tmp_path)
    cliOptions = [
        '--style=numpy',
        '--arg-type-hints-in-docstring=False',
        *replacementCliOptions,
    ]
    tomlOptions = [
        "style = 'numpy'",
        'arg-type-hints-in-docstring = false',
        *replacementTomlOptions,
    ]

    # Only `public` is documented, so required names are reported as missing
    missingResult = _invokeNativeCli(
        source=source,
        fixturePath=classAttributeNameKindsFixture,
        cliOptions=cliOptions,
        tomlOptions=tomlOptions,
    )
    if expectedMissingNames:
        assert missingResult.exit_code == 1
        assert missingResult.output.count('DOC601') == 1
        assert missingResult.output.count('DOC603') == 1
        actualMissingNames = extractListedNames(
            missingResult.output,
            'Attributes in the class definition but not in the docstring: [',
        )
        assert sorted(actualMissingNames) == sorted(expectedMissingNames)
    else:
        assert missingResult.exit_code == 0
        assert 'No violations' in missingResult.output

    # Every name is documented, so ignored names are reported as extras
    documentedResult = _invokeNativeCli(
        source=source,
        fixturePath=documentedClassAttributesFixture,
        cliOptions=cliOptions,
        tomlOptions=tomlOptions,
    )
    if expectedExtraNames:
        assert documentedResult.exit_code == 1
        assert documentedResult.output.count('DOC602') == 1
        assert documentedResult.output.count('DOC603') == 1
        actualExtraArgs = extractListedNames(
            documentedResult.output,
            'Arguments in the docstring but not in the actual class'
            ' attributes: [',
        )
        actualExtraNames = [
            arg.split(':', maxsplit=1)[0] for arg in actualExtraArgs
        ]
        assert sorted(actualExtraNames) == sorted(expectedExtraNames)
    else:
        assert documentedResult.exit_code == 0
        assert 'No violations' in documentedResult.output
