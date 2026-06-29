"""Helper functions to classes/methods in visitor.py"""

from __future__ import annotations

import ast
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from pydoclint.utils.return_anno import ReturnAnnotation
    from pydoclint.utils.return_arg import ReturnArg
    from pydoclint.utils.yield_arg import YieldArg

from pydoclint.utils.arg import Arg, ArgList
from pydoclint.utils.edge_case_error import EdgeCaseError
from pydoclint.utils.generic import (
    appendArgsToCheckToV105,
    buildClassAttrToDefaultMapping,
    getDocstring,
    specialEqual,
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
        shouldDocumentPrivateClassAttributes: bool,
        treatPropertyMethodsAsClassAttributes: bool,
        onlyAttrsWithClassVarAreTreatedAsClassAttrs: bool,
        requireInlineClassVarDocs: bool,
        checkArgDefaults: bool,
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
    shouldDocumentPrivateClassAttributes : bool
        Whether to document private class attributes.
    treatPropertyMethodsAsClassAttributes : bool
        Whether to treat property methods as class attributes.
    onlyAttrsWithClassVarAreTreatedAsClassAttrs : bool
        Whether only attributes with ClassVar are treated as class attributes.
    requireInlineClassVarDocs : bool
        Whether to require inline class attribute docs.
    checkArgDefaults : bool
        Whether to check argument defaults.

    Returns
    -------
    None
    """
    docuemntedAndClassArgs = getDocumentedAndActualClassArgLists(
        node=node,
        style=style,
        shouldDocumentPrivateClassAttributes=shouldDocumentPrivateClassAttributes,
        treatPropertyMethodsAsClassAttributes=treatPropertyMethodsAsClassAttributes,
        onlyAttrsWithClassVarAreTreatedAsClassAttrs=(
            onlyAttrsWithClassVarAreTreatedAsClassAttrs
        ),
        checkArgDefaults=checkArgDefaults,
        violations=violations,
        skipCheckingShortDocstrings=skipCheckingShortDocstrings,
        requireInlineClassVarDocs=requireInlineClassVarDocs,
        argTypeHintsInDocstring=argTypeHintsInDocstring,
    )

    if docuemntedAndClassArgs is None:
        return

    docArgs, actualArgs = docuemntedAndClassArgs

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
        shouldDocumentPrivateClassAttributes: bool,
        treatPropertyMethodsAsClassAttributes: bool,
        onlyAttrsWithClassVarAreTreatedAsClassAttrs: bool,
        checkArgDefaults: bool,
        violations: list[Violation],
        skipCheckingShortDocstrings: bool,
        requireInlineClassVarDocs: bool,
        argTypeHintsInDocstring: bool,
) -> tuple[ArgList, ArgList] | None:
    """
    Get documented and actual class attribute lists.

    Parameters
    ----------
    node : ast.ClassDef
        The class definition node.
    style : str
        The docstring style.
    shouldDocumentPrivateClassAttributes : bool
        Whether to document private class attributes.
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

    Returns
    -------
    tuple[ArgList, ArgList] | None
        A tuple containing the documented and actual class attribute lists, or
        None if the class has no docstring or should be skipped.
    """
    actualArgs: ArgList = extractClassAttributesFromNode(
        node=node,
        shouldDocumentPrivateClassAttributes=(
            shouldDocumentPrivateClassAttributes
        ),
        treatPropertyMethodsAsClassAttrs=treatPropertyMethodsAsClassAttributes,
        onlyAttrsWithClassVarAreTreatedAsClassAttrs=(
            onlyAttrsWithClassVarAreTreatedAsClassAttrs
        ),
        checkArgDefaults=checkArgDefaults,
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
        shouldDocumentPrivateClassAttributes=shouldDocumentPrivateClassAttributes,
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
        shouldDocumentPrivateClassAttributes: bool,
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
        The actual class attributes extracted from the class definition.
    shouldDocumentPrivateClassAttributes : bool
        Whether we should document private class attributes. If ``True``,
        private class attributes will be included.
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
            if (
                arg is not None
                and (
                    shouldDocumentPrivateClassAttributes
                    or not arg.name.startswith('_')
                )
                and actualArgs.contains(arg)
            ):
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


def extractClassAttributesFromNode(
        *,
        node: ast.ClassDef,
        shouldDocumentPrivateClassAttributes: bool,
        treatPropertyMethodsAsClassAttrs: bool,
        onlyAttrsWithClassVarAreTreatedAsClassAttrs: bool,
        checkArgDefaults: bool,
) -> ArgList:
    """
    Extract class attributes from an AST node.

    Parameters
    ----------
    node : ast.ClassDef
        The class definition
    shouldDocumentPrivateClassAttributes : bool
        Whether we should document private class attributes.  If ``True``,
        private class attributes will be included in the return value.
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

    atl: list[Arg] = []
    for itm in node.body:
        if isinstance(itm, ast.AnnAssign):  # with type hints ("a: int = 1")
            atl.append(Arg.fromAstAnnAssign(itm))
        elif isinstance(itm, ast.Assign):  # no type hints
            if not isinstance(itm.targets, list) or len(itm.targets) == 0:
                raise EdgeCaseError(
                    '`item.targets` needs to be a list of length > 0.'
                    f' Instead, it is {itm.targets}'
                )

            atl.extend(ArgList.fromAstAssign(itm).infoList)
        elif isinstance(itm, (ast.AsyncFunctionDef, ast.FunctionDef)):  # noqa: SIM102
            if treatPropertyMethodsAsClassAttrs and checkIsPropertyMethod(itm):
                typeHint = (
                    '' if itm.returns is None else unparseName(itm.returns)
                )
                atl.append(
                    Arg(
                        name=itm.name,
                        typeHint=typeHint,
                    )
                )

    if not shouldDocumentPrivateClassAttributes:
        atl = [_ for _ in atl if not _.name.startswith('_')]

    if onlyAttrsWithClassVarAreTreatedAsClassAttrs:
        atl = [
            Arg(
                name=_.name,
                typeHint=_.typeHint[9:-1],  # remove "ClassVar[" and "]"
            )
            for _ in atl
            if (
                _.typeHint.startswith('ClassVar[') and _.typeHint.endswith(']')
            )
        ]

    astArgList = ArgList(infoList=atl)

    if not checkArgDefaults:  # no need to add defaults to type hints
        return astArgList

    argToDefaultMapping: dict[str, ast.expr] = buildClassAttrToDefaultMapping(
        node,
    )

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

    try:
        if generatorAnnotationKind is not None:
            annotationArgs = _extractGeneratorOrAsyncGeneratorAnnotationArgs(
                returnAnnoText,
                generatorAnnotationKind=generatorAnnotationKind,
            )
            yieldType = unparseName(annotationArgs[0])
        elif hasIteratorOrIterableAsReturnAnnotation:
            annotationSlice = _extractAnnotationSubscriptSlice(returnAnnoText)
            yieldType = unparseName(annotationSlice)
        else:
            yieldType = returnAnnoText
    except (AttributeError, TypeError, IndexError, ValueError):
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
    try:
        if generatorAnnotationKind is GeneratorAnnotationKind.ASYNC_GENERATOR:
            _extractAsyncGeneratorAnnotationSubscriptArgs(returnAnnoText)
            returnType = 'None'
            return stripQuotes(returnType)

        generatorArgs = _extractGeneratorAnnotationSubscriptArgs(
            returnAnnoText
        )
        if len(generatorArgs) <= GENERATOR_RETURN_TYPE_ARG_INDEX:
            returnType = 'None'
        else:
            returnArg = generatorArgs[GENERATOR_RETURN_TYPE_ARG_INDEX]
            returnType = unparseName(returnArg)
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
        raise AttributeError('Return annotation must parse to an expression')

    parsedValue = parsedBody0.value
    if not isinstance(parsedValue, ast.Subscript):
        raise AttributeError('Return annotation must be subscripted')

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
