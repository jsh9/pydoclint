import subprocess
import sys
from pathlib import Path


def testMain():
    """Essentially an integration test"""
    mainScriptPath: Path = Path.cwd().parent / 'pydoclint/main.py'
    result = subprocess.run(
        [
            sys.executable,
            mainScriptPath,
            r'--exclude="\.git|.?venv|\.tox|build"',  # overrides pyproject.toml
            '.',
        ],
        text=True,
        capture_output=True,
    )

    assert result.returncode != 0  # we expect DOC violations to happen
    assert 'Error: ' not in result.stderr  # but we don't expect it to crash
