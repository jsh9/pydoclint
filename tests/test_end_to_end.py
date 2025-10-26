import re

from click.testing import CliRunner

from pydoclint.main import main as cliMain

EXCLUDE_PATTERN = r'\.git|.?venv|\.tox|build'
EXCLUDE_REGEX = re.compile(EXCLUDE_PATTERN)


def testMain() -> None:
    """
    Run the Click CLI end-to-end and ensure it reports violations cleanly.
    """
    runner = CliRunner()
    result = runner.invoke(
        cliMain,
        [f'--exclude={EXCLUDE_PATTERN}', '.'],
        catch_exceptions=False,
    )

    assert result.exit_code != 0  # we expect DOC violations to happen
    assert 'Error: ' not in result.output
