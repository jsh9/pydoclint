from pathlib import Path
from typing import Any, Dict, List, Type

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
    'paths, expected',
    [
        (['/a/b/c', '/a/b/d', '/a/b/e/f/g'], '/a/b'),
        (['a/b/c', 'a/b/d', 'a/b/e/f/g'], 'a/b'),
        (['/a/b/c', '/a/b/d', '/a/b/e/f/g/file.txt'], '/a/b'),
        (['/a/b/c', '/e/f/g', '/a/b/e/f/g'], '/'),
        (['~/a/b/c', '~/e/f/g', '~/a/b/e/f/g'], '~'),
        (['a/b/c', 'e/f/g', 'a/b/e/f/g'], '.'),
        (['a/b/c', 'a/b/d', 'a/b/e/f/g'], 'a/b'),
        (['./a/b/c', './a/b/d', './a/b/e/f/g'], 'a/b'),
        (['./a/b/c', './e/f/g', './a/b/e/f/g'], '.'),
    ],
)
def testFindCommonParentFolder(paths: List[str], expected: str) -> None:
    result = findCommonParentFolder(paths, makeAbsolute=False).as_posix()
    assert result == expected


@pytest.mark.parametrize(
    'filename, enforce, expected',
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
        expected: Dict[str, Any],
) -> None:
    tomlConfig = parseOneTomlFile(filename, enforcePydoclintSection=enforce)
    assert tomlConfig == expected


@pytest.mark.parametrize(
    'filename, expectedException',
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
        expectedException: Type[Exception],
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
        samplePath = _writeSamplePythonFile(Path('.'))
        result = runner.invoke(cli_main, [str(samplePath)])
        assert result.exit_code == 0
        assert 'No violations' in result.output


def testCliConfigMissingFileRaisesError() -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        samplePath = _writeSamplePythonFile(Path('.'))
        result = runner.invoke(
            cli_main,
            ['--config', 'custom.toml', str(samplePath)],
        )
        assert result.exit_code == 2
        assert 'Config file "custom.toml" does not exist.' in result.output


def testCliConfigMissingSectionRaisesError() -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        samplePath = _writeSamplePythonFile(Path('.'))
        badConfig = Path('bad.toml')
        badConfig.write_text('[tool.other]\nflag = true\n')
        result = runner.invoke(
            cli_main,
            ['--config', str(badConfig), str(samplePath)],
        )
        assert result.exit_code == 2
        assert (
            'Config file "bad.toml" does not have a [tool.pydoclint] section.'
            in result.output
        )
