import ast
from pathlib import Path

import click

from pydoclint.violation import Violation
from pydoclint.visitor import Visitor


@click.command(
    context_settings={'help_option_names': ['-h', '--help']},
    # While Click does set this field automatically using the docstring, mypyc
    # (annoyingly) strips them, so we need to set it here too.
    help='Yes',
)
@click.option(
    '-c',
    '--code',
    type=str,
    help='The source code to check',
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
    '-th',
    '--check-arg-order',
    type=bool,
    show_default=True,
    default=True,
    help='Whether to check docstring argument order agasint function signature',
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
        code: str | None,
        paths: tuple[str, ...],
        check_type_hint: bool,
        check_arg_order: bool,
) -> None:
    """Command-line entry point of pydoclint"""
    ctx.ensure_object(dict)

    if paths and code is not None:
        click.echo(
            main.get_usage(ctx)
            + "\n\n'paths' and 'code' cannot be passed simultaneously."
        )
        ctx.exit(1)

    if not paths and code is None:
        click.echo(
            main.get_usage(ctx) + "\n\nOne of 'paths' or 'code' is required."
        )
        ctx.exit(1)

    violationsInAllFiles: dict[str, list[Violation]] = _checkPaths(
        paths=paths,
        checkTypeHint=check_type_hint,
        checkArgOrder=check_arg_order,
    )

    if len(violationsInAllFiles) > 0:
        counter = 0
        for filename, violationsInThisFile in violationsInAllFiles.items():
            counter += 1
            if len(violationsInThisFile) > 0:
                if counter > 1:
                    print('')

                print(filename)
                for violation in violationsInThisFile:
                    print('    ' + str(violation))

        ctx.exit(1)

    ctx.exit(0)


def _checkPaths(
        paths: tuple[str, ...],
        checkTypeHint: bool = True,
        checkArgOrder: bool = True,
) -> dict[str, list[Violation]]:
    filenames: list[Path] = []

    for path_ in paths:
        path = Path(path_)
        if path.is_file():
            filenames.append(path)
        elif path.is_dir():
            filenames.extend(sorted(path.rglob('*.py')))

    allViolations: dict[str, list[Violation]] = {}

    for filename in filenames:
        violationsInThisFile: list[Violation] = _checkFile(
            filename.as_posix(),
            checkTypeHint=checkTypeHint,
            checkArgOrder=checkArgOrder,
        )
        allViolations[filename.as_posix()] = violationsInThisFile

    return allViolations


def _checkFile(
        filename: str,
        checkTypeHint: bool = True,
        checkArgOrder: bool = True,
) -> list[Violation]:
    with open(filename) as fp:
        src: str = ''.join(fp.readlines())

    tree: ast.Module = ast.parse(src)
    visitor = Visitor(
        checkTypeHint=checkTypeHint,
        checkArgOrder=checkArgOrder,
    )
    visitor.visit(tree)
    return visitor.violations


if __name__ == '__main__':
    main()
