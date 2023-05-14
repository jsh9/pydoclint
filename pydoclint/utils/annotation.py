import ast
from typing import Optional

from pydoclint.utils.astTypes import Annotation


def parseAnnotation(node: Optional[Annotation]) -> Optional[str]:
    """Parse type annotations from argument list or return annotation."""
    if node is None:
        return None

    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Subscript):
        value: str = parseAnnotation(node.value)
        slice_: str = parseAnnotation(node.slice)
        return f'{value}[{slice_}]'

    if isinstance(node, ast.Index):
        return parseAnnotation(node.value)

    if isinstance(node, ast.Tuple):
        return ', '.join(map(parseAnnotation, node.elts))

    if isinstance(node, ast.Constant):
        return str(node.value)

    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return parseAnnotation(node.left) + ' | ' + parseAnnotation(node.right)

    return None
