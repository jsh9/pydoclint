import ast
from typing import List, Optional, Set

from numpydoc.docscrape import NumpyDocString, Parameter

from pydoclint.arg import Arg, ArgList
from pydoclint.method_type import MethodType
from pydoclint.utils import returns
from pydoclint.utils.astTypes import AllFunctionDef
from pydoclint.utils.generic import detectMethodType, isShortDocstring
from pydoclint.violation import Violation


class Visitor(ast.NodeVisitor):
    """A class to recursively visit all the nodes in a parsed module"""

    def __init__(
            self,
            checkTypeHint: bool = True,
            checkArgOrder: bool = True,
            skipCheckingShortDocstrings: bool = True,
    ) -> None:
        self.checkTypeHint: bool = checkTypeHint
        self.checkArgOrder: bool = checkArgOrder
        self.skipCheckingShortDocstrings: bool = skipCheckingShortDocstrings

        self.parent: Optional[ast.AST] = None  # keep track of parent node
        self.violations: List[Violation] = []

    def visit_ClassDef(self, node: ast.ClassDef):  # noqa: D102
        currentParent = self.parent  # keep aside
        self.parent = node

        self.generic_visit(node)

        self.parent = currentParent  # restore

    def visit_FunctionDef(self, node: AllFunctionDef):  # noqa: D102
        currentParent = self.parent  # keep aside
        self.parent = node

        docstring_: Optional[str] = ast.get_docstring(node)
        docstring: str = '' if docstring_ is None else docstring_

        argViolations: List[Violation]
        returnViolations: List[Violation]

        if docstring == '':
            # We don't check functions without docstrings.
            # We defer to
            # flake8-docstrings (https://github.com/PyCQA/flake8-docstrings)
            # or pydocstyle (https://www.pydocstyle.org/en/stable/)
            # to determine whether a function needs a docstring.
            argViolations = []
            returnViolations = []
        else:
            # Note: a NumpyDocString object has the following sections:
            # *  {'Signature': '', 'Summary': [''], 'Extended Summary': [],
            # *  'Parameters': [], 'Returns': [], 'Yields': [], 'Receives': [],
            # *  'Raises': [], 'Warns': [], 'Other Parameters': [],
            # *  'Attributes': [], 'Methods': [], 'See Also': [], 'Notes': [],
            # *  'Warnings': [], 'References': '', 'Examples': '', 'index': {}}
            docStruct: NumpyDocString = NumpyDocString(docstring)

            isShort: bool = isShortDocstring(docStruct)
            if self.skipCheckingShortDocstrings and isShort:
                argViolations = []
                returnViolations = []
            else:
                argViolations = self.checkArguments(
                    node, currentParent, docStruct
                )
                if docstring == '':
                    returnViolations = []
                else:
                    returnViolations = self.checkReturns(node, docStruct)

        self.violations.extend(argViolations)
        self.violations.extend(returnViolations)

        self.generic_visit(node)

        self.parent = currentParent  # restore

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):  # noqa: D102
        # Treat async functions similarly to regular ones
        self.visit_FunctionDef(node)

    def visit_Raise(self, node: ast.Raise):  # noqa: D102
        self.generic_visit(node)

    def checkArguments(
            self,
            node: AllFunctionDef,
            parent_: ast.AST,
            docstringStruct: NumpyDocString,
    ) -> List[Violation]:
        """
        Check input arguments of the function.

        Parameters
        ----------
        node : AllFunctionDef
            The current function node.  It can be a regular function
            or an async function.
        parent_ : ast.AST
            The parent of the current node, which can be another function,
            a class, etc.
        docstringStruct : NumpyDocString
            The parsed docstring structure.

        Returns
        -------
        List[Violation]
            A list of argument violations
        """
        argList: List[ast.arg] = list(node.args.args)

        if isinstance(parent_, ast.ClassDef):
            mType: MethodType = detectMethodType(node)
            if mType in {MethodType.INSTANCE_METHOD, MethodType.CLASS_METHOD}:
                argList = argList[1:]  # no need to document `self` and `cls`

        docArgList: List[Parameter] = docstringStruct.get('Parameters', [])
        return self.validateDocArgs(docArgList, argList, node)

    def validateDocArgs(
            self,
            docArgList: List[Parameter],
            actualArgs: List[ast.arg],
            node: AllFunctionDef,
    ) -> List[Violation]:
        """
        Validate the argument list in the docstring against the "actual"
        arguments (the argument list in the function signature).

        Parameters
        ----------
        docArgList : List[Parameter]
            The argument list from the docstring
        actualArgs : List[ast.arg]
            The argument list from the function signature
        node : AllFunctionDef
            The current function node

        Returns
        -------
        List[Violation]
            A list of argument violations. It can be empty.
        """
        functionName: str = node.name
        lineNum: int = node.lineno

        fnNameMsg = f'Function `{functionName}`:'

        v101 = Violation(code=101, line=lineNum, msgPrefix=fnNameMsg)
        v102 = Violation(code=102, line=lineNum, msgPrefix=fnNameMsg)
        v104 = Violation(code=104, line=lineNum, msgPrefix=fnNameMsg)
        v105 = Violation(code=105, line=lineNum, msgPrefix=fnNameMsg)

        docArgs = ArgList([Arg.fromNumpydocParam(_) for _ in docArgList])
        funcArgs = ArgList([Arg.fromAstArg(_) for _ in actualArgs])

        if docArgs.length() == 0 and funcArgs.length() == 0:
            return []

        violations: List[Violation] = []
        if docArgs.length() < funcArgs.length():
            violations.append(v101)

        if docArgs.length() > funcArgs.length():
            violations.append(v102)

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
                violations.append(v104)
            elif docArgs.equals(
                funcArgs,
                checkTypeHint=False,
                orderMatters=self.checkArgOrder,
            ):
                violations.append(v105)
            elif docArgs.equals(
                funcArgs,
                checkTypeHint=False,
                orderMatters=False,
            ):
                violations.append(v104)
                violations.append(v105)
            else:
                argsInFuncNotInDoc: Set[Arg] = funcArgs.subtract(docArgs)
                argsInDocNotInFunc: Set[Arg] = docArgs.subtract(funcArgs)

                msgPostfixParts: List[str] = []
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

                violations.append(
                    Violation(
                        code=103,
                        line=lineNum,
                        msgPrefix=fnNameMsg,
                        msgPostfix=' '.join(msgPostfixParts),
                    )
                )

        return violations

    @classmethod
    def checkReturns(
            cls,
            node: AllFunctionDef,
            nonEmptyDocStruct: NumpyDocString,
    ) -> List[Violation]:
        """Check return statement & return type annotation of this function"""
        msgPrefix: str = f'Function `{node.name}`'
        lineNum: int = node.lineno

        v201 = Violation(code=201, line=lineNum, msgPrefix=msgPrefix)
        v202 = Violation(code=202, line=lineNum, msgPrefix=msgPrefix)

        hasReturnStmt: bool = returns.hasReturnStatements(node)
        hasReturnAnno: bool = returns.hasReturnAnnotation(node)

        docstringHasReturnSection = bool(nonEmptyDocStruct.get('Returns'))

        violations: List[Violation] = []
        if (hasReturnStmt or hasReturnAnno) and not docstringHasReturnSection:
            violations.append(v201)

        if docstringHasReturnSection and not (hasReturnAnno or hasReturnAnno):
            violations.append(v202)

        return violations
