import ast

AllFunctionDef = ast.AsyncFunctionDef | ast.FunctionDef
FunctionOrClassDef = ast.AsyncFunctionDef | ast.FunctionDef | ast.ClassDef
Block = ast.If | ast.While | ast.For | ast.AsyncFor | ast.With | ast.AsyncWith
Annotation = (
    ast.Name | ast.Subscript | ast.Index | ast.Tuple | ast.Constant | ast.BinOp
)
