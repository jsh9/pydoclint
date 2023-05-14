import ast
import importlib.metadata as importlib_metadata
from typing import Any, Generator

from pydoclint.visitor import Visitor


class Plugin:
    """Flake8 plugin entry point"""

    name = 'pydoclint'
    version = importlib_metadata.version(name)

    def __init__(self, tree: ast.AST) -> None:
        self._tree = tree

    @classmethod
    def add_options(cls, parser):  # noqa: D102
        parser.add_option(
            '-th',
            '--check-type-hint',
            action='store',
            default='True',
            help='Whether to check type hints in the docstring',
        )
        parser.add_option(
            '-ao',
            '--check-arg-order',
            action='store',
            default='True',
            help=(
                'Whether to check argument orders in the docstring'
                ' against the argument list in the function signature'
            ),
        )

    @classmethod
    def parse_options(cls, options):  # noqa: D102
        cls.check_type_hint = options.check_type_hint
        cls.check_arg_order = options.check_arg_order

    def run(self) -> Generator[tuple[int, int, str, Any], None, None]:
        """Run the linter and yield the violation information"""
        checkTypeHint = self._bool('--check-type-hint', self.check_type_hint)
        checkArgOrder = self._bool('--check-arg-order', self.check_arg_order)

        v = Visitor(checkTypeHint=checkTypeHint, checkArgOrder=checkArgOrder)
        v.visit(self._tree)
        violationInfo = [_.getInfoForFlake8() for _ in v.violations]
        for line, colOffset, msg in violationInfo:
            yield line, colOffset, msg, type(self)

    @classmethod
    def _bool(cls, optionName: str, optionValue: str) -> bool:
        if optionValue == 'True':
            return True

        if optionValue == 'False':
            return False

        raise ValueError(f'Invalid argument value: {optionName}={optionValue}')
