from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

import click
from click.core import ParameterSource

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


class MissingPydoclintSectionError(RuntimeError):
    """Raised when the [tool.pydoclint] section is missing in a config file."""


def injectDefaultOptionsFromUserSpecifiedTomlFilePath(
        ctx: click.Context,
        param: click.Parameter,
        value: str | None,
) -> str | None:
    """
    Inject default objects from user-specified .toml file path.

    Parameters
    ----------
    ctx : click.Context
        The "click" context
    param : click.Parameter
        The "click" parameter; not used in this function; just a placeholder
    value : str | None
        The full path of the .toml file. (It needs to be named ``value`` so
        that ``click`` can correctly use it as a callback function.)

    Returns
    -------
    str | None
        The full path of the .toml file

    Raises
    ------
    click.BadParameter
        If the path supplied doesn't exist or lacks a [tool.pydoclint] section
    """
    if not value:
        return None

    logger.info('Loading config from user-specified .toml file: %s', value)

    # Only enforce when users explicitly specify a config file
    assert param.name is not None  # so that mypy is happy
    enforcePydoclintSection = (
        ctx.get_parameter_source(param.name) == ParameterSource.COMMANDLINE
    )

    try:
        config = parseOneTomlFile(
            tomlFilename=Path(value),
            enforcePydoclintSection=enforcePydoclintSection,
        )
    except FileNotFoundError as exc:
        raise click.BadParameter(str(exc), ctx=ctx, param=param) from exc
    except MissingPydoclintSectionError as exc:
        raise click.BadParameter(str(exc), ctx=ctx, param=param) from exc

    updateCtxDefaultMap(ctx=ctx, config=config)
    return value


def parseToml(paths: Sequence[str] | None) -> dict[str, Any]:
    """Parse the pyproject.toml located in the common parent of ``paths``"""
    if paths is None:
        return {}

    commonParent: Path = findCommonParentFolder(paths)
    tomlFilename = commonParent / Path('pyproject.toml')
    logger.info(
        'Loading config from inferred .toml file path: %s', tomlFilename
    )
    return parseOneTomlFile(tomlFilename)


def parseOneTomlFile(
        tomlFilename: Path,
        *,
        enforcePydoclintSection: bool = False,
) -> dict[str, Any]:
    """Parse a .toml file"""
    if not tomlFilename.exists():
        message = f'Config file "{tomlFilename}" does not exist.'
        logger.info('%s Nothing to load.', message)
        if enforcePydoclintSection:
            raise FileNotFoundError(message)

        return {}

    try:
        with Path(tomlFilename).open('rb') as fp:
            rawConfig = tomllib.load(fp)
    except Exception as exc:
        logger.info(
            'Failed to load "%s": %s; ignoring this', tomlFilename, exc
        )
        if enforcePydoclintSection:
            raise

        return {}

    toolSection = rawConfig.get('tool')
    if not isinstance(toolSection, dict) or 'pydoclint' not in toolSection:
        message = (
            f'Config file "{tomlFilename}" does not have'
            ' a [tool.pydoclint] section.'
        )
        logger.info(message)
        if enforcePydoclintSection:
            raise MissingPydoclintSectionError(message)

        finalConfig = {}
    else:
        pydoclintSection = toolSection['pydoclint']
        finalConfig = {
            k.replace('-', '_'): v for k, v in pydoclintSection.items()
        }

    if len(finalConfig) > 0:
        logger.info('Found options defined in %s:', tomlFilename)
        logger.info(finalConfig)
    else:
        logger.info('No config found in %s.', tomlFilename)

    return finalConfig


def findCommonParentFolder(
        paths: Sequence[str],
        *,
        makeAbsolute: bool = True,  # allow makeAbsolute=False just for testing
) -> Path:
    """Find the common parent folder of the given ``paths``"""
    paths_: Sequence[Path] = [Path(path) for path in paths]

    common_parent = paths_[0]
    for candidate_path in paths_[1:]:
        reference = common_parent
        comparison = candidate_path
        if len(reference.parts) > len(comparison.parts):
            reference, comparison = comparison, reference

        new_common = reference
        for i, part in enumerate(reference.parts):
            if part != comparison.parts[i]:
                new_common = Path(*reference.parts[:i])
                break

        common_parent = new_common

    if makeAbsolute:
        return common_parent.absolute()

    return common_parent


def updateCtxDefaultMap(ctx: click.Context, config: dict[str, Any]) -> None:
    """Update the ``click`` context default map with the provided ``config``"""
    default_map: dict[str, Any] = {}
    if ctx.default_map:
        default_map.update(ctx.default_map)

    default_map.update(config)
    ctx.default_map = default_map
