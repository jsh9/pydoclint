import ast

from numpydoc.docscrape import NumpyDocString, Parameter

from pydoclint.arg import Arg, ArgList
from pydoclint.violation import Violation
from pydoclint.method_type import MethodType
from pydoclint.utils import returns
from pydoclint.utils import generic
from pydoclint.utils.astTypes import AllFunctionDef


class Visitor(ast.NodeVisitor):
    def __init__(
            self,
            checkTypeHint: bool,
            checkArgOrder: bool,
    ) -> None:
        self.checkTypeHint: bool = checkTypeHint
        self.checkArgOrder: bool = checkArgOrder

        self.parent: ast.AST | None = None  # keep track of parent node
        self.violations: list[Violation] = []

    def visit_ClassDef(self, node: ast.ClassDef):
        currentParent = self.parent  # keep aside
        self.parent = node

        self.generic_visit(node)

        self.parent = currentParent  # restore

    def visit_FunctionDef(self, node: AllFunctionDef):
        currentParent = self.parent  # keep aside
        self.parent = node

        docstring_: str | None = ast.get_docstring(node)
        docstring: str = '' if docstring_ is None else docstring_
        docStruct: NumpyDocString = NumpyDocString(docstring)

        argViolations = self.checkArguments(node, currentParent, docStruct)

        if docstring == '':
            returnViolations = []
        else:
            returnViolations = self.checkReturns(node, docStruct)

        self.violations.extend(argViolations)
        self.violations.extend(returnViolations)

        self.generic_visit(node)

        self.parent = currentParent  # restore

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        # Treat async functions similarly to regular ones
        self.visit_FunctionDef(node)

    def visit_Raise(self, node: ast.Raise):
        # print(f"Raises: {ast.unparse(node.exc)}\n")
        self.generic_visit(node)

    def checkArguments(
            self,
            node: ast.FunctionDef,
            parent_: ast.AST,
            docstringStruct: NumpyDocString,
    ) -> list[Violation]:
        argList: list[ast.arg] = [arg for arg in node.args.args]

        if isinstance(parent_, ast.ClassDef):
            mType: MethodType = generic.detectMethodType(node)
            if mType in {MethodType.INSTANCE_METHOD, MethodType.CLASS_METHOD}:
                argList = argList[1:]  # no need to document `self` and `cls`

        isDunderFunc: bool = node.name.startswith('__')
        isPrivateFunc: bool = not isDunderFunc and node.name.startswith('_')

        if not node.body or not isinstance(node.body[0], ast.Expr):
            # We don't check functions without docstrings.
            # We defer to
            # flake8-docstrings (https://github.com/PyCQA/flake8-docstrings)
            # or pydocstyle (https://www.pydocstyle.org/en/stable/)
            # to determine whether a function needs a docstring.
            return []

        docArgList: list[Parameter] = docstringStruct.get('Parameters', [])
        return self.validateDocArgList(docArgList, argList, node.name)

    def validateDocArgList(
            self,
            docArgList: list[Parameter],
            actualArgs: list[ast.arg],
            functionName: str,
    ) -> list[Violation]:
        fnNameMsg = f'Function: {functionName}.'

        docArgs = ArgList([Arg.fromNumpydocParam(_) for _ in docArgList])
        funcArgs = ArgList([Arg.fromAstArg(_) for _ in actualArgs])

        if docArgs.length() == 0 and funcArgs.length() == 0:
            return []

        violations: list[Violation] = []
        if docArgs.length() < funcArgs.length():
            violations.append(Violation(101, msgPrefix=fnNameMsg))

        if docArgs.length() > funcArgs.length():
            violations.append(Violation(102, msgPrefix=fnNameMsg))

        if not docArgs.equals(
            funcArgs,
            checkTypeHint=self.checkTypeHint,
            orderMatters=self.checkArgOrder,
        ):
            if docArgs.equals(
                funcArgs,
                checkTypeHint=self.checkTypeHint,
                orderMatters=False,
            ):
                violations.append(Violation(104, msgPrefix=fnNameMsg))
            elif docArgs.equals(
                funcArgs,
                checkTypeHint=False,
                orderMatters=self.checkArgOrder,
            ):
                violations.append(Violation(105, msgPrefix=fnNameMsg))
            elif docArgs.equals(
                funcArgs,
                checkTypeHint=False,
                orderMatters=False,
            ):
                violations.append(Violation(104, msgPrefix=fnNameMsg))
                violations.append(Violation(105, msgPrefix=fnNameMsg))
            else:
                argsInFuncNotInDoc: set[Arg] = funcArgs.subtract(docArgs)
                argsInDocNotInFunc: set[Arg] = docArgs.subtract(funcArgs)

                msgPostfixParts: list[str] = []
                if argsInFuncNotInDoc:
                    msgPostfixParts.append(
                        'Arguments in the function signature but not in the'
                        f' docstring: {sorted(argsInFuncNotInDoc)}.'
                    )

                if argsInDocNotInFunc:
                    msgPostfixParts.append(
                        'Arguments in the docstring but not in the function'
                        f' signature: {sorted(argsInDocNotInFunc)}.'
                    )

                msgPostfix: str = ' '.join(msgPostfixParts)

                violations.append(
                    Violation(103, msgPrefix=fnNameMsg, msgPostfix=msgPostfix)
                )

        return violations

    @classmethod
    def checkReturns(
            cls,
            node: AllFunctionDef,
            nonEmptyDocStruct: NumpyDocString,
    ) -> list[Violation]:
        msgPrefix: str = f'Function "{node.name}"'

        hasReturnStmt: bool = returns.hasReturnStatements(node)
        hasReturnAnno: bool = returns.hasReturnAnnotation(node)

        docstringHasReturnSection = bool(nonEmptyDocStruct.get('Returns'))

        violations: list[Violation] = []
        if (hasReturnStmt or hasReturnAnno) and not docstringHasReturnSection:
            violations.append(Violation(201, msgPrefix=msgPrefix))

        if docstringHasReturnSection and not (hasReturnAnno or hasReturnAnno):
            violations.append(Violation(202, msgPrefix=msgPrefix))

        return violations
