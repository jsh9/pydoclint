import ast
import sys
from typing import Union

FuncOrAsyncFuncDef = Union[ast.AsyncFunctionDef, ast.FunctionDef]
ClassOrFunctionDef = Union[ast.ClassDef, ast.AsyncFunctionDef, ast.FunctionDef]
AnnotationType = Union[
    ast.Name,
    ast.Subscript,
    ast.Index,
    ast.Tuple,
    ast.Constant,
    ast.BinOp,
    ast.Attribute,
]

LegacyBlockTypes = [
    ast.If,
    ast.While,
    ast.For,
    ast.AsyncFor,
    ast.With,
    ast.AsyncWith,
    ast.Try,
    ast.ExceptHandler,
]

if sys.version_info < (3, 10):
    BlockType = tuple(LegacyBlockTypes)
elif sys.version_info < (3, 11):
    BlockType = tuple(LegacyBlockTypes + [ast.match_case])
else:
    BlockType = tuple(LegacyBlockTypes + [ast.match_case, ast.TryStar])
