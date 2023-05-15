import ast
from typing import Union

AllFunctionDef = Union[ast.AsyncFunctionDef, ast.FunctionDef]
ClassOrFunctionDef = Union[ast.ClassDef, ast.AsyncFunctionDef, ast.FunctionDef]
Block = (ast.If, ast.While, ast.For, ast.AsyncFor, ast.With, ast.AsyncWith)
Annotation = Union[
    ast.Name, ast.Subscript, ast.Index, ast.Tuple, ast.Constant, ast.BinOp
]
