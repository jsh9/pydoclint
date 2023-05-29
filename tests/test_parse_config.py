from pathlib import Path
from typing import Any, Dict, List

import pytest

from pydoclint.parse_config import findCommonParentFolder, parseOneTomlFile

THIS_DIR = Path(__file__).parent
DATA_DIR = THIS_DIR / 'data'


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
    'filename, expected',
    [
        (Path('a_path_that_doesnt_exist.toml'), {}),
        (
            DATA_DIR / 'example_config.toml',
            {'some_custom_option': True, 'style': 'google'},
        ),
    ],
)
def testParseOneTomlFile(filename: Path, expected: Dict[str, Any]) -> None:
    tomlConfig = parseOneTomlFile(filename)
    assert tomlConfig == expected
