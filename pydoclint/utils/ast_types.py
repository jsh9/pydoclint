from __future__ import annotations

import ast
import sys

FuncOrAsyncFuncDef = ast.AsyncFunctionDef | ast.FunctionDef
ClassOrFunctionDef = ast.ClassDef | ast.AsyncFunctionDef | ast.FunctionDef

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

if sys.version_info >= (3, 11):
    BlockType = (*LegacyBlockTypes, ast.match_case, ast.TryStar)
else:  # Python 3.10 only, because this project doesn't support Python 3.9
    BlockType = (*LegacyBlockTypes, ast.match_case)
