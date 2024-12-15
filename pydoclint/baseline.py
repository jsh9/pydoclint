from __future__ import annotations

from itertools import groupby
from pathlib import Path

from pydoclint.utils.violation import Violation

SEPARATOR = '--------------------\n'
LEN_INDENT = 4
INDENT = ' ' * LEN_INDENT


def generateBaseline(
        violationsInAllFiles: dict[str, list[Violation]], path: Path
) -> None:
    """Generate baseline file based of passed violations."""
    with path.open('w', encoding='utf-8') as baseline:
        for file, violations in violationsInAllFiles.items():
            if violations:
                baseline.write(f'{file}\n')
                for violation in violations:
                    baseline.write(f'{INDENT}{str(violation).strip()}\n')

                baseline.write(f'{SEPARATOR}')


def parseBaseline(path: Path) -> dict[str, set[str]]:
    """Parse baseline file."""
    with path.open('r', encoding='utf-8') as baseline:
        parsed: dict[str, set[str]] = {}
        splittedFiles = [
            list(group)
            for key, group in groupby(
                baseline.readlines(), lambda x: x == SEPARATOR
            )
            if not key
        ]
        for file in splittedFiles:
            parsed[file[0].strip()] = {func.strip() for func in file[1:]}

        return parsed


def removeBaselineViolations(
        baseline: dict[str, set[str]],
        violationsInAllFiles: dict[str, list[Violation]],
) -> tuple[bool, dict[str, list[Violation]]]:
    """
    Remove from the violation dictionary the already existing violations
    specified in the baseline file.
    """
    baselineRegenerationNeeded = False
    clearedViolationsAllFiles: dict[str, list[Violation]] = {}
    for file, violations in violationsInAllFiles.items():
        if oldViolations := baseline.get(file):
            newViolations = []
            if len(violations) < len(oldViolations):
                baselineRegenerationNeeded = True

            for violation in violations:
                if f'{str(violation).strip()}' not in oldViolations:
                    newViolations.append(violation)

            if newViolations:
                clearedViolationsAllFiles[file] = newViolations
        elif violations:
            clearedViolationsAllFiles[file] = violations

    return baselineRegenerationNeeded, clearedViolationsAllFiles
