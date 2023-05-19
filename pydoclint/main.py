import ast
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import click

from pydoclint.utils.violation import Violation
from pydoclint.visitor import Visitor


def validateStyleValue(
        context: click.Context,
        param: click.Parameter,
        value: Optional[str],
) -> Optional[str]:
    """Validate the value of the 'style' option"""
    if value not in {'numpy', 'google'}:
        raise click.BadParameter('"--style" must be "numpy" or "google"')

    return value


@click.command(
    context_settings={'help_option_names': ['-h', '--help']},
    # While Click does set this field automatically using the docstring, mypyc
    # (annoyingly) strips them, so we need to set it here too.
    help='Yes',
)
@click.option(
    '-s',
    '--src',
    type=str,
    help='The source code to check',
)
@click.option(
    '-q',
    '--quiet',
    is_flag=True,
    default=False,
    help='If True, do not print the file names being checked to the terminal.',
)
@click.option(
    '--exclude',
    type=str,
    show_default=True,
    default=r'\.git|\.tox',
    help=(
        'Regex pattern to exclude files/folders. Please add quotes (both'
        ' double and single quotes are fine) around the regex in the'
        ' command line.'
    ),
)
@click.option(
    '--style',
    type=str,
    show_default=True,
    default='numpy',
    callback=validateStyleValue,
    help='',
)
@click.option(
    '-th',
    '--check-type-hint',
    type=bool,
    show_default=True,
    default=True,
    help='Whether to check type hints in docstrings',
)
@click.option(
    '-ao',
    '--check-arg-order',
    type=bool,
    show_default=True,
    default=True,
    help='Whether to check docstring argument order against function signature',
)
@click.option(
    '-scsd',
    '--skip-checking-short-docstrings',
    type=bool,
    show_default=True,
    default=True,
    help='If True, skip checking if the docstring only has a short summary.',
)
@click.option(
    '-scr',
    '--skip-checking-raises',
    type=bool,
    show_default=True,
    default=False,
    help='If True, skip checking docstring "Raises" section against "raise" statements',
)
@click.argument(
    'paths',
    nargs=-1,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True,
        allow_dash=True,
    ),
    is_eager=True,
)
@click.pass_context
def main(
        ctx: click.Context,
        quiet: bool,
        exclude: str,
        style: str,
        src: Optional[str],
        paths: Tuple[str, ...],
        check_type_hint: bool,
        check_arg_order: bool,
        skip_checking_short_docstrings: bool,
        skip_checking_raises: bool,
) -> None:
    """Command-line entry point of pydoclint"""
    ctx.ensure_object(dict)

    if paths and src is not None:
        click.echo(
            main.get_usage(ctx)
            + "\n\n'paths' and 'src' cannot be passed simultaneously."
        )
        ctx.exit(1)

    if not paths and src is None:
        click.echo(
            main.get_usage(ctx) + "\n\nOne of 'paths' or 'src' is required."
        )
        ctx.exit(1)

    violationsInAllFiles: Dict[str, List[Violation]] = _checkPaths(
        quiet=quiet,
        exclude=exclude,
        style=style,
        paths=paths,
        checkTypeHint=check_type_hint,
        checkArgOrder=check_arg_order,
        skipCheckingShortDocstrings=skip_checking_short_docstrings,
        skipCheckingRaises=skip_checking_raises,
    )

    violationCounter: int = 0
    if len(violationsInAllFiles) > 0:
        counter = 0
        for filename, violationsInThisFile in violationsInAllFiles.items():
            counter += 1
            if len(violationsInThisFile) > 0:
                if counter > 1:
                    print('')

                click.echo(click.style(filename, fg='yellow', bold=True))
                for violation in violationsInThisFile:
                    violationCounter += 1
                    fourSpaces = '    '
                    click.echo(fourSpaces, nl=False)
                    click.echo(f'{violation.line}: ', nl=False)
                    click.echo(
                        click.style(
                            f'{violation.fullErrorCode}',
                            fg='red',
                            bold=True,
                        ),
                        nl=False,
                    )
                    click.echo(f': {violation.msg}')

    if violationCounter > 0:
        ctx.exit(1)
    else:
        if not quiet:
            click.echo(click.style('🎉 No violations 🎉', fg='green', bold=True))

        ctx.exit(0)


def _checkPaths(
        paths: Tuple[str, ...],
        style: str = 'numpy',
        checkTypeHint: bool = True,
        checkArgOrder: bool = True,
        skipCheckingShortDocstrings: bool = True,
        skipCheckingRaises: bool = False,
        quiet: bool = False,
        exclude: str = '',
) -> Dict[str, List[Violation]]:
    filenames: List[Path] = []

    if not quiet:
        skipMsg = f'Skipping files that match this pattern: {exclude}'
        click.echo(click.style(skipMsg, fg='yellow', bold=True))

    excludePattern = re.compile(exclude)

    for path_ in paths:
        path = Path(path_)
        if path.is_file():
            filenames.append(path)
        elif path.is_dir():
            filenames.extend(sorted(path.rglob('*.py')))

    allViolations: Dict[str, List[Violation]] = {}

    for filename in filenames:
        if excludePattern.search(filename.as_posix()):
            continue

        if not quiet:
            click.echo(click.style(filename, fg='cyan', bold=True))

        violationsInThisFile: List[Violation] = _checkFile(
            filename,
            style=style,
            checkTypeHint=checkTypeHint,
            checkArgOrder=checkArgOrder,
            skipCheckingShortDocstrings=skipCheckingShortDocstrings,
            skipCheckingRaises=skipCheckingRaises,
        )
        allViolations[filename.as_posix()] = violationsInThisFile

    return allViolations


def _checkFile(
        filename: Path,
        style: str = 'numpy',
        checkTypeHint: bool = True,
        checkArgOrder: bool = True,
        skipCheckingShortDocstrings: bool = True,
        skipCheckingRaises: bool = False,
) -> List[Violation]:
    with open(filename) as fp:
        src: str = ''.join(fp.readlines())

    tree: ast.Module = ast.parse(src)
    visitor = Visitor(
        style=style,
        checkTypeHint=checkTypeHint,
        checkArgOrder=checkArgOrder,
        skipCheckingShortDocstrings=skipCheckingShortDocstrings,
        skipCheckingRaises=skipCheckingRaises,
    )
    visitor.visit(tree)
    return visitor.violations


if __name__ == '__main__':
    main()
