import ast
from typing import List

from pydoclint.utils.internal_error import InternalError
from pydoclint.utils.annotation import unparseAnnotation


class ReturnAnnotation:
    """A class to hold the return annotation in a function's signature"""
    def __init__(self, annotation: str) -> None:
        self.annotation = annotation

    def isTuple(self) -> bool:
        return self.annotation.lower().startswith('tuple[')

    def decompose(self) -> List[str]:
        if self.isTuple():
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
            return [self.annotation]
