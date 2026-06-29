from __future__ import annotations

import ast
import json

from pydoclint.utils.edge_case_error import EdgeCaseError
from pydoclint.utils.generic import stripQuotes
from pydoclint.utils.unparser_custom import unparseName

MIN_TUPLE_ANNOTATION_LENGTH = len('tuple[]')  # shortest valid tuple annotation


class ReturnAnnotation:
    """A class to hold the return annotation in a function's signature"""

    def __init__(self, annotation: str | None) -> None:
        self.annotation: str | None = stripQuotes(annotation)

    def __str__(self) -> str:
        return f'ReturnAnnotation(annotation={json.dumps(self.annotation)})'

    def __repr__(self) -> str:
        return self.__str__()

    def decompose(self) -> list[str]:
        """
        Numpy style allows decomposing the returning tuple into individual
        element.  For example, if the return annotation is ``Tuple[int,
        bool]``, you can put 2 return values in the return section: int, and
        bool.

        This method decomposes such return annotation into individual elements.

        Returns
        -------
        list[str]
            The decomposed element

        Raises
        ------
        EdgeCaseError
            When the annotation string has strange values
        """
        if self._isTuple():
            assert self.annotation is not None  # narrow type for static checkers

            if not self.annotation.endswith(']'):
                raise EdgeCaseError('Return annotation not ending with `]`')

            if len(self.annotation) < MIN_TUPLE_ANNOTATION_LENGTH:
                raise EdgeCaseError(f'Impossible annotation {self.annotation}')

            if self.annotation.lower() == 'tuple[]':
                return []

            insideTuple: str = self.annotation[6:-1]
            if insideTuple.endswith('...'):  # like this: Tuple[int, ...]
                # because we don't know the tuple's length
                return [self.annotation]

            parsedBody0 = ast.parse(insideTuple).body[0]
            assert isinstance(parsedBody0, ast.Expr), "Shouldn't have happened"

            if isinstance(
                parsedBody0.value, (ast.Attribute, ast.Name)
            ):  # such as Tuple[int]
                return [insideTuple]

            if isinstance(
                parsedBody0.value, ast.Tuple
            ):  # like Tuple[int, str]
                elts: list[ast.expr] = parsedBody0.value.elts
                return [unparseName(_) for _ in elts]

            raise EdgeCaseError('decompose(): This should not have happened')

        return self.putAnnotationInList()

    def _isTuple(self) -> bool:
        try:
            assert self.annotation is not None  # narrow type for static checkers
            parsedBody0 = ast.parse(self.annotation).body[0]
            if not isinstance(parsedBody0, ast.Expr):
                return False

            parsedValue = parsedBody0.value
            if not isinstance(parsedValue, ast.Subscript):
                return False

            parsedValueName = parsedValue.value
            if not isinstance(parsedValueName, ast.Name):
                return False

            annoHead = parsedValueName.id
        except (TypeError, IndexError, AssertionError):
            return False
        else:
            return annoHead in {'tuple', 'Tuple'}

    def putAnnotationInList(self) -> list[str]:
        """Put annotation string in a list"""
        return [] if self.annotation is None else [self.annotation]
