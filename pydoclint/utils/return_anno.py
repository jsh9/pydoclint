import ast
from typing import List, Optional

from pydoclint.utils.annotation import unparseAnnotation
from pydoclint.utils.internal_error import InternalError


class ReturnAnnotation:
    """A class to hold the return annotation in a function's signature"""

    def __init__(self, annotation: Optional[str]) -> None:
        self.annotation = annotation

    def decompose(self) -> List[str]:
        """
        Numpy style allows decomposing the returning tuple into individual
        element.  For example, if the return annotation is `Tuple[int, bool]`,
        you can put 2 return values in the return section: int, and bool.

        This method decomposes such return annotation into individual elements.

        Returns
        -------
        List[str]
            The decomposed element

        Raises
        ------
        InternalError
            When the annotation string has strange values
        """
        if self._isTuple():  # noqa: R506
            if not self.annotation.endswith(']'):
                raise InternalError('Return annotation not ending with `]`')

            if len(self.annotation) < 7:
                raise InternalError(f'Impossible annotation {self.annotation}')

            if self.annotation.lower() == 'tuple[]':
                return []

            insideTuple: str = self.annotation[6:-1]
            if insideTuple.endswith('...'):  # like this: Tuple[int, ...]
                return [self.annotation]  # b/c we don't know the tuple's length

            parsedBody0: ast.Expr = ast.parse(insideTuple).body[0]
            if isinstance(parsedBody0.value, ast.Name):  # like this: Tuple[int]
                return [insideTuple]

            if isinstance(parsedBody0.value, ast.Tuple):  # like Tuple[int, str]
                elts: List = parsedBody0.value.elts
                return [unparseAnnotation(_) for _ in elts]

            raise InternalError('decompose(): This should not have happened')
        else:
            return self.putAnnotationInList()

    def _isTuple(self) -> bool:
        return (
            self.annotation is not None
            and self.annotation.lower().startswith('tuple[')
        )

    def putAnnotationInList(self) -> List[str]:
        """Put annotation string in a list"""
        return [] if self.annotation is None else [self.annotation]
