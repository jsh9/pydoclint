"""Helper functions to classes/methods in visitor.py"""

from __future__ import annotations

import ast
import re
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from pydoclint.utils.return_anno import ReturnAnnotation
    from pydoclint.utils.return_arg import ReturnArg
    from pydoclint.utils.yield_arg import YieldArg

from pydoclint.utils.arg import Arg, ArgList
from pydoclint.utils.edge_case_error import EdgeCaseError
from pydoclint.utils.generic import (
    NameKind,
    appendArgsToCheckToV105,
    buildClassAttrToDefaultMapping,
    classifyName,
    getDocstring,
    isPlaceholderDefault,
    specialEqual,
    stripBacktickWrapper,
    stripQuotes,
)
from pydoclint.utils.parse_docstring import parseDocstringInGivenStyle
from pydoclint.utils.return_yield_raise import GeneratorAnnotationKind
from pydoclint.utils.special_methods import checkIsPropertyMethod
from pydoclint.utils.unparser_custom import unparseName
from pydoclint.utils.violation import Violation

SPHINX_MSG_POSTFIX: str = (
    ' (Please read'
    ' https://jsh9.github.io/pydoclint/checking_class_attributes.html'
    ' on how to correctly document class attributes.)'
)
GENERATOR_RETURN_TYPE_ARG_INDEX: int = 2
GENERATOR_MAX_ARG_COUNT: int = GENERATOR_RETURN_TYPE_ARG_INDEX + 1
ASYNC_GENERATOR_MAX_ARG_COUNT: int = 2


def checkClassAttributesAgainstClassDocstring(
        *,
        node: ast.ClassDef,
        style: str,
        violations: list[Violation],
        lineNum: int,
        msgPrefix: str,
        shouldCheckArgOrder: bool,
        argTypeHintsInSignature: bool,
        argTypeHintsInDocstring: bool,
        skipCheckingShortDocstrings: bool,
        ignorePrivateClassAttributes: bool,
        ignoreUnderscoreOnlyClassAttributes: bool,
        ignoreSpecialDunderClassAttributes: bool,
        treatPropertyMethodsAsClassAttributes: bool,
        onlyAttrsWithClassVarAreTreatedAsClassAttrs: bool,
        requireInlineClassVarDocs: bool,
        checkArgDefaults: bool,
        isStubFile: bool,
) -> None:
    """
    Check class attribute list against the attribute list in docstring.

    Parameters
    ----------
    node : ast.ClassDef
        The class definition node.
    style : str
        The docstring style.
    violations : list[Violation]
        The list of violations.
    lineNum : int
        The line number for reporting violations.
    msgPrefix : str
        The message prefix for violations.
    shouldCheckArgOrder : bool
        Whether to check the order of arguments.
    argTypeHintsInSignature : bool
        Whether type hints are in the function signature.
    argTypeHintsInDocstring : bool
        Whether to include type hints in docstring.
    skipCheckingShortDocstrings : bool
        Whether to skip checking short docstrings.
    ignorePrivateClassAttributes : bool
        Whether to ignore private class attributes (such as ``_value``) when
        checking the docstring. Ignored attributes must not appear in the
        docstring.
    ignoreUnderscoreOnlyClassAttributes : bool
        Whether to ignore class attributes with underscore-only names (such as
        ``_``) when checking the docstring. Ignored attributes must not appear
        in the docstring.
    ignoreSpecialDunderClassAttributes : bool
        Whether to ignore class attributes with special dunder names (such as
        ``__slots__``) when checking the docstring. Ignored attributes must not
        appear in the docstring.
    treatPropertyMethodsAsClassAttributes : bool
        Whether to treat property methods as class attributes.
    onlyAttrsWithClassVarAreTreatedAsClassAttrs : bool
        Whether only attributes with ClassVar are treated as class attributes.
    requireInlineClassVarDocs : bool
        Whether to require inline class attribute docs.
    checkArgDefaults : bool
        Whether to check argument defaults.
    isStubFile : bool
        Whether the class is in a stub (.pyi) file.

    Returns
    -------
    None
    """
    # In stub files, a `...` default is a placeholder that doesn't say what
    # the default is (see `Visitor.checkArguments()`)
    placeholderDefaultNames: frozenset[str] = (
        frozenset(
            name
            for name, default in buildClassAttrToDefaultMapping(node).items()
            if isPlaceholderDefault(default)
        )
        if isStubFile and checkArgDefaults
        else frozenset()
    )

    docuemntedAndClassArgs = getDocumentedAndActualClassArgLists(
        node=node,
        style=style,
        ignorePrivateClassAttributes=ignorePrivateClassAttributes,
        ignoreUnderscoreOnlyClassAttributes=(
            ignoreUnderscoreOnlyClassAttributes
        ),
        ignoreSpecialDunderClassAttributes=(
            ignoreSpecialDunderClassAttributes
        ),
        treatPropertyMethodsAsClassAttributes=treatPropertyMethodsAsClassAttributes,
        onlyAttrsWithClassVarAreTreatedAsClassAttrs=(
            onlyAttrsWithClassVarAreTreatedAsClassAttrs
        ),
        checkArgDefaults=checkArgDefaults,
        violations=violations,
        skipCheckingShortDocstrings=skipCheckingShortDocstrings,
        requireInlineClassVarDocs=requireInlineClassVarDocs,
        argTypeHintsInDocstring=argTypeHintsInDocstring,
        placeholderDefaultNames=placeholderDefaultNames,
    )

    if docuemntedAndClassArgs is None:
        return

    docArgs, actualArgs = docuemntedAndClassArgs
    docArgs = removeDocstringDefaults(
        docArgs=docArgs,
        argNames=placeholderDefaultNames,
    )

    checkDocArgsLengthAgainstActualArgs(
        docArgs=docArgs,
        actualArgs=actualArgs,
        violations=violations,
        violationForDocArgsLengthShorter=Violation(
            code=601,
            line=lineNum,
            msgPrefix=msgPrefix,
            msgPostfix=SPHINX_MSG_POSTFIX,
        ),
        violationForDocArgsLengthLonger=Violation(
            code=602,
            line=lineNum,
            msgPrefix=msgPrefix,
            msgPostfix=SPHINX_MSG_POSTFIX,
        ),
    )

    checkNameOrderAndTypeHintsOfDocArgsAgainstActualArgs(
        docArgs=docArgs,
        actualArgs=actualArgs,
        violations=violations,
        actualArgsAreClassAttributes=True,
        violationForOrderMismatch=Violation(
            code=604,
            line=lineNum,
            msgPrefix=msgPrefix,
            msgPostfix=SPHINX_MSG_POSTFIX,
        ),
        violationForTypeHintMismatch=Violation(
            code=605,
            line=lineNum,
            msgPrefix=msgPrefix,
            msgPostfix=SPHINX_MSG_POSTFIX,
        ),
        shouldCheckArgOrder=shouldCheckArgOrder,
        argTypeHintsInSignature=argTypeHintsInSignature,
        argTypeHintsInDocstring=argTypeHintsInDocstring,
        requireInlineClassVarDocs=requireInlineClassVarDocs,
        lineNum=lineNum,
        msgPrefix=msgPrefix,
    )


def getDocumentedAndActualClassArgLists(
        *,
        node: ast.ClassDef,
        style: str,
        ignorePrivateClassAttributes: bool,
        ignoreUnderscoreOnlyClassAttributes: bool,
        ignoreSpecialDunderClassAttributes: bool,
        treatPropertyMethodsAsClassAttributes: bool,
        onlyAttrsWithClassVarAreTreatedAsClassAttrs: bool,
        checkArgDefaults: bool,
        violations: list[Violation],
        skipCheckingShortDocstrings: bool,
        requireInlineClassVarDocs: bool,
        argTypeHintsInDocstring: bool,
        placeholderDefaultNames: frozenset[str] = frozenset(),
) -> tuple[ArgList, ArgList] | None:
    """
    Get documented and actual class attribute lists.

    Parameters
    ----------
    node : ast.ClassDef
        The class definition node.
    style : str
        The docstring style.
    ignorePrivateClassAttributes : bool
        Whether to ignore private class attributes (such as ``_value``) when
        checking the docstring. Ignored attributes must not appear in the
        docstring.
    ignoreUnderscoreOnlyClassAttributes : bool
        Whether to ignore class attributes with underscore-only names (such as
        ``_``) when checking the docstring. Ignored attributes must not appear
        in the docstring.
    ignoreSpecialDunderClassAttributes : bool
        Whether to ignore class attributes with special dunder names (such as
        ``__slots__``) when checking the docstring. Ignored attributes must not
        appear in the docstring.
    treatPropertyMethodsAsClassAttributes : bool
        Whether to treat property methods as class attributes.
    onlyAttrsWithClassVarAreTreatedAsClassAttrs : bool
        Whether only attributes with ClassVar are treated as class attributes.
    checkArgDefaults : bool
        Whether to check argument defaults.
    violations : list[Violation]
        The list of violations.
    skipCheckingShortDocstrings : bool
        Whether to skip checking short docstrings.
    requireInlineClassVarDocs : bool
        Whether to require inline class attribute docs.
    argTypeHintsInDocstring : bool
        Whether to include type hints in docstring.
    placeholderDefaultNames : frozenset[str], default=frozenset()
        Names of the class attributes whose default is the ``...`` placeholder
        in a stub (.pyi) file. Their defaults aren't added to the type hints.

    Returns
    -------
    tuple[ArgList, ArgList] | None
        A tuple containing the documented and actual class attribute lists, or
        None if the class has no docstring or should be skipped.
    """
    actualArgs: ArgList = extractClassAttributesFromNode(
        node=node,
        ignorePrivateClassAttributes=ignorePrivateClassAttributes,
        ignoreUnderscoreOnlyClassAttributes=(
            ignoreUnderscoreOnlyClassAttributes
        ),
        ignoreSpecialDunderClassAttributes=(
            ignoreSpecialDunderClassAttributes
        ),
        treatPropertyMethodsAsClassAttrs=treatPropertyMethodsAsClassAttributes,
        onlyAttrsWithClassVarAreTreatedAsClassAttrs=(
            onlyAttrsWithClassVarAreTreatedAsClassAttrs
        ),
        checkArgDefaults=checkArgDefaults,
        placeholderDefaultNames=placeholderDefaultNames,
    )

    classDocstring: str = getDocstring(node)

    if classDocstring == '':
        # We don't check classes without any docstrings.
        # We defer to
        # flake8-docstrings (https://github.com/PyCQA/flake8-docstrings)
        # or pydocstyle (https://www.pydocstyle.org/en/stable/)
        # to determine whether a class needs a docstring.
        return None

    doc, potentialParsingError = parseDocstringInGivenStyle(
        docstring=classDocstring,
        style=style,
    )
    if potentialParsingError is not None:
        violations.append(
            Violation(
                code=1,
                line=node.lineno,
                msgPrefix=f'Class `{node.name}`:',
                msgPostfix=str(potentialParsingError).replace('\n', ' '),
            )
        )
        return None

    if skipCheckingShortDocstrings and doc.isShortDocstring:
        return None

    docArgs: ArgList = doc.attrList

    if requireInlineClassVarDocs and not docArgs.isEmpty:
        violations.append(
            Violation(
                code=607,
                line=node.lineno,
                msgPrefix=f'Class `{node.name}`:',
            )
        )
        # wipe out the args so we can catch any missing ones from inline docs
        docArgs = ArgList([])

    updateDocumentedArgListWithInlineDocstrings(
        node=node,
        docArgs=docArgs,
        actualArgs=actualArgs,
        argTypeHintsInDocstring=argTypeHintsInDocstring,
        requireInlineClassVarDocs=requireInlineClassVarDocs,
        violations=violations,
    )

    return docArgs, actualArgs


def updateDocumentedArgListWithInlineDocstrings(
        *,
        node: ast.ClassDef,
        docArgs: ArgList,
        actualArgs: ArgList,
        argTypeHintsInDocstring: bool,
        requireInlineClassVarDocs: bool,
        violations: list[Violation],
) -> None:
    """
    Check for inline class attribute docstrings and add them to the documented
    argument list.

    PEP-257 supports inline documentation for class variables, so we check for
    constant string literals after assignments in the class body.

    Parameters
    ----------
    node : ast.ClassDef
        The class definition node.
    docArgs : ArgList
        The argument list parsed from the class docstring.
    actualArgs : ArgList
        The actual class attributes extracted from the class definition and
        already filtered according to the class-attribute name options.
    argTypeHintsInDocstring : bool
        Whether argument type hints are expected to be in the docstring.
    requireInlineClassVarDocs : bool
        Whether to require inline class attribute docs.
    violations : list[Violation]
        The list of violations to append to.

    Returns
    -------
    None
        This function modifies ``docArgs`` in place.
    """
    prev = None
    idx = -1

    for element in node.body:
        # keep track of assignment index
        if isinstance(element, (ast.AnnAssign, ast.Assign)):
            idx += 1
            isExprConstantAfterAssign = False
        else:
            isExprConstantAfterAssign = (
                isinstance(element, ast.Expr)
                and isinstance(element.value, ast.Constant)
                and isinstance(prev, (ast.AnnAssign, ast.Assign))
            )

        if isExprConstantAfterAssign:
            arg = None

            if isinstance(prev, ast.AnnAssign):
                arg = Arg.fromAstAnnAssign(prev)
            elif isinstance(prev, ast.Assign):
                # technically, ast.Assign supports a list of _multiple_
                # targets, but for class attributes, multiple targets are
                # invalid. take the first target as the attribute name.
                args = ArgList.fromAstAssign(prev)
                if len(args.infoList) == 1:
                    arg = args.infoList[0]

            # only add if the var is in the actualArgs and
            # not already in docArgs, otherwise, it is a violation
            if arg is not None and actualArgs.contains(arg):
                if not requireInlineClassVarDocs:
                    violations.append(
                        Violation(
                            line=element.lineno,
                            code=606,
                            msgPrefix=(
                                f'Class `{node.name}`, Attribute `{arg.name}`:'
                            ),
                        )
                    )
                else:
                    # pull the type from the doc comment
                    arg.typeHint = ''
                    if argTypeHintsInDocstring:
                        docComment = cast('str', element.value.value)
                        if ':' in docComment:
                            # type hint is before the first colon
                            # on the first line
                            arg.typeHint = (
                                docComment.split('\n')[0].split(':')[0].strip()
                            )

                    docArgs.insertAt(idx, arg)

        prev = element


def shouldSkipCheckingPrivateFunction(
        *,
        name: str,
        skipCheckingPrivateFunctions: bool,
) -> bool:
    """
    Return whether to skip checking a function's docstring based on its name.

    When ``--skip-checking-private-functions`` is on, a function is skipped
    (its docstring is not checked) if its name is private, such as ``_helper``
    or ``__mangled``, or underscore-only, such as ``_`` in a ``singledispatch``
    registration. Public functions and special dunder methods, such as
    ``__init__``, are always checked.

    Parameters
    ----------
    name : str
        The function or method name.
    skipCheckingPrivateFunctions : bool
        The value of the ``--skip-checking-private-functions`` option.

    Returns
    -------
    bool
        True if the function should not be checked.
    """
    if not skipCheckingPrivateFunctions:
        return False

    return classifyName(name) in {NameKind.PRIVATE, NameKind.UNDERSCORE_ONLY}


def shouldIgnoreArgumentName(
        *,
        name: str,
        ignorePrivateArgs: bool,
        ignoreUnderscoreOnlyArgs: bool,
        ignoreSpecialDunderArgs: bool,
) -> bool:
    """Return whether a function argument name should be ignored."""
    # collectFuncArgs() prefixes star arguments with * or **, which are not
    # part of the Python identifier being classified.
    identifier = name.lstrip('*')
    nameKind = classifyName(identifier)
    if nameKind is NameKind.PRIVATE:
        return ignorePrivateArgs

    if nameKind is NameKind.UNDERSCORE_ONLY:
        return ignoreUnderscoreOnlyArgs

    if nameKind is NameKind.SPECIAL_DUNDER:
        return ignoreSpecialDunderArgs

    return False


def shouldIgnoreClassAttributeName(
        *,
        name: str,
        ignorePrivateClassAttributes: bool,
        ignoreUnderscoreOnlyClassAttributes: bool,
        ignoreSpecialDunderClassAttributes: bool,
) -> bool:
    """Return whether a class attribute name should be ignored."""
    nameKind = classifyName(name)
    if nameKind is NameKind.PRIVATE:
        return ignorePrivateClassAttributes

    if nameKind is NameKind.UNDERSCORE_ONLY:
        return ignoreUnderscoreOnlyClassAttributes

    if nameKind is NameKind.SPECIAL_DUNDER:
        return ignoreSpecialDunderClassAttributes

    return False


def extractClassAttributesFromNode(
        *,
        node: ast.ClassDef,
        ignorePrivateClassAttributes: bool,
        ignoreUnderscoreOnlyClassAttributes: bool,
        ignoreSpecialDunderClassAttributes: bool,
        treatPropertyMethodsAsClassAttrs: bool,
        onlyAttrsWithClassVarAreTreatedAsClassAttrs: bool,
        checkArgDefaults: bool,
        placeholderDefaultNames: frozenset[str] = frozenset(),
) -> ArgList:
    """
    Extract class attributes from an AST node.

    Parameters
    ----------
    node : ast.ClassDef
        The class definition
    ignorePrivateClassAttributes : bool
        Whether to ignore private class attributes (such as ``_value``) when
        checking the docstring. Ignored attributes must not appear in the
        docstring.
    ignoreUnderscoreOnlyClassAttributes : bool
        Whether to ignore class attributes with underscore-only names (such as
        ``_``) when checking the docstring. Ignored attributes must not appear
        in the docstring.
    ignoreSpecialDunderClassAttributes : bool
        Whether to ignore class attributes with special dunder names (such as
        ``__slots__``) when checking the docstring. Ignored attributes must not
        appear in the docstring.
    treatPropertyMethodsAsClassAttrs : bool
        Whether we'd like to treat property methods as class attributes. If
        ``True``, property methods will be included in the return value.
    onlyAttrsWithClassVarAreTreatedAsClassAttrs : bool
        If ``True``, only the attributes whose type annotations are wrapped
        within ``ClassVar`` (where ``ClassVar`` is imported from ``typing``)
        are treated as class attributes, and all other attributes are treated
        as instance attributes.
    checkArgDefaults : bool
        If True, we should extract the arguments' default values and attach
        them to the type hints.
    placeholderDefaultNames : frozenset[str], default=frozenset()
        Names of the class attributes whose default is the ``...`` placeholder
        in a stub (.pyi) file. Their defaults aren't attached to the type
        hints.

    Returns
    -------
    ArgList
        The argument list

    Raises
    ------
    EdgeCaseError
        When the length of ``item.targets`` is 0
    """
    if 'body' not in node.__dict__ or len(node.body) == 0:
        return ArgList([])

    classAttributes: list[Arg] = []
    for itm in node.body:
        if isinstance(itm, ast.AnnAssign):  # with type hints ("a: int = 1")
            classAttributes.append(Arg.fromAstAnnAssign(itm))
        elif isinstance(itm, ast.Assign):  # no type hints
            if not isinstance(itm.targets, list) or len(itm.targets) == 0:
                raise EdgeCaseError(
                    '`item.targets` needs to be a list of length > 0.'
                    f' Instead, it is {itm.targets}'
                )

            classAttributes.extend(ArgList.fromAstAssign(itm).infoList)
        elif isinstance(itm, (ast.AsyncFunctionDef, ast.FunctionDef)):  # noqa: SIM102
            if treatPropertyMethodsAsClassAttrs and checkIsPropertyMethod(itm):
                typeHint = (
                    '' if itm.returns is None else unparseName(itm.returns)
                )
                classAttributes.append(
                    Arg(
                        name=itm.name,
                        typeHint=typeHint,
                    )
                )

    classAttributes = [
        arg
        for arg in classAttributes
        if not shouldIgnoreClassAttributeName(
            name=arg.name,
            ignorePrivateClassAttributes=ignorePrivateClassAttributes,
            ignoreUnderscoreOnlyClassAttributes=(
                ignoreUnderscoreOnlyClassAttributes
            ),
            ignoreSpecialDunderClassAttributes=(
                ignoreSpecialDunderClassAttributes
            ),
        )
    ]

    if onlyAttrsWithClassVarAreTreatedAsClassAttrs:
        classAttributes = [
            Arg(
                name=_.name,
                typeHint=_.typeHint[9:-1],  # remove "ClassVar[" and "]"
            )
            for _ in classAttributes
            if (
                _.typeHint.startswith('ClassVar[') and _.typeHint.endswith(']')
            )
        ]

    astArgList = ArgList(infoList=classAttributes)

    if not checkArgDefaults:  # no need to add defaults to type hints
        return astArgList

    argToDefaultMapping: dict[str, ast.expr] = {
        name: default
        for name, default in buildClassAttrToDefaultMapping(node).items()
        if name not in placeholderDefaultNames
    }

    return ArgList([
        Arg.fromArgWithMapping(_, argToDefaultMapping)
        for _ in astArgList.infoList
    ])


def checkDocArgsLengthAgainstActualArgs(
        *,
        docArgs: ArgList,
        actualArgs: ArgList,
        violations: list[Violation],
        violationForDocArgsLengthShorter: Violation,  # such as V101, V601
        violationForDocArgsLengthLonger: Violation,  # such as V102, V602
) -> None:
    """Check lengths of doc arg list against actual arg list"""
    if docArgs.length < actualArgs.length:
        violations.append(violationForDocArgsLengthShorter)

    if docArgs.length > actualArgs.length:
        violations.append(violationForDocArgsLengthLonger)


def checkNameOrderAndTypeHintsOfDocArgsAgainstActualArgs(
        *,
        docArgs: ArgList,
        actualArgs: ArgList,
        violations: list[Violation],
        actualArgsAreClassAttributes: bool,
        violationForOrderMismatch: Violation,  # such as V104, V604
        violationForTypeHintMismatch: Violation,  # such as V105, V605
        shouldCheckArgOrder: bool,
        argTypeHintsInSignature: bool,
        argTypeHintsInDocstring: bool,
        requireInlineClassVarDocs: bool,
        lineNum: int,
        msgPrefix: str,
) -> None:
    """
    Check the arg/attr list in the docstring against the actual arg/attr list
    (either the function arguments or class attributes).
    """
    if not docArgs.equals(
        actualArgs,
        checkTypeHint=True,
        orderMatters=shouldCheckArgOrder,
    ):
        if docArgs.equals(
            actualArgs,
            checkTypeHint=True,
            orderMatters=False,
        ):
            violations.append(violationForOrderMismatch)
        elif docArgs.equals(
            actualArgs,
            checkTypeHint=False,
            orderMatters=shouldCheckArgOrder,
        ):
            if argTypeHintsInSignature and argTypeHintsInDocstring:
                v105new = appendArgsToCheckToV105(
                    original_v105=violationForTypeHintMismatch,
                    funcArgs=actualArgs,
                    docArgs=docArgs,
                )
                violations.append(v105new)
        elif docArgs.equals(
            actualArgs,
            checkTypeHint=False,
            orderMatters=False,
        ):
            v105new = appendArgsToCheckToV105(
                original_v105=violationForTypeHintMismatch,
                funcArgs=actualArgs,
                docArgs=docArgs,
            )
            violations.extend([violationForOrderMismatch, v105new])
        else:
            argsInFuncNotInDoc: set[Arg] = actualArgs.subtract(
                docArgs,
                checkTypeHint=False,
            )
            argsInDocNotInFunc: set[Arg] = docArgs.subtract(
                actualArgs,
                checkTypeHint=False,
            )

            msgPostfixParts: list[str] = []

            string0 = (
                'Attributes in the class definition but not '
                if actualArgsAreClassAttributes
                else 'Arguments in the function signature but not '
            )

            if argsInFuncNotInDoc:
                if requireInlineClassVarDocs and actualArgsAreClassAttributes:
                    string0 += 'documented inline:'
                else:
                    string0 += 'in the docstring:'

                msgPostfixParts.append(
                    string0 + f' {sorted(argsInFuncNotInDoc)}.'
                )

            string1 = (
                ' actual class attributes:'
                if actualArgsAreClassAttributes
                else ' function signature:'
            )

            if argsInDocNotInFunc:
                msgPostfixParts.append(
                    'Arguments in the docstring but not in the'
                    + string1
                    + f' {sorted(argsInDocNotInFunc)}.'
                )

            msgPostfixTemp: str = ' '.join(msgPostfixParts)

            if actualArgsAreClassAttributes:
                msgPostfixTemp += SPHINX_MSG_POSTFIX

            violations.append(
                Violation(
                    code=603 if actualArgsAreClassAttributes else 103,
                    line=lineNum,
                    msgPrefix=msgPrefix,
                    msgPostfix=msgPostfixTemp,
                )
            )


def addStarsToDocstringArgsWhenApplicable(
        *,
        docArgs: ArgList,
        funcArgs: ArgList,
) -> ArgList:
    """
    Align docstring vararg names with the signature's ``*args``/``**kwargs``.

    Parameters
    ----------
    docArgs : ArgList
        Arguments parsed from the docstring. These may omit the leading ``*``
        characters when documenting ``*args``/``**kwargs``.
    funcArgs : ArgList
        Arguments collected from the function signature. These provide the
        authoritative star-argument names we map onto.

    Returns
    -------
    ArgList
        A possibly new ``ArgList`` where docstring entries that describe
        varargs adopt the exact names (including leading ``*``) from the
        signature. Non-vararg entries are left untouched.

    Examples
    --------
    >>> funcArgs = ArgList([
    ...     Arg(name='*args', typeHint=''),
    ...     Arg(name='param', typeHint='int'),
    ... ])
    >>> docArgs = ArgList([
    ...     Arg(name='args', typeHint=''),
    ...     Arg(name='param', typeHint='int'),
    ... ])
    >>> normalized = addStarsToDocstringArgsWhenApplicable(
    ...     docArgs=docArgs, funcArgs=funcArgs
    ... )
    >>> [arg.name for arg in normalized.infoList]
    ['*args', 'param']
    """
    starArgs = [arg for arg in funcArgs.infoList if arg.isStarArg()]
    if len(starArgs) == 0:
        return docArgs

    strippedNameToStarName = {
        arg.name.lstrip('*'): arg.name for arg in starArgs
    }

    normalizedDocArgs: list[Arg] = []
    for docArg in docArgs.infoList:
        if docArg.isStarArg():
            normalizedDocArgs.append(docArg)
            continue

        strippedDocName = docArg.name.lstrip('*')
        if strippedDocName in strippedNameToStarName:
            normalizedDocArgs.append(
                Arg(
                    name=strippedNameToStarName[strippedDocName],
                    typeHint=docArg.typeHint,
                )
            )
        else:
            normalizedDocArgs.append(docArg)

    return ArgList(normalizedDocArgs)


DOCSTRING_DEFAULT_PREFIX_PATTERN = re.compile(r',\s*default\s*=')


def _removeDocstringDefault(typeHint: str) -> str:
    """Remove an outer default suffix while preserving annotation text."""
    # Backticks can wrap the type and the default together, such as in
    # ``int, default=3``, so remove them first (just as type comparison does)
    unwrapped = stripBacktickWrapper(typeHint)

    # A `, default=` can also appear inside the type itself, such as in
    # `Annotated[int, 'units, default=3']`. There, the text before it is not a
    # complete expression (it has an unclosed string or bracket). So the outer
    # default starts at the first match whose preceding text parses.
    for match in DOCSTRING_DEFAULT_PREFIX_PATTERN.finditer(unwrapped):
        annotation = unwrapped[: match.start()].rstrip()
        if not annotation:  # an untyped arg, such as `value (, default=3)`
            return ''

        try:
            ast.parse(annotation.strip(), mode='eval')
        except SyntaxError:
            continue

        return annotation

    return typeHint


def removeDocstringDefaults(
        *,
        docArgs: ArgList,
        argNames: frozenset[str],
) -> ArgList:
    """
    Remove the documented defaults of the given args.

    This is for args whose default is the ``...`` placeholder in a stub (.pyi)
    file. ``= ...`` means that there is a default value but doesn't say what it
    is, so the docstring may give any default value or none, and only the types
    are compared.

    Parameters
    ----------
    docArgs : ArgList
        Arguments (or class attributes) parsed from the docstring
    argNames : frozenset[str]
        Names of the args whose documented defaults are removed

    Returns
    -------
    ArgList
        The docstring args, with the defaults of the given args removed. All
        other args are left untouched.
    """
    if len(argNames) == 0:
        return docArgs

    return ArgList([
        Arg(name=_.name, typeHint=_removeDocstringDefault(_.typeHint))
        if _.name in argNames
        else _
        for _ in docArgs.infoList
    ])


def checkReturnTypesForViolations(
        *,
        style: str,
        returnAnnotation: ReturnAnnotation,
        violationList: list[Violation],
        returnSection: list[ReturnArg],
        violation: Violation,
) -> None:
    """Check return types between function signature and docstring"""
    if style == 'numpy':
        checkReturnTypesForNumpyStyle(
            returnAnnotation=returnAnnotation,
            violationList=violationList,
            returnSection=returnSection,
            violation=violation,
        )
    else:
        checkReturnTypesForGoogleOrSphinxStyle(
            returnAnnotation=returnAnnotation,
            violationList=violationList,
            returnSection=returnSection,
            violation=violation,
        )


def checkReturnTypesForNumpyStyle(
        *,
        returnAnnotation: ReturnAnnotation,
        violationList: list[Violation],
        returnSection: list[ReturnArg],
        violation: Violation,
) -> None:
    """Check return types for numpy docstring style"""
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
    returnAnnoItems: list[str] = returnAnnotation.decompose()
    returnAnnoInList: list[str] = returnAnnotation.putAnnotationInList()

    returnSecTypes: list[str] = [stripQuotes(_.argType) for _ in returnSection]

    if returnAnnoInList != returnSecTypes:
        if len(returnAnnoItems) != len(returnSection):
            msg = f'Return annotation has {len(returnAnnoItems)}'
            msg += ' type(s); docstring return section has'
            msg += f' {len(returnSection)} type(s).'
            violationList.append(violation.appendMoreMsg(moreMsg=msg))
        elif not all(
            # Equivalent to:
            # >>> specialEqual(x, y) for x, y in zip(..., ...)
            map(specialEqual, returnSecTypes, returnAnnoItems)
        ):
            msg1 = f'Return annotation types: {returnAnnoItems}; '
            msg2 = f'docstring return section types: {returnSecTypes}'
            violationList.append(violation.appendMoreMsg(msg1 + msg2))


def checkReturnTypesForGoogleOrSphinxStyle(
        *,
        returnAnnotation: ReturnAnnotation,
        violationList: list[Violation],
        returnSection: list[ReturnArg],
        violation: Violation,
) -> None:
    """Check return types for Google or Sphinx docstring style"""
    # The Google docstring style does not allow (or at least does
    # not encourage) splitting tuple return types (such as
    # Tuple[int, str, bool]) into individual types (int, str, and
    # bool).
    # Therefore, in Google-style docstrings, people should always
    # use one compound style for tuples.

    if len(returnSection) > 0:
        retArgType: str = stripQuotes(returnSection[0].argType)
        if returnAnnotation.annotation is None:
            msg = 'Return annotation has 0 type(s); docstring'
            msg += ' return section has 1 type(s).'
            violationList.append(violation.appendMoreMsg(moreMsg=msg))
        elif not specialEqual(retArgType, returnAnnotation.annotation):
            msg = 'Return annotation types: '
            msg += str([returnAnnotation.annotation]) + '; '
            msg += 'docstring return section types: '
            msg += str([retArgType])
            violationList.append(violation.appendMoreMsg(moreMsg=msg))
    elif bool(returnAnnotation.annotation):  # not empty str or not None
        msg = 'Return annotation has 1 type(s); docstring'
        msg += ' return section has 0 type(s).'
        violationList.append(violation.appendMoreMsg(moreMsg=msg))


def checkYieldTypesForViolations(
        *,
        originalReturnAnnotation: ReturnAnnotation,
        violationList: list[Violation],
        yieldSection: list[YieldArg],
        violation: Violation,
        generatorAnnotationKind: GeneratorAnnotationKind | None,
        hasIteratorOrIterableAsReturnAnnotation: bool,
        requireYieldSectionWhenYieldingNothing: bool,
) -> None:
    """
    Check yield types between function signature and docstring.

    The ``originalReturnAnnotation`` value must be the original function return
    annotation, such as ``Iterator[Dict[str, Any]]``. It must not be a
    pre-extracted yield type, such as ``Dict[str, Any]``. This helper calls
    ``extractYieldTypeFromGeneratorOrIteratorAnnotation`` and extracts the
    yield type exactly once before comparing it with the docstring "Yields"
    section.

    Parameters
    ----------
    originalReturnAnnotation : ReturnAnnotation
        The original function return annotation from the signature.
    violationList : list[Violation]
        The list of violations to append to.
    yieldSection : list[YieldArg]
        The parsed docstring "Yields" section.
    violation : Violation
        The DOC404 violation object to append when yield types mismatch.
    generatorAnnotationKind : GeneratorAnnotationKind | None
        The kind of Generator-like original return annotation, if present.
    hasIteratorOrIterableAsReturnAnnotation : bool
        Whether the original return annotation is an Iterator, Iterable,
        AsyncIterator, or AsyncIterable.
    requireYieldSectionWhenYieldingNothing : bool
        Whether a "Yields" section is required when the extracted yield type is
        None.

    Returns
    -------
    None
        This function mutates ``violationList`` in place.
    """
    # Even though the numpy docstring guide demonstrates that we can
    # write multiple values in the "Yields" section
    # (https://numpydoc.readthedocs.io/en/latest/format.html#yields),
    # in pydoclint we still only require putting all the yielded
    # values into one `Generator[..., ..., ...]`, because it is easier
    # to check and less ambiguous.

    originalReturnAnnoText: str | None = originalReturnAnnotation.annotation

    extract = extractYieldTypeFromGeneratorOrIteratorAnnotation
    yieldType: str | None = extract(
        returnAnnoText=originalReturnAnnoText,
        generatorAnnotationKind=generatorAnnotationKind,
        hasIteratorOrIterableAsReturnAnnotation=(
            hasIteratorOrIterableAsReturnAnnotation
        ),
    )

    if len(yieldSection) > 0:
        if originalReturnAnnoText is None:
            msg = 'Return annotation does not exist or is not'
            msg += ' Generator[...]/Iterator[...]/Iterable[...],'
            msg += ' but docstring "yields" section has 1 type(s).'
            violationList.append(violation.appendMoreMsg(moreMsg=msg))
        elif yieldSection[0].argType != yieldType:
            msg = (
                'The yield type (the 0th arg in Generator[...]'
                '/Iterator[...]): '
            )
            msg += str(yieldType) + '; '
            msg += 'docstring "yields" section types: '
            msg += str(yieldSection[0].argType)
            violationList.append(violation.appendMoreMsg(moreMsg=msg))
    elif (
        (
            generatorAnnotationKind is not None
            or hasIteratorOrIterableAsReturnAnnotation
        )
        and yieldType == 'None'
        and not requireYieldSectionWhenYieldingNothing
    ):
        # This means that we don't need to have a "Yields" section in the
        # docstring if the yield type is None.
        pass
    elif originalReturnAnnoText != '':
        msg = 'Return annotation exists, but docstring'
        msg += ' "yields" section does not exist or has 0 type(s).'
        violationList.append(violation.appendMoreMsg(moreMsg=msg))


def extractYieldTypeFromGeneratorOrIteratorAnnotation(
        returnAnnoText: str | None,
        generatorAnnotationKind: GeneratorAnnotationKind | None,
        hasIteratorOrIterableAsReturnAnnotation: bool,  # noqa: FBT001
) -> str | None:
    """
    Extract yield type from generator or iterator annotations.

    The caller supplies the generator kind so this helper only chooses arity
    rules; supported annotation spellings stay owned by the AST annotation
    detectors.
    """
    #
    # "Yield type" is the 0th element in a Generator
    # type annotation (Generator[YieldType, SendType,
    # ReturnType])
    # https://docs.python.org/3/library/typing.html#typing.Generator
    # Or it's the 0th (only) element in Iterator
    yieldType: str | None

    # Keep each annotation family in its own try so malformed annotations fall
    # back to the original text without hiding normal branch logic.
    if generatorAnnotationKind is not None:
        try:
            annotationArgs: list[ast.expr] = (
                _extractGeneratorOrAsyncGeneratorAnnotationArgs(
                    returnAnnoText,
                    generatorAnnotationKind=generatorAnnotationKind,
                )
            )
            yieldType = unparseName(annotationArgs[0])
        except (AttributeError, TypeError, IndexError, ValueError):
            yieldType = returnAnnoText
    elif hasIteratorOrIterableAsReturnAnnotation:
        try:
            annotationSlice: ast.expr = _extractAnnotationSubscriptSlice(
                returnAnnoText
            )
            yieldType = unparseName(annotationSlice)
        except (AttributeError, TypeError, IndexError, ValueError):
            yieldType = returnAnnoText
    else:
        yieldType = returnAnnoText

    return stripQuotes(yieldType)


def getReturnTypeToDocument(
        returnAnnotation: ReturnAnnotation,
        *,
        generatorAnnotationKind: GeneratorAnnotationKind | None,
) -> str | None:
    """
    Return the annotation type that a Returns section should document.

    Generator-like annotations document their generator return type, while
    Iterator and Iterable annotations keep the original annotation because they
    do not have Generator's omitted return-type slot.
    """
    if generatorAnnotationKind is None:
        return returnAnnotation.annotation

    return extractReturnTypeFromGeneratorAnnotation(
        returnAnnoText=returnAnnotation.annotation,
        generatorAnnotationKind=generatorAnnotationKind,
    )


def extractReturnTypeFromGeneratorAnnotation(
        returnAnnoText: str | None,
        *,
        generatorAnnotationKind: GeneratorAnnotationKind,
) -> str | None:
    """
    Extract return type from Generator and AsyncGenerator annotations.

    The caller supplies the generator kind so this helper does not re-detect
    annotation kind from raw text. That keeps spelling support centralized in
    the AST annotation detectors.
    """
    #
    # "Return type" is the 2nd element in a Generator type annotation
    # (Generator[YieldType, SendType, ReturnType]). Per PEP 696, it defaults
    # to None when only yield type or yield+send type are provided.
    # AsyncGenerator has no return type argument, so its return type is always
    # None when its arity can be interpreted.
    # https://docs.python.org/3/library/typing.html#typing.Generator
    returnType: str | None

    # AsyncGenerator has no ReturnType slot; successful arity validation means
    # the documented return type is None.
    if generatorAnnotationKind is GeneratorAnnotationKind.ASYNC_GENERATOR:
        try:
            _extractAsyncGeneratorAnnotationSubscriptArgs(returnAnnoText)
        except (AttributeError, TypeError, IndexError, ValueError):
            returnType = returnAnnoText
        else:
            returnType = 'None'

        return stripQuotes(returnType)

    try:
        generatorArgs: list[ast.expr]
        generatorArgs = _extractGeneratorAnnotationSubscriptArgs(
            returnAnnoText
        )
        # Abbreviated Generator annotations default ReturnType to None.
        returnType = (
            'None'
            if len(generatorArgs) <= GENERATOR_RETURN_TYPE_ARG_INDEX
            else unparseName(generatorArgs[GENERATOR_RETURN_TYPE_ARG_INDEX])
        )
    except (AttributeError, TypeError, IndexError, ValueError):
        returnType = returnAnnoText

    return stripQuotes(returnType)


def _extractGeneratorOrAsyncGeneratorAnnotationArgs(
        returnAnnoText: str | None,
        *,
        generatorAnnotationKind: GeneratorAnnotationKind,
) -> list[ast.expr]:
    """
    Extract generator-like annotation args according to their detected kind.

    ``Generator`` annotations are interpretable with 1-3 args, while
    ``AsyncGenerator`` annotations are interpretable with 1-2 args. The caller
    supplies the kind so this helper only applies the correct arity rule; it
    does not decide which annotation spellings are recognized.
    """
    if generatorAnnotationKind is GeneratorAnnotationKind.ASYNC_GENERATOR:
        return _extractAsyncGeneratorAnnotationSubscriptArgs(returnAnnoText)

    return _extractGeneratorAnnotationSubscriptArgs(returnAnnoText)


def _extractGeneratorAnnotationSubscriptArgs(
        returnAnnoText: str | None,
) -> list[ast.expr]:
    """
    Extract Generator args only when its arity can be interpreted (i.e., 1-3
    args).
    """
    annotationArgs = _extractAnnotationSubscriptArgs(returnAnnoText)
    if 1 <= len(annotationArgs) <= GENERATOR_MAX_ARG_COUNT:
        return annotationArgs

    raise ValueError('Generator annotations must have 1 to 3 arguments')


def _extractAsyncGeneratorAnnotationSubscriptArgs(
        returnAnnoText: str | None,
) -> list[ast.expr]:
    """
    Extract AsyncGenerator args only when its arity can be interpreted (i.e.,
    1-2 args).
    """
    annotationArgs = _extractAnnotationSubscriptArgs(returnAnnoText)
    if 1 <= len(annotationArgs) <= ASYNC_GENERATOR_MAX_ARG_COUNT:
        return annotationArgs

    raise ValueError('AsyncGenerator annotations must have 1 to 2 arguments')


def _extractAnnotationSubscriptArgs(
        returnAnnoText: str | None,
) -> list[ast.expr]:
    """Return the arguments supplied inside a subscript annotation."""
    annotationSlice = _extractAnnotationSubscriptSlice(returnAnnoText)
    if isinstance(annotationSlice, ast.Tuple):
        return list(annotationSlice.elts)

    return [annotationSlice]


def _extractAnnotationSubscriptSlice(returnAnnoText: str | None) -> ast.expr:
    """Return the slice inside a subscript annotation."""
    if returnAnnoText is None:
        raise TypeError('Return annotation cannot be None')

    parsedBody0 = ast.parse(returnAnnoText).body[0]
    if not isinstance(parsedBody0, ast.Expr):
        raise TypeError('Return annotation must parse to an expression')

    parsedValue = parsedBody0.value
    if not isinstance(parsedValue, ast.Subscript):
        raise TypeError('Return annotation must be subscripted')

    return parsedValue.slice


def addMismatchedRaisesExceptionViolation(
        *,
        docRaises: list[str],
        actualRaises: list[str],
        violations: list[Violation],
        violationForRaisesMismatch: Violation,  # such as V503
        lineNum: int,
        msgPrefix: str,
) -> None:
    """
    Add a violation for mismatched exception type between function body and
    docstring
    """
    msgPostfix: str = (
        f'Raised exceptions in the docstring: {docRaises}.'
        f' Raised exceptions in the body: {actualRaises}.'
    )
    violations.append(
        Violation(
            code=violationForRaisesMismatch.code,
            line=lineNum,
            msgPrefix=msgPrefix,
            msgPostfix=msgPostfix,
        )
    )
