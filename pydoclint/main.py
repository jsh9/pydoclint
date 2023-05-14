import ast
from pathlib import Path
import click

from pydoclint.visitor import Visitor
from pydoclint.violation import Violation


@click.command(
    context_settings={"help_option_names": ["-h", "--help"]},
    # While Click does set this field automatically using the docstring, mypyc
    # (annoyingly) strips 'em so we need to set it here too.
    help="Yes",
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
) -> int:
    """Main entry point of pydoclint"""

    ctx.ensure_object(dict)

    if paths and code is not None:
        click.echo(
            main.get_usage(ctx)
            + "\n\n'paths' and 'code' cannot be passed simultaneously."
        )
        ctx.exit(1)

    if not paths and code is None:
        click.echo(main.get_usage(ctx) + "\n\nOne of 'paths' or 'code' is required.")
        ctx.exit(1)

    checkPathsStatus: int = _checkPaths(
        paths=paths,
        checkTypeHint=check_type_hint,
        checkArgOrder=check_arg_order,
    )

    ctx.exit(checkPathsStatus)


def _checkPaths(
        paths: tuple[str, ...],
        checkTypeHint: bool = True,
        checkArgOrder: bool = True,
):
    filenames: list[Path] = []

    for path_ in paths:
        path = Path(path_)
        if path.is_file():
            filenames.append(path)
        elif path.is_dir():
            filenames.extend(sorted(path.rglob('*.py')))

    for filename in filenames:
        with open(filename) as fp:
            src: str = ''.join(fp.readlines())

        tree: ast.Module = ast.parse(src)

        visitor = Visitor(
            checkTypeHint=checkTypeHint,
            checkArgOrder=checkArgOrder,
        )
        visitor.visit(tree)

        violations: list[Violation] = visitor.violations
        print(violations)

        if len(violations) > 0:
            return 1

        return 0


if __name__ == '__main__':
    main()
