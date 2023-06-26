import ast
import importlib.metadata as importlib_metadata
from typing import Any, Generator, Tuple

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
            '--style',
            action='store',
            default='numpy',
            parse_from_config=True,
            help='Which style of docstring is your code base using',
        )
        parser.add_option(
            '-ths',
            '--type-hints-in-signature',
            action='store',
            default='True',
            parse_from_config=True,
            help='Whether to require type hints in function signatures',
        )
        parser.add_option(
            '-thd',
            '--type-hints-in-docstring',
            action='store',
            default='True',
            parse_from_config=True,
            help='Whether to require type hints in the argument list in docstrings',
        )
        parser.add_option(
            '-ao',
            '--check-arg-order',
            action='store',
            default='True',
            parse_from_config=True,
            help=(
                'Whether to check argument orders in the docstring'
                ' against the argument list in the function signature'
            ),
        )
        parser.add_option(
            '-scsd',
            '--skip-checking-short-docstrings',
            action='store',
            default='True',
            parse_from_config=True,
            help='If True, skip checking if the docstring only has a short summary.',
        )
        parser.add_option(
            '-scr',
            '--skip-checking-raises',
            action='store',
            default='False',
            parse_from_config=True,
            help='If True, skip checking docstring "Raises" section against "raise" statements',
        )
        parser.add_option(
            '-aid',
            '--allow-init-docstring',
            action='store',
            default='False',
            parse_from_config=True,
            help='If True, allow both __init__() and the class def to have docstrings',
        )
        parser.add_option(
            '-rrs',
            '--require-return-section-when-returning-none',
            action='store',
            default='False',
            parse_from_config=True,
            help=(
                'If False, a return section is not needed in docstring if'
                ' the function body does not have a "return" statement and'
                ' the return type annotation is "-> None".'
            ),
        )
        parser.add_option(
            '-crt',
            '--check-return-types',
            action='store',
            default='True',
            parse_from_config=True,
            help=(
                'If True, check that the type(s) in the docstring return section and'
                ' the return annotation in the function signature are consistent'
            ),
        )

    @classmethod
    def parse_options(cls, options):  # noqa: D102
        cls.type_hints_in_signature = options.type_hints_in_signature
        cls.type_hints_in_docstring = options.type_hints_in_docstring
        cls.check_arg_order = options.check_arg_order
        cls.skip_checking_short_docstrings = (
            options.skip_checking_short_docstrings
        )
        cls.skip_checking_raises = options.skip_checking_raises
        cls.allow_init_docstring = options.allow_init_docstring
        cls.require_return_section_when_returning_none = (
            options.require_return_section_when_returning_none
        )
        cls.style = options.style

    def run(self) -> Generator[Tuple[int, int, str, Any], None, None]:
        """Run the linter and yield the violation information"""
        typeHintsInSignature = self._bool(
            '--type-hints-in-signature',
            self.type_hints_in_signature,
        )
        typeHintsInDocstring = self._bool(
            '--type-hints-in-docstring',
            self.type_hints_in_docstring,
        )
        checkArgOrder = self._bool('--check-arg-order', self.check_arg_order)
        skipCheckingShortDocstrings = self._bool(
            '--skip-checking-short-docstrings',
            self.skip_checking_short_docstrings,
        )
        skipCheckingRaises = self._bool(
            '--skip-checking-raises',
            self.skip_checking_raises,
        )
        allowInitDocstring = self._bool(
            '--allow-init-docstring',
            self.allow_init_docstring,
        )
        requireReturnSectionWhenReturningNone = self._bool(
            '--require-return-section-when-returning-none',
            self.require_return_section_when_returning_none,
        )

        if self.style not in {'numpy', 'google'}:
            raise ValueError(
                'Invalid value for "--style": must be "numpy" or "google"'
            )

        v = Visitor(
            typeHintsInSignature=typeHintsInSignature,
            typeHintsInDocstring=typeHintsInDocstring,
            checkArgOrder=checkArgOrder,
            skipCheckingShortDocstrings=skipCheckingShortDocstrings,
            skipCheckingRaises=skipCheckingRaises,
            allowInitDocstring=allowInitDocstring,
            requireReturnSectionWhenReturningNone=requireReturnSectionWhenReturningNone,
            style=self.style,
        )
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
