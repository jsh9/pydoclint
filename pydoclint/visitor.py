import ast
from typing import List, Optional, Set

from pydoclint.utils.arg import Arg, ArgList
from pydoclint.utils.astTypes import FuncOrAsyncFuncDef
from pydoclint.utils.doc import Doc
from pydoclint.utils.generic import (
    collectFuncArgs,
    detectMethodType,
    generateMsgPrefix,
    getDocstring,
    isPropertyMethod,
)
from pydoclint.utils.internal_error import InternalError
from pydoclint.utils.method_type import MethodType
from pydoclint.utils.return_yield_raise import (
    hasGeneratorAsReturnAnnotation,
    hasRaiseStatements,
    hasReturnAnnotation,
    hasReturnStatements,
    hasYieldStatements,
    isReturnAnnotationNone,
)
from pydoclint.utils.violation import Violation


class Visitor(ast.NodeVisitor):
    """A class to recursively visit all the nodes in a parsed module"""

    def __init__(
            self,
            style: str = 'numpy',
            checkTypeHint: bool = True,
            checkArgOrder: bool = True,
            skipCheckingShortDocstrings: bool = True,
            skipCheckingRaises: bool = False,
            allowInitDocstring: bool = False,
            requireReturnSectionWhenReturningNone: bool = False,
    ) -> None:
        self.style: str = style
        self.checkTypeHint: bool = checkTypeHint
        self.checkArgOrder: bool = checkArgOrder
        self.skipCheckingShortDocstrings: bool = skipCheckingShortDocstrings
        self.skipCheckingRaises: bool = skipCheckingRaises
        self.allowInitDocstring: bool = allowInitDocstring
        self.requireReturnSectionWhenReturningNone: bool = (
            requireReturnSectionWhenReturningNone
        )

        self.parent: Optional[ast.AST] = None  # keep track of parent node
        self.violations: List[Violation] = []

    def visit_ClassDef(self, node: ast.ClassDef):  # noqa: D102
        currentParent = self.parent  # keep aside
        self.parent = node

        self.generic_visit(node)

        self.parent = currentParent  # restore

    def visit_FunctionDef(self, node: FuncOrAsyncFuncDef):  # noqa: D102
        parent_ = self.parent  # keep aside
        self.parent = node

        isClassConstructor: bool = node.name == '__init__' and isinstance(
            parent_, ast.ClassDef
        )

        docstring: str = getDocstring(node)

        if isClassConstructor:
            docstring = self._checkClassConstructorDocstrings(
                node=node,
                parent_=parent_,
                initDocstring=docstring,
            )

        argViolations: List[Violation]
        returnViolations: List[Violation]
        yieldViolations: List[Violation]
        raiseViolations: List[Violation]

        if docstring == '':
            # We don't check functions without docstrings.
            # We defer to
            # flake8-docstrings (https://github.com/PyCQA/flake8-docstrings)
            # or pydocstyle (https://www.pydocstyle.org/en/stable/)
            # to determine whether a function needs a docstring.
            argViolations = []
            returnViolations = []
            yieldViolations = []
            raiseViolations = []
        else:
            try:
                doc: Doc = Doc(docstring=docstring, style=self.style)
            except Exception as excp:
                doc = Doc(docstring='', style=self.style)
                self.violations.append(
                    Violation(
                        code=1,
                        line=node.lineno,
                        msgPrefix=f'Function/method `{node.name}`:',
                        msgPostfix=str(excp).replace('\n', ' '),
                    )
                )

            isShort: bool = doc.isShortDocstring
            if self.skipCheckingShortDocstrings and isShort:
                argViolations = []
                returnViolations = []
                yieldViolations = []
                raiseViolations = []
            else:
                argViolations = self.checkArguments(node, parent_, doc)
                if docstring == '':
                    returnViolations = []
                    yieldViolations = []
                    raiseViolations = []
                else:
                    returnViolations = self.checkReturns(node, parent_, doc)
                    yieldViolations = self.checkYields(node, parent_, doc)
                    if not self.skipCheckingRaises:
                        raiseViolations = self.checkRaises(node, parent_, doc)
                    else:
                        raiseViolations = []

            if isClassConstructor:
                # Re-check return violations because the rules are
                # different for class constructors.
                returnViolations = (
                    self.checkReturnsAndYieldsInClassConstructor(
                        parent=parent_, doc=doc
                    )
                )

        self.violations.extend(argViolations)
        self.violations.extend(returnViolations)
        self.violations.extend(yieldViolations)
        self.violations.extend(raiseViolations)

        self.generic_visit(node)

        self.parent = parent_  # restore

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):  # noqa: D102
        # Treat async functions similarly to regular ones
        self.visit_FunctionDef(node)

    def visit_Raise(self, node: ast.Raise):  # noqa: D102
        self.generic_visit(node)

    def _checkClassConstructorDocstrings(  # noqa: C901
            self,
            node: FuncOrAsyncFuncDef,
            parent_: ast.ClassDef,
            initDocstring: str,
    ) -> str:
        """
        Check class docstring and __init__() docstring.

        If only class docstring exists, or if __init__() is not allowed to have
        its own docstring, return the class docstring for further checking.

        Otherwise, return the __init__() docstring for further checking.
        """
        if not isinstance(parent_, ast.ClassDef):
            msg = (
                'This should not have happened; please contact the authors'
                ' and share the full call stack.'
            )
            raise InternalError(msg)

        className: str = parent_.name
        classLineNum: int = parent_.lineno

        classDocstring: str = getDocstring(parent_)

        if len(initDocstring) == 0:  # __init__() doesn't have its own docstring
            # Check class docstring instead, because that's what we care
            # about when checking the class constructor.
            return classDocstring

        # Below: __init__() has its own docstring
        if not self.allowInitDocstring:
            self.violations.append(
                Violation(
                    code=301,
                    line=node.lineno,
                    msgPrefix=f'Class `{className}`:',
                )
            )
            return classDocstring

        # Below: __init__() is allowed to have a separate docstring
        try:
            classDoc = Doc(docstring=classDocstring, style=self.style)
        except Exception as excp:
            classDoc = Doc(docstring='', style=self.style)
            self.violations.append(
                Violation(
                    code=1,
                    line=parent_.lineno,
                    msgPrefix=f'Class `{className}`:',
                    msgPostfix=str(excp).replace('\n', ' '),
                )
            )

        try:
            initDoc = Doc(docstring=initDocstring, style=self.style)
        except Exception as excp:
            initDoc = Doc(docstring='', style=self.style)
            self.violations.append(
                Violation(
                    code=1,
                    line=node.lineno,
                    msgPrefix=f'Method `{node.name}`',
                    msgPostfix=str(excp).replace('\n', ' '),
                )
            )

        if classDoc.hasReturnsSection:
            self.violations.append(
                Violation(
                    code=302,
                    line=classLineNum,
                    msgPrefix=f'Class `{className}`:',
                )
            )

        if initDoc.hasReturnsSection:
            self.violations.append(
                Violation(
                    code=303,
                    line=node.lineno,
                    msgPrefix=f'Class `{className}`:',
                )
            )

        if classDoc.argList.nonEmpty:
            self.violations.append(
                Violation(
                    code=304,
                    line=classLineNum,
                    msgPrefix=f'Class `{className}`:',
                )
            )

        if classDoc.hasYieldsSection:
            self.violations.append(
                Violation(
                    code=306,
                    line=classLineNum,
                    msgPrefix=f'Class `{className}`:',
                )
            )

        if initDoc.hasYieldsSection:
            self.violations.append(
                Violation(
                    code=307,
                    line=classLineNum,
                    msgPrefix=f'Class `{className}`:',
                )
            )

        if classDoc.hasRaisesSection:
            self.violations.append(
                Violation(
                    code=305,
                    line=classLineNum,
                    msgPrefix=f'Class `{className}`:',
                )
            )

        return initDocstring

    def checkArguments(  # noqa: C901
            self,
            node: FuncOrAsyncFuncDef,
            parent_: ast.AST,
            doc: Doc,
    ) -> List[Violation]:
        """
        Check input arguments of the function.

        Parameters
        ----------
        node : FuncOrAsyncFuncDef
            The current function node.  It can be a regular function
            or an async function.
        parent_ : ast.AST
            The parent of the current node, which can be another function,
            a class, etc.
        doc : Doc
            The parsed docstring structure.

        Returns
        -------
        List[Violation]
            A list of argument violations
        """
        astArgList: List[ast.arg] = collectFuncArgs(node)

        isMethod: bool = isinstance(parent_, ast.ClassDef)
        msgPrefix: str = generateMsgPrefix(node, parent_, appendColon=True)

        if isMethod:
            mType: MethodType = detectMethodType(node)
            if mType in {MethodType.INSTANCE_METHOD, MethodType.CLASS_METHOD}:
                astArgList = astArgList[1:]  # no need to document self/cls

        lineNum: int = node.lineno
        v101 = Violation(code=101, line=lineNum, msgPrefix=msgPrefix)
        v102 = Violation(code=102, line=lineNum, msgPrefix=msgPrefix)
        v104 = Violation(code=104, line=lineNum, msgPrefix=msgPrefix)
        v105 = Violation(code=105, line=lineNum, msgPrefix=msgPrefix)

        docArgs = doc.argList
        funcArgs = ArgList([Arg.fromAstArg(_) for _ in astArgList])

        if docArgs.length == 0 and funcArgs.length == 0:
            return []

        violations: List[Violation] = []
        if docArgs.length < funcArgs.length:
            violations.append(v101)

        if docArgs.length > funcArgs.length:
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
                        msgPrefix=msgPrefix,
                        msgPostfix=' '.join(msgPostfixParts),
                    )
                )

        return violations

    def checkReturns(
            self,
            node: FuncOrAsyncFuncDef,
            parent: ast.AST,
            doc: Doc,
    ) -> List[Violation]:
        """Check return statement & return type annotation of this function"""
        lineNum: int = node.lineno
        msgPrefix = generateMsgPrefix(node, parent, appendColon=False)

        v201 = Violation(code=201, line=lineNum, msgPrefix=msgPrefix)
        v202 = Violation(code=202, line=lineNum, msgPrefix=msgPrefix)

        hasReturnStmt: bool = hasReturnStatements(node)
        hasReturnAnno: bool = hasReturnAnnotation(node)
        hasGenAsRetAnno: bool = hasGeneratorAsReturnAnnotation(node)

        docstringHasReturnSection: bool = doc.hasReturnsSection

        violations: List[Violation] = []
        if not docstringHasReturnSection and not isPropertyMethod(node):
            if hasReturnStmt or (hasReturnAnno and not hasGenAsRetAnno):
                # If "Generator[...]" is put in the return type annotation,
                # we don't need a "Returns" section in the docstring. Instead,
                # we need a "Yields" section.
                if self.requireReturnSectionWhenReturningNone:
                    violations.append(v201)
                elif not isReturnAnnotationNone(node):
                    violations.append(v201)

        if docstringHasReturnSection and not (hasReturnStmt or hasReturnAnno):
            violations.append(v202)

        return violations

    @classmethod
    def checkReturnsAndYieldsInClassConstructor(
            cls,
            parent: ast.ClassDef,
            doc: Doc,
    ) -> List[Violation]:
        """Check the presence of a Returns/Yields section in class docstring"""
        violations: List[Violation] = []
        if doc.hasReturnsSection:
            violations.append(
                Violation(
                    code=302,
                    line=parent.lineno,
                    msgPrefix=f'Class `{parent.name}`:',
                )
            )

        if doc.hasYieldsSection:
            violations.append(
                Violation(
                    code=306,
                    line=parent.lineno,
                    msgPrefix=f'Class `{parent.name}`:',
                )
            )

        return violations

    @classmethod
    def checkYields(
            cls,
            node: FuncOrAsyncFuncDef,
            parent: ast.AST,
            doc: Doc,
    ) -> List[Violation]:
        """Check violations on 'yield' statements or 'Generator' annotation"""
        violations: List[Violation] = []

        lineNum: int = node.lineno
        msgPrefix = generateMsgPrefix(node, parent, appendColon=False)

        v401 = Violation(code=401, line=lineNum, msgPrefix=msgPrefix)
        v402 = Violation(code=402, line=lineNum, msgPrefix=msgPrefix)
        v403 = Violation(code=403, line=lineNum, msgPrefix=msgPrefix)

        docstringHasYieldsSection: bool = doc.hasYieldsSection

        hasYieldStmt: bool = hasYieldStatements(node)
        hasGenAsRetAnno: bool = hasGeneratorAsReturnAnnotation(node)

        if not docstringHasYieldsSection:
            if hasGenAsRetAnno:
                violations.append(v401)

            if hasYieldStmt:
                violations.append(v402)

        if docstringHasYieldsSection:
            if not hasYieldStmt and not hasGenAsRetAnno:
                violations.append(v403)

        return violations

    @classmethod
    def checkRaises(
            cls,
            node: FuncOrAsyncFuncDef,
            parent: ast.AST,
            doc: Doc,
    ) -> List[Violation]:
        """Check violations on 'raise' statements"""
        violations: List[Violation] = []

        lineNum: int = node.lineno
        msgPrefix = generateMsgPrefix(node, parent, appendColon=False)

        v501 = Violation(code=501, line=lineNum, msgPrefix=msgPrefix)
        v502 = Violation(code=502, line=lineNum, msgPrefix=msgPrefix)

        docstringHasRaisesSection: bool = doc.hasRaisesSection
        hasRaiseStmt: bool = hasRaiseStatements(node)

        if hasRaiseStmt and not docstringHasRaisesSection:
            violations.append(v501)

        if not hasRaiseStmt and docstringHasRaisesSection:
            violations.append(v502)

        return violations
