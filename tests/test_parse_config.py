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
CONFIG_DATA_DIR: Path = THIS_DIR / 'test_data' / 'config_files'


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


def _writeSamplePythonFile(directory: Path) -> Path:
    """Create a minimal Python file that passes linting."""
    samplePath = directory / 'sample.py'
    # fmt: off
    samplePath.write_text(
        'def foo():\n'
        '    """Summary."""\n'
        '    pass\n'
    )
    # fmt: on
    return samplePath


def testCliDefaultConfigMissingFileIsAllowed() -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        samplePath = _writeSamplePythonFile(Path())
        result = runner.invoke(cli_main, [str(samplePath)])
        assert result.exit_code == 0
        assert 'No violations' in result.output


def testCliConfigMissingFileRaisesError() -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        samplePath = _writeSamplePythonFile(Path())
        result = runner.invoke(
            cli_main,
            ['--config', 'custom.toml', str(samplePath)],
        )
        assert result.exit_code == 2
        assert 'Config file "custom.toml" does not exist.' in result.output


def testCliConfigMissingSectionRaisesError() -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        samplePath = _writeSamplePythonFile(Path())
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


@pytest.mark.parametrize('source', ['cli', 'toml'])
@pytest.mark.parametrize(
    ('optionName', 'value', 'expectedMessage'),
    [
        (
            'ignore-underscore-args',
            True,
            'The option `--ignore-underscore-args` no longer works; please use '
            '`--ignore-underscore-only-args=True` instead',
        ),
        (
            'ignore-underscore-args',
            False,
            'The option `--ignore-underscore-args` no longer works; please use '
            '`--ignore-underscore-only-args=False` instead',
        ),
        (
            'should-document-private-class-attributes',
            True,
            'The option `--should-document-private-class-attributes` no longer '
            'works. To preserve its previous behavior, please use both '
            '`--ignore-private-class-attributes=False` and '
            '`--ignore-underscore-only-class-attributes=False` instead',
        ),
        (
            'should-document-private-class-attributes',
            False,
            'The option `--should-document-private-class-attributes` no longer '
            'works. To preserve its previous behavior, please use both '
            '`--ignore-private-class-attributes=True` and '
            '`--ignore-underscore-only-class-attributes=True` instead',
        ),
    ],
)
def testRemovedOptionsShowMigrationError(
        source: str,
        optionName: str,
        value: bool,
        expectedMessage: str,
) -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        samplePath = _writeSamplePythonFile(Path())

        if source == 'cli':
            arguments = [
                f'--{optionName}={value}',
                str(samplePath),
            ]
        else:
            configPath = Path('pyproject.toml')
            configPath.write_text(
                f'[tool.pydoclint]\n{optionName} = {str(value).lower()}\n',
                encoding='utf-8',
            )
            arguments = [str(samplePath)]

        result = runner.invoke(cli_main, arguments)
        assert result.exit_code == 1
        assert expectedMessage in result.output
