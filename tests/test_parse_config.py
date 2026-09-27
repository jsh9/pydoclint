import shutil
from pathlib import Path
from typing import Any

import pytest
from click.testing import CliRunner

from pydoclint.main import main as cli_main
from pydoclint.parse_config import (
    MissingPydoclintSectionError,
    findCommonParentFolder,
    parseOneTomlFile,
)

THIS_DIR = Path(__file__).parent
DATA_DIR = THIS_DIR / 'test_data'
CONFIG_DATA_DIR: Path = DATA_DIR / 'config_files'
minimalFixture = DATA_DIR / 'common/minimal.py'
classAttributeNameKindsFixture = (
    DATA_DIR / 'private_and_underscore_only_options/class_attributes.py'
)
underscoreArgumentFixture = (
    DATA_DIR
    / 'private_and_underscore_only_options'
    / 'underscore_only_function_argument.py'
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


@pytest.mark.parametrize(
    'source',
    ['cli', 'inferred_toml', 'explicit_toml'],
)
@pytest.mark.parametrize(
    (
        'ignorePrivateClassAttributes',
        'ignoreUnderscoreOnlyClassAttributes',
        'expectedMissingNames',
    ),
    [
        (True, True, []),
        (True, False, ['_: bool', '__: float']),
        (False, True, ['_private: str']),
        (False, False, ['_private: str', '_: bool', '__: float']),
    ],
)
def testClassAttributeNameOptionsPropagateThroughNativeConfig(
        source: str,
        ignorePrivateClassAttributes: bool,
        ignoreUnderscoreOnlyClassAttributes: bool,
        expectedMissingNames: list[str],
) -> None:
    """Ensure CLI and TOML sources propagate both class name controls."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        samplePath = _copyPythonFixture(
            Path(),
            classAttributeNameKindsFixture,
        )
        arguments = _getConfigArguments(
            source=source,
            samplePath=samplePath,
            cliOptions=[
                '--style=numpy',
                '--arg-type-hints-in-docstring=False',
                '--ignore-private-class-attributes='
                f'{ignorePrivateClassAttributes}',
                '--ignore-underscore-only-class-attributes='
                f'{ignoreUnderscoreOnlyClassAttributes}',
            ],
            tomlOptions=[
                "style = 'numpy'",
                'arg-type-hints-in-docstring = false',
                'ignore-private-class-attributes ='
                f' {str(ignorePrivateClassAttributes).lower()}',
                'ignore-underscore-only-class-attributes ='
                f' {str(ignoreUnderscoreOnlyClassAttributes).lower()}',
            ],
        )

        result = runner.invoke(cli_main, arguments)
        if not expectedMissingNames:
            assert result.exit_code == 0
            assert 'No violations' in result.output
            return

        assert result.exit_code == 1
        assert result.output.count('DOC601') == 1
        assert result.output.count('DOC603') == 1
        actualMissingNames = (
            result.output
            .split(
                'Attributes in the class definition but not in the docstring: [',
                maxsplit=1,
            )[1]
            .split('].', maxsplit=1)[0]
            .split(', ')
        )
        assert sorted(actualMissingNames) == sorted(expectedMissingNames)


@pytest.mark.parametrize(
    'source',
    ['cli', 'inferred_toml', 'explicit_toml'],
)
@pytest.mark.parametrize('ignoreUnderscoreOnlyArgs', [True, False])
def testUnderscoreOnlyArgumentOptionPropagatesThroughNativeConfig(
        source: str,
        ignoreUnderscoreOnlyArgs: bool,
) -> None:
    """Ensure CLI and TOML propagate the underscore-only argument control."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        samplePath = _copyPythonFixture(Path(), underscoreArgumentFixture)
        arguments = _getConfigArguments(
            source=source,
            samplePath=samplePath,
            cliOptions=[
                '--style=google',
                '--arg-type-hints-in-docstring=False',
                '--check-return-types=False',
                f'--ignore-underscore-only-args={ignoreUnderscoreOnlyArgs}',
            ],
            tomlOptions=[
                "style = 'google'",
                'arg-type-hints-in-docstring = false',
                'check-return-types = false',
                'ignore-underscore-only-args ='
                f' {str(ignoreUnderscoreOnlyArgs).lower()}',
            ],
        )

        result = runner.invoke(cli_main, arguments)
        if ignoreUnderscoreOnlyArgs:
            assert result.exit_code == 0
            assert 'No violations' in result.output
        else:
            assert result.exit_code == 1
            assert result.output.count('DOC101') == 1
            assert result.output.count('DOC103') == 1
            assert (
                'Arguments in the function signature but not in the'
                ' docstring: [_: int].' in result.output
            )


@pytest.mark.parametrize(
    'source',
    ['cli', 'inferred_toml', 'explicit_toml'],
)
@pytest.mark.parametrize(
    ('optionName', 'value', 'expectedMessage'),
    [
        (
            'ignore-underscore-args',
            True,
            'The option `--ignore-underscore-args` no longer works; remove it.'
            ' Its replacement, `--ignore-underscore-only-args`, defaults to'
            ' `True` (`ignore-underscore-only-args = true` in TOML/Flake8),'
            ' which preserves this behavior.',
        ),
        (
            'ignore-underscore-args',
            False,
            'The option `--ignore-underscore-args` no longer works. Replace it'
            ' with `--ignore-underscore-only-args=False` on the command line or'
            ' `ignore-underscore-only-args = false` in TOML/Flake8 config.',
        ),
        (
            'should-document-private-class-attributes',
            True,
            'The option `--should-document-private-class-attributes` no longer'
            ' works. Use `--ignore-private-class-attributes=False` and'
            ' `--ignore-underscore-only-class-attributes=False` on the command'
            ' line, or `ignore-private-class-attributes = false` and'
            ' `ignore-underscore-only-class-attributes = false` in TOML/Flake8'
            ' config. Special dunder class attributes are always excluded.',
        ),
        (
            'should-document-private-class-attributes',
            False,
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
        source: str,
        optionName: str,
        value: bool,
        expectedMessage: str,
) -> None:
    """Ensure native config sources reject removed options with guidance."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        samplePath = _copyPythonFixture(Path(), minimalFixture)

        arguments = _getConfigArguments(
            source=source,
            samplePath=samplePath,
            cliOptions=[f'--{optionName}={value}'],
            tomlOptions=[f'{optionName} = {str(value).lower()}'],
        )

        result = runner.invoke(cli_main, arguments)
        assert result.exit_code == 1
        assert expectedMessage in result.output
