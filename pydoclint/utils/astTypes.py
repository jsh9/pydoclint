from __future__ import annotations

import ast
import sys
from typing import Union

if sys.version_info < (3, 10):
    # This is because using `|` with `from __future__ import annotations`
    # works in type annotations in Python 3.8 and 3.9, but not 
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
else:
    FuncOrAsyncFuncDef = ast.AsyncFunctionDef | ast.FunctionDef
    ClassOrFunctionDef = ast.ClassDef | ast.AsyncFunctionDef | ast.FunctionDef
    AnnotationType = (
        ast.Name
        | ast.Subscript
        | ast.Index
        | ast.Tuple
        | ast.Constant
        | ast.BinOp
        | ast.Attribute
    )

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
