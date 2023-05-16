import ast
from typing import Union

FuncOrAsyncFuncDef = Union[ast.AsyncFunctionDef, ast.FunctionDef]
ClassOrFunctionDef = Union[ast.ClassDef, ast.AsyncFunctionDef, ast.FunctionDef]
BlockType = (ast.If, ast.While, ast.For, ast.AsyncFor, ast.With, ast.AsyncWith)
AnnotationType = Union[
    ast.Name,
    ast.Subscript,
    ast.Index,
    ast.Tuple,
    ast.Constant,
    ast.BinOp,
    ast.Attribute,
]
