from pydoclint.main import _checkFile
from tests.test_main import DATA_DIR


def testPlayground() -> None:
    """
    This is a placeholder test for testing the `playground.py` file.

    When you want to quickly test something, you can add contents into
    tests/test_data/playground.py and run this test function.
    """
    violations = _checkFile(
        filename=DATA_DIR / 'playground.py',
        style='google',
    )
    expected = []
    assert list(map(str, violations)) == expected
