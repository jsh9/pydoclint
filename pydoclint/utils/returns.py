import ast

from pydoclint.utils import walk
from pydoclint.utils.generic import getFunctionId
from pydoclint.utils.astTypes import AllFunctionDef, Block


def hasReturnAnnotation(node: AllFunctionDef) -> bool:
    return node.returns is not None


def hasReturnStatements(node: AllFunctionDef) -> bool:
    thisId = getFunctionId(node)
    for child, parent in walk.walk(node):
        if isinstance(child, ast.Return):
            if isinstance(parent, AllFunctionDef):
                # Only return True if the parent is `node` (in other words, if
                # this return statement doesn't come from a nested function)
                parentId = getFunctionId(parent)
                if thisId == parentId:
                    return True

            if isinstance(parent, Block):
                return True

    return False
