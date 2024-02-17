import ast
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import click

from pydoclint import __version__
from pydoclint.baseline import (
    generateBaseline,
    parseBaseline,
    removeBaselineViolations,
)
from pydoclint.parse_config import (
    injectDefaultOptionsFromUserSpecifiedTomlFilePath,
)
from pydoclint.utils.violation import Violation
from pydoclint.visitor import Visitor

# Due to a potential bug in Windows + pre-commit, non-ASCII
# characters cannot be rendered correctly as stdout in the terminal.
# Therefore, we set all CLI output as stderr.
# (More details in https://github.com/jsh9/pydoclint/issues/20)
echoAsError = True


def validateStyleValue(
        context: click.Context,
        param: click.Parameter,
        value: Optional[str],
) -> Optional[str]:
    """Validate the value of the 'style' option"""
    if value not in {'numpy', 'google', 'sphinx'}:
        raise click.BadParameter(
            '"--style" must be "numpy", "google", or "sphinx"'
        )

    return value


@click.command(
    context_settings={'help_option_names': ['-h', '--help']},
    help='Pydoclint, a linter for Python docstring styles',
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
    '-ths',
    '--type-hints-in-signature',
    show_default=True,
    default='None',
    help='(Deprecated) Please use --arg-type-hints-in-signature instead',
)
@click.option(
    '-aths',
    '--arg-type-hints-in-signature',
    type=bool,
    show_default=True,
    default=True,
    help='Whether to require argument type hints in function signatures',
)
@click.option(
    '-thd',
    '--type-hints-in-docstring',
    show_default=True,
    default='None',
    help='(Deprecated) Please use --arg-type-hints-in-docstring instead',
)
@click.option(
    '-athd',
    '--arg-type-hints-in-docstring',
    type=bool,
    show_default=True,
    default=True,
    help='Whether to require type hints in the argument list in docstrings',
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
@click.option(
    '-aid',
    '--allow-init-docstring',
    type=bool,
    show_default=True,
    default=False,
    help='If True, allow both __init__() and the class def to have docstrings',
)
@click.option(
    '--require-return-section-when-returning-none',
    show_default=True,
    default='None',
    help=(
        '(Deprecated) Please use'
        ' --require-return-section-when-returning-nothing instead.'
    ),
)
@click.option(
    '-rrs',
    '--require-return-section-when-returning-nothing',
    type=bool,
    show_default=True,
    default=False,
    help=(
        'If False, a return section is not needed in docstring if'
        ' the function body does not have a "return" statement and'
        ' the return type annotation is "-> None" or "-> NoReturn".'
    ),
)
@click.option(
    '-crt',
    '--check-return-types',
    type=bool,
    show_default=True,
    default=True,
    help=(
        'If True, check that the type(s) in the docstring return section and'
        ' the return annotation in the function signature are consistent'
    ),
)
@click.option(
    '-rys',
    '--require-yield-section-when-yielding-nothing',
    type=bool,
    show_default=True,
    default=False,
    help=(
        'If False, a yields section is not needed in docstring if'
        ' the function yields None.'
    ),
)
@click.option(
    '-cyt',
    '--check-yield-types',
    type=bool,
    show_default=True,
    default=True,
    help=(
        'If True, check that the type(s) in the docstring "yields" section and'
        ' the return annotation in the function signature are consistent'
    ),
)
@click.option(
    '-iua',
    '--ignore-underscore-args',
    type=bool,
    show_default=True,
    default=True,
    help=(
        'If True, underscore arguments (such as _, __, ...) in the function'
        ' signature do not need to appear in the docstring.'
    ),
)
@click.option(
    '--baseline',
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        readable=True,
        writable=True,
        allow_dash=True,
    ),
    help=(
        'The file name containing the existing violations (the "baseline").'
        ' If specified, only new violations will be reported, and the'
        ' violations in the baseline file are ignored.'
    ),
)
@click.option(
    '--generate-baseline',
    type=bool,
    show_default=True,
    default=False,
    help=(
        'If True, generates a new baseline file. (The name of the baseline'
        ' file should be specified by the --baseline option.)'
    ),
)
@click.option(
    '-sfn',
    '--show-filenames-in-every-violation-message',
    type=bool,
    show_default=True,
    default=False,
    help='If True, show file names in the front of every violation message.',
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
@click.option(
    '--config',
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        readable=True,
        allow_dash=False,
        path_type=str,
    ),
    is_eager=True,
    callback=injectDefaultOptionsFromUserSpecifiedTomlFilePath,
    default='pyproject.toml',
    help=(
        'The full path of the .toml config file that contains the config'
        ' options; note that the command line options take precedence'
        ' over the .toml file'
    ),
)
@click.version_option(__version__)
@click.pass_context
def main(  # noqa: C901
        ctx: click.Context,
        quiet: bool,
        exclude: str,
        style: str,
        paths: Tuple[str, ...],
        type_hints_in_signature: str,
        type_hints_in_docstring: str,
        arg_type_hints_in_signature: bool,
        arg_type_hints_in_docstring: bool,
        check_arg_order: bool,
        skip_checking_short_docstrings: bool,
        skip_checking_raises: bool,
        allow_init_docstring: bool,
        check_return_types: bool,
        check_yield_types: bool,
        ignore_underscore_args: bool,
        require_return_section_when_returning_none: bool,
        require_return_section_when_returning_nothing: bool,
        require_yield_section_when_yielding_nothing: bool,
        generate_baseline: bool,
        baseline: str,
        show_filenames_in_every_violation_message: bool,
        config: Optional[str],  # don't remove it b/c it's required by `click`
) -> None:
    """Command-line entry point of pydoclint"""
    ctx.ensure_object(dict)

    if type_hints_in_docstring != 'None':  # it means users supply this option
        click.echo(
            click.style(
                ''.join([
                    'The option `--type-hints-in-docstring` has been renamed;',
                    ' please use `--arg-type-hints-in-docstring` instead',
                ]),
                fg='red',
                bold=True,
            ),
            err=echoAsError,
        )
        ctx.exit(1)

    if type_hints_in_signature != 'None':  # it means users supply this option
        click.echo(
            click.style(
                ''.join([
                    'The option `--type-hints-in-signature` has been renamed;',
                    ' please use `--arg-type-hints-in-signature` instead',
                ]),
                fg='red',
                bold=True,
            ),
            err=echoAsError,
        )
        ctx.exit(1)

    # it means users supply this option
    if require_return_section_when_returning_none != 'None':
        click.echo(
            click.style(
                ''.join([
                    'The option `--require-return-section-when-returning-none`',
                    ' has been renamed; please use',
                    '`--require-return-section-when-returning-nothing` instead',
                ]),
                fg='red',
                bold=True,
            ),
            err=echoAsError,
        )
        ctx.exit(1)

    # it means users supply this option
    if baseline is not None:
        baselinePath = Path(baseline)
        if not (generate_baseline or baselinePath.exists()):
            click.echo(
                click.style(
                    "The baseline file was specified but it doesn't exist.\n"
                    'Use --generate-baseline True to generate it.',
                    fg='red',
                    bold=True,
                ),
                err=echoAsError,
            )
            ctx.exit(1)

    violationsInAllFiles: Dict[str, List[Violation]] = _checkPaths(
        quiet=quiet,
        exclude=exclude,
        style=style,
        paths=paths,
        argTypeHintsInSignature=arg_type_hints_in_signature,
        argTypeHintsInDocstring=arg_type_hints_in_docstring,
        checkArgOrder=check_arg_order,
        skipCheckingShortDocstrings=skip_checking_short_docstrings,
        skipCheckingRaises=skip_checking_raises,
        allowInitDocstring=allow_init_docstring,
        checkReturnTypes=check_return_types,
        checkYieldTypes=check_yield_types,
        ignoreUnderscoreArgs=ignore_underscore_args,
        requireReturnSectionWhenReturningNothing=(
            require_return_section_when_returning_nothing
        ),
        requireYieldSectionWhenYieldingNothing=(
            require_yield_section_when_yielding_nothing
        ),
    )

    if generate_baseline:
        if baseline is None:
            click.echo(
                click.style(
                    'The baseline file was not specified. '
                    'Use --baseline option or specify it in your config file',
                    fg='red',
                    bold=True,
                ),
                err=echoAsError,
            )
            ctx.exit(1)

        generateBaseline(violationsInAllFiles, baselinePath)
        click.echo(
            click.style(
                'Baseline file was sucessfuly generated', fg='green', bold=True
            ),
            err=echoAsError,
        )
        ctx.exit(0)

    if baseline is not None:
        parsedBaseline = parseBaseline(baselinePath)
        (
            baselineRegenerationNeeded,
            violationsInAllFiles,
        ) = removeBaselineViolations(parsedBaseline, violationsInAllFiles)
        if baselineRegenerationNeeded:
            click.echo(
                click.style(
                    'Some old violations was fixed. Please regenerate'
                    ' your baseline file after fixing new problems.\n'
                    'Use option --generate-baseline True',
                    fg='red',
                    bold=True,
                ),
                err=echoAsError,
            )

    violationCounter: int = 0
    if len(violationsInAllFiles) > 0:
        counter = 0
        for filename, violationsInThisFile in violationsInAllFiles.items():
            counter += 1
            if len(violationsInThisFile) > 0:
                if counter > 1:
                    print('')

                if not show_filenames_in_every_violation_message:
                    click.echo(
                        click.style(filename, fg='yellow', bold=True),
                        err=echoAsError,
                    )

                for violation in violationsInThisFile:
                    violationCounter += 1
                    if not show_filenames_in_every_violation_message:
                        fourSpaces = '    '
                        click.echo(fourSpaces, nl=False, err=echoAsError)
                    else:
                        click.echo(
                            click.style(filename, fg='yellow', bold=True),
                            nl=False,
                            err=echoAsError,
                        )
                        click.echo(':', nl=False, err=echoAsError)

                    click.echo(
                        f'{violation.line}: ', nl=False, err=echoAsError
                    )
                    click.echo(
                        click.style(
                            f'{violation.fullErrorCode}',
                            fg='red',
                            bold=True,
                        ),
                        nl=False,
                        err=echoAsError,
                    )
                    click.echo(f': {violation.msg}', err=echoAsError)

    if violationCounter > 0:
        ctx.exit(1)
    else:
        if not quiet:
            click.echo(
                click.style('🎉 No violations 🎉', fg='green', bold=True),
                err=echoAsError,
            )

        ctx.exit(0)


def _checkPaths(
        paths: Tuple[str, ...],
        style: str = 'numpy',
        argTypeHintsInSignature: bool = True,
        argTypeHintsInDocstring: bool = True,
        checkArgOrder: bool = True,
        skipCheckingShortDocstrings: bool = True,
        skipCheckingRaises: bool = False,
        allowInitDocstring: bool = False,
        checkReturnTypes: bool = True,
        checkYieldTypes: bool = True,
        ignoreUnderscoreArgs: bool = True,
        requireReturnSectionWhenReturningNothing: bool = False,
        requireYieldSectionWhenYieldingNothing: bool = False,
        quiet: bool = False,
        exclude: str = '',
) -> Dict[str, List[Violation]]:
    filenames: List[Path] = []

    if not quiet:
        skipMsg = f'Skipping files that match this pattern: {exclude}'
        click.echo(
            click.style(skipMsg, fg='yellow', bold=True), err=echoAsError
        )

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
            click.echo(
                click.style(filename, fg='cyan', bold=True), err=echoAsError
            )

        violationsInThisFile: List[Violation] = _checkFile(
            filename,
            style=style,
            argTypeHintsInSignature=argTypeHintsInSignature,
            argTypeHintsInDocstring=argTypeHintsInDocstring,
            checkArgOrder=checkArgOrder,
            skipCheckingShortDocstrings=skipCheckingShortDocstrings,
            skipCheckingRaises=skipCheckingRaises,
            allowInitDocstring=allowInitDocstring,
            checkReturnTypes=checkReturnTypes,
            checkYieldTypes=checkYieldTypes,
            ignoreUnderscoreArgs=ignoreUnderscoreArgs,
            requireReturnSectionWhenReturningNothing=(
                requireReturnSectionWhenReturningNothing
            ),
            requireYieldSectionWhenYieldingNothing=(
                requireYieldSectionWhenYieldingNothing
            ),
        )
        allViolations[filename.as_posix()] = violationsInThisFile

    return allViolations


def _checkFile(
        filename: Path,
        style: str = 'numpy',
        argTypeHintsInSignature: bool = True,
        argTypeHintsInDocstring: bool = True,
        checkArgOrder: bool = True,
        skipCheckingShortDocstrings: bool = True,
        skipCheckingRaises: bool = False,
        allowInitDocstring: bool = False,
        checkReturnTypes: bool = True,
        checkYieldTypes: bool = True,
        ignoreUnderscoreArgs: bool = True,
        requireReturnSectionWhenReturningNothing: bool = False,
        requireYieldSectionWhenYieldingNothing: bool = False,
) -> List[Violation]:
    with open(filename, encoding='utf8') as fp:
        src: str = ''.join(fp.readlines())

    tree: ast.Module = ast.parse(src)
    visitor = Visitor(
        style=style,
        argTypeHintsInSignature=argTypeHintsInSignature,
        argTypeHintsInDocstring=argTypeHintsInDocstring,
        checkArgOrder=checkArgOrder,
        skipCheckingShortDocstrings=skipCheckingShortDocstrings,
        skipCheckingRaises=skipCheckingRaises,
        allowInitDocstring=allowInitDocstring,
        checkReturnTypes=checkReturnTypes,
        checkYieldTypes=checkYieldTypes,
        ignoreUnderscoreArgs=ignoreUnderscoreArgs,
        requireReturnSectionWhenReturningNothing=(
            requireReturnSectionWhenReturningNothing
        ),
        requireYieldSectionWhenYieldingNothing=(
            requireYieldSectionWhenYieldingNothing
        ),
    )
    visitor.visit(tree)
    return visitor.violations


if __name__ == '__main__':
    main()
