import sys
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

import click

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def parseConfig(
        ctx: click.Context,
        file: str,
        quiet: bool = False,
) -> None:
    """
    Inject default objects from user-specified .toml file path.

    Parameters
    ----------
    ctx : click.Context
        The "click" context
    file : str
        The full path of the .toml file. (It needs to be named ``value``
        so that ``click`` can correctly use it as a callback function.)
    quiet : bool
        Should the output be silenced. Defaults to False.
    """
    if not quiet:
        click.echo(f'Loading config from user-specified .toml file: {file}')
    config = parseOneTomlFile(tomlFilename=Path(file), quiet=quiet)
    updateCtxDefaultMap(ctx=ctx, config=config)


def parseToml(
        paths: Optional[Sequence[str]], quiet: bool = False
) -> Dict[str, Any]:
    """Parse the pyproject.toml located in the common parent of ``paths``"""
    if paths is None:
        return {}

    commonParent: Path = findCommonParentFolder(paths)
    tomlFilename = commonParent / Path('pyproject.toml')
    if not quiet:
        click.echo(
            f'Loading config from inferred .toml file path: {tomlFilename}'
        )
    return parseOneTomlFile(tomlFilename, quiet=quiet)


def parseOneTomlFile(
        tomlFilename: Path, quiet: bool = False
) -> Dict[str, Any]:
    """Parse a .toml file"""
    if not tomlFilename.exists():
        click.echo(f'File "{tomlFilename}" does not exist; nothing to load.')
        return {}

    try:
        with open(tomlFilename, 'rb') as fp:
            rawConfig = tomllib.load(fp)

        pydoclintSection = rawConfig['tool']['pydoclint']
        finalConfig = {
            k.replace('-', '_'): v for k, v in pydoclintSection.items()
        }
    except Exception:
        finalConfig = {}

    if not quiet:
        if len(finalConfig) > 0:
            click.echo(f'Found options defined in {tomlFilename}:')
            click.echo(finalConfig)
        else:
            click.echo(f'No config found in {tomlFilename}.')

    return finalConfig


def findCommonParentFolder(
        paths: Sequence[str],
        makeAbsolute: bool = True,  # allow makeAbsolute=False just for testing
) -> Path:
    """Find the common parent folder of the given ``paths``"""
    paths = [Path(path) for path in paths]

    common_parent = paths[0]
    for path in paths[1:]:
        if len(common_parent.parts) > len(path.parts):
            common_parent, path = path, common_parent

        for i, part in enumerate(common_parent.parts):
            if part != path.parts[i]:
                common_parent = Path(*common_parent.parts[:i])
                break

    if makeAbsolute:
        return common_parent.absolute()

    return common_parent


def updateCtxDefaultMap(ctx: click.Context, config: Dict[str, Any]) -> None:
    """Update the ``click`` context default map with the provided ``config``"""
    default_map: Dict[str, Any] = {}
    if ctx.default_map:
        default_map.update(ctx.default_map)

    default_map.update(config)
    ctx.default_map = default_map
