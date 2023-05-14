import ast

from pydoclint.utils import walk
from pydoclint.utils.astTypes import AllFunctionDef, Block
from pydoclint.utils.generic import getFunctionId


def hasReturnAnnotation(node: AllFunctionDef) -> bool:
    """Check whether the function node has a return type annotation"""
    return node.returns is not None


def hasReturnStatements(node: AllFunctionDef) -> bool:
    """Check whether the function node has any return statements"""
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
