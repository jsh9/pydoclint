import ast
from typing import List, Optional, Set

from pydoclint.utils.annotation import unparseAnnotation
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
from pydoclint.utils.return_anno import ReturnAnnotation
from pydoclint.utils.return_arg import ReturnArg
from pydoclint.utils.return_yield_raise import (
    hasGeneratorAsReturnAnnotation,
    hasIteratorOrIterableAsReturnAnnotation,
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
            typeHintsInSignature: bool = True,
            typeHintsInDocstring: bool = True,
            checkArgOrder: bool = True,
            skipCheckingShortDocstrings: bool = True,
            skipCheckingRaises: bool = False,
            allowInitDocstring: bool = False,
            checkReturnTypes: bool = True,
            requireReturnSectionWhenReturningNone: bool = False,
    ) -> None:
        self.style: str = style
        self.typeHintsInSignature: bool = typeHintsInSignature
        self.typeHintsInDocstring: bool = typeHintsInDocstring
        self.checkArgOrder: bool = checkArgOrder
        self.skipCheckingShortDocstrings: bool = skipCheckingShortDocstrings
        self.skipCheckingRaises: bool = skipCheckingRaises
        self.allowInitDocstring: bool = allowInitDocstring
        self.checkReturnTypes: bool = checkReturnTypes
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
        v106 = Violation(code=106, line=lineNum, msgPrefix=msgPrefix)
        v107 = Violation(code=107, line=lineNum, msgPrefix=msgPrefix)
        v108 = Violation(code=108, line=lineNum, msgPrefix=msgPrefix)
        v109 = Violation(code=109, line=lineNum, msgPrefix=msgPrefix)
        v110 = Violation(code=110, line=lineNum, msgPrefix=msgPrefix)
        v111 = Violation(code=111, line=lineNum, msgPrefix=msgPrefix)

        docArgs: ArgList = doc.argList
        funcArgs: ArgList = ArgList([Arg.fromAstArg(_) for _ in astArgList])

        if docArgs.length == 0 and funcArgs.length == 0:
            return []

        violations: List[Violation] = []
        if docArgs.length < funcArgs.length:
            violations.append(v101)

        if docArgs.length > funcArgs.length:
            violations.append(v102)

        if self.typeHintsInSignature and funcArgs.noTypeHints():
            violations.append(v106)

        if self.typeHintsInSignature and not funcArgs.hasTypeHintInAllArgs():
            violations.append(v107)

        if not self.typeHintsInSignature and funcArgs.hasTypeHintInAnyArg():
            violations.append(v108)

        if self.typeHintsInDocstring and docArgs.noTypeHints():
            violations.append(v109)

        if self.typeHintsInDocstring and not docArgs.hasTypeHintInAllArgs():
            violations.append(v110)

        if not self.typeHintsInDocstring and docArgs.hasTypeHintInAnyArg():
            violations.append(v111)

        if not docArgs.equals(
            funcArgs,
            checkTypeHint=True,
            orderMatters=self.checkArgOrder,
        ):
            if docArgs.equals(
                funcArgs,
                checkTypeHint=True,
                orderMatters=False,
            ):
                violations.append(v104)
            elif docArgs.equals(
                funcArgs,
                checkTypeHint=False,
                orderMatters=self.checkArgOrder,
            ):
                if self.typeHintsInSignature and self.typeHintsInDocstring:
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

    def checkReturns(  # noqa: C901
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
        v203 = Violation(code=203, line=lineNum, msgPrefix=msgPrefix)

        hasReturnStmt: bool = hasReturnStatements(node)
        hasReturnAnno: bool = hasReturnAnnotation(node)
        hasGenAsRetAnno: bool = hasGeneratorAsReturnAnnotation(node)
        onlyHasYieldStmt: bool = hasYieldStatements(node) and not hasReturnStmt
        hasIterAsRetAnno: bool = hasIteratorOrIterableAsReturnAnnotation(node)

        docstringHasReturnSection: bool = doc.hasReturnsSection

        violations: List[Violation] = []
        if not docstringHasReturnSection and not isPropertyMethod(node):
            if (
                # fmt: off
                not (onlyHasYieldStmt and hasIterAsRetAnno)
                and (hasReturnStmt or (hasReturnAnno and not hasGenAsRetAnno))

                # fmt: on
            ):
                # If "Generator[...]" is put in the return type annotation,
                # we don't need a "Returns" section in the docstring. Instead,
                # we need a "Yields" section.
                if self.requireReturnSectionWhenReturningNone:
                    violations.append(v201)
                elif not isReturnAnnotationNone(node):
                    violations.append(v201)

        if docstringHasReturnSection and not (hasReturnStmt or hasReturnAnno):
            violations.append(v202)

        if self.checkReturnTypes:
            if hasReturnAnno:
                returnAnno = ReturnAnnotation(unparseAnnotation(node.returns))
            else:
                returnAnno = ReturnAnnotation(annotation=None)

            if docstringHasReturnSection:
                returnSec: List[ReturnArg] = doc.returnSection
            else:
                returnSec = []

            if self.style == 'numpy':
                # If the return annotation is a tuple (such as Tuple[int, str]),
                # we consider both in the docstring to be a valid style:
                #
                # Option 1:
                # >    Returns
                # >    -------
                # >    Tuple[int, str]
                # >        ...
                #
                # Option 2:
                # >    Returns
                # >    -------
                # >    int
                # >        ...
                # >    str
                # >        ...
                #
                #  This is why we are comparing both the decomposed annotation
                #  types and the original annotation type
                returnAnnoItems: List[str] = returnAnno.decompose()
                returnAnnoInList: List[str] = returnAnno.putAnnotationInList()

                returnSecTypes: List[str] = [_.argType for _ in returnSec]

                if returnAnnoInList != returnSecTypes:
                    if len(returnAnnoItems) != len(returnSec):
                        msg = f'Return annotation has {len(returnAnnoItems)}'
                        msg += ' type(s); docstring return section has'
                        msg += f' {len(returnSec)} type(s).'
                        violations.append(v203.appendMoreMsg(moreMsg=msg))
                    else:
                        if returnSecTypes != returnAnnoItems:
                            msg1 = (
                                f'Return annotation types: {returnAnnoItems}; '
                            )
                            msg2 = f'docstring return section types: {returnSecTypes}'
                            violations.append(v203.appendMoreMsg(msg1 + msg2))

            else:  # Google style
                # The Google docstring style does not allow (or at least does
                # not encourage) splitting tuple return types (such as
                # Tuple[int, str, bool]) into individual types (int, str, and
                # bool).
                # Therefore, in Google-style docstrings, people should always
                # use one compound style for tuples.

                if len(returnSec) > 0:
                    if returnAnno.annotation is None:
                        msg = 'Return annotation has 0 type(s); docstring'
                        msg += ' return section has 1 type(s).'
                        violations.append(v203.appendMoreMsg(moreMsg=msg))
                    elif returnSec[0].argType != returnAnno.annotation:
                        msg = 'Return annotation types: '
                        msg += str([returnAnno.annotation]) + '; '
                        msg += 'docstring return section types: '
                        msg += str([returnSec[0].argType])
                        violations.append(v203.appendMoreMsg(moreMsg=msg))
                else:
                    if returnAnno.annotation != '':
                        msg = 'Return annotation has 1 type(s); docstring'
                        msg += ' return section has 0 type(s).'
                        violations.append(v203.appendMoreMsg(moreMsg=msg))

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
