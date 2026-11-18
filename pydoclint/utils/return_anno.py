from __future__ import annotations

import ast
import json

from pydoclint.utils.generic import stripBacktickWrapper, stripQuotes
from pydoclint.utils.unparser_custom import unparseName


def _parseAnnotationExpr(text: str) -> ast.expr | None:
    # Unwrap outer string quotes when the whole return annotation is a string
    # forward reference (such as `'tuple[int, str]'`).
    try:
        expr: ast.expr = ast.parse(text, mode='eval').body
    except (SyntaxError, ValueError):
        return None

    if isinstance(expr, ast.Constant) and isinstance(expr.value, str):
        try:
            expr = ast.parse(expr.value.strip(), mode='eval').body
        except (SyntaxError, ValueError):
            return None

    return expr


class ReturnAnnotation:
    """A class to hold the return annotation in a function's signature"""

    def __init__(self, annotation: str | None) -> None:
        self._rawAnnotation: str | None = annotation
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
        """
        tupleSubscript: ast.Subscript | None = self._parseTupleSubscript()
        if tupleSubscript is None:
            return self.putAnnotationInList()

        sliceExpr: ast.expr = tupleSubscript.slice
        if isinstance(sliceExpr, ast.Constant) and sliceExpr.value is Ellipsis:
            return self.putAnnotationInList()

        if isinstance(sliceExpr, ast.Tuple):
            elts: list[ast.expr] = sliceExpr.elts
            if (
                len(elts) > 0
                and isinstance(elts[-1], ast.Constant)
                and elts[-1].value is Ellipsis
            ):
                # Variadic tuple such as `Tuple[int, ...]`: length is unknown
                return self.putAnnotationInList()

            return [stripQuotes(unparseName(_)) for _ in elts]

        return [stripQuotes(unparseName(sliceExpr))]

    def _isTuple(self) -> bool:
        return self._parseTupleSubscript() is not None

    def _parseTupleSubscript(self) -> ast.Subscript | None:
        if self._rawAnnotation is None:
            return None

        unwrapped: str = stripBacktickWrapper(self._rawAnnotation).strip()
        if unwrapped == '':
            return None

        expr: ast.expr | None = _parseAnnotationExpr(unwrapped)
        if expr is None and self.annotation is not None:
            expr = _parseAnnotationExpr(self.annotation.strip())

        if not isinstance(expr, ast.Subscript):
            return None

        subscriptHead: ast.expr = expr.value
        if isinstance(subscriptHead, ast.Name):
            # Only top-level tuple/Tuple annotations are decomposed here.
            isTupleHead: bool = subscriptHead.id in {'tuple', 'Tuple'}
        elif isinstance(subscriptHead, ast.Constant) and isinstance(
            subscriptHead.value, str
        ):
            # Handles stringified head such as `'tuple'[int, int, str]`
            isTupleHead = subscriptHead.value in {'tuple', 'Tuple'}
        else:
            isTupleHead = False

        return expr if isTupleHead else None

    def putAnnotationInList(self) -> list[str]:
        """Put annotation string in a list"""
        return [] if self.annotation is None else [self.annotation]
