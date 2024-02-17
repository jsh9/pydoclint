"""Helper functions to classes/methods in visitor.py"""
import ast
import sys
from typing import List, Optional

from pydoclint.utils.annotation import unparseAnnotation
from pydoclint.utils.generic import specialEqual, stripQuotes
from pydoclint.utils.return_anno import ReturnAnnotation
from pydoclint.utils.return_arg import ReturnArg
from pydoclint.utils.violation import Violation
from pydoclint.utils.yield_arg import YieldArg


def checkReturnTypesForViolations(
        *,
        style: str,
        returnAnnotation: ReturnAnnotation,
        violationList: List[Violation],
        returnSection: List[ReturnArg],
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
        violationList: List[Violation],
        returnSection: List[ReturnArg],
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
    returnAnnoItems: List[str] = returnAnnotation.decompose()
    returnAnnoInList: List[str] = returnAnnotation.putAnnotationInList()

    returnSecTypes: List[str] = [stripQuotes(_.argType) for _ in returnSection]

    if returnAnnoInList != returnSecTypes:
        if len(returnAnnoItems) != len(returnSection):
            msg = f'Return annotation has {len(returnAnnoItems)}'
            msg += ' type(s); docstring return section has'
            msg += f' {len(returnSection)} type(s).'
            violationList.append(violation.appendMoreMsg(moreMsg=msg))
        else:
            if not all(
                specialEqual(x, y)
                for x, y in zip(returnSecTypes, returnAnnoItems)
            ):
                msg1 = f'Return annotation types: {returnAnnoItems}; '
                msg2 = f'docstring return section types: {returnSecTypes}'
                violationList.append(violation.appendMoreMsg(msg1 + msg2))


def checkReturnTypesForGoogleOrSphinxStyle(
        *,
        returnAnnotation: ReturnAnnotation,
        violationList: List[Violation],
        returnSection: List[ReturnArg],
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
    else:
        if bool(returnAnnotation.annotation):  # not empty str or not None
            msg = 'Return annotation has 1 type(s); docstring'
            msg += ' return section has 0 type(s).'
            violationList.append(violation.appendMoreMsg(moreMsg=msg))


def checkYieldTypesForViolations(
        *,
        returnAnnotation: ReturnAnnotation,
        violationList: List[Violation],
        yieldSection: List[YieldArg],
        violation: Violation,
        hasGeneratorAsReturnAnnotation: bool,
        hasIteratorOrIterableAsReturnAnnotation: bool,
        requireYieldSectionWhenYieldingNothing: bool,
) -> None:
    """Check yield types between function signature and docstring"""
    # Even though the numpy docstring guide demonstrates that we can
    # write multiple values in the "Yields" section
    # (https://numpydoc.readthedocs.io/en/latest/format.html#yields),
    # in pydoclint we still only require putting all the yielded
    # values into one `Generator[..., ..., ...]`, because it is easier
    # to check and less ambiguous.

    returnAnnoText: Optional[str] = returnAnnotation.annotation
    yieldType: str = extractYieldTypeFromGeneratorOrIteratorAnnotation(
        returnAnnoText,
        hasGeneratorAsReturnAnnotation,
        hasIteratorOrIterableAsReturnAnnotation,
    )

    if len(yieldSection) > 0:
        if returnAnnoText is None:
            msg = 'Return annotation does not exist or is not'
            msg += ' Generator[...]/Iterator[...]/Iterable[...],'
            msg += ' but docstring "yields" section has 1 type(s).'
            violationList.append(violation.appendMoreMsg(moreMsg=msg))
        else:
            if yieldSection[0].argType != yieldType:
                msg = (
                    'The yield type (the 0th arg in Generator[...]'
                    '/Iterator[...]): '
                )
                msg += str(yieldType) + '; '
                msg += 'docstring "yields" section types: '
                msg += str(yieldSection[0].argType)
                violationList.append(violation.appendMoreMsg(moreMsg=msg))
    else:
        if (
            (
                hasGeneratorAsReturnAnnotation
                or hasIteratorOrIterableAsReturnAnnotation
            )
            and yieldType == 'None'
            and not requireYieldSectionWhenYieldingNothing
        ):
            # This means that we don't need to have a "Yields" section in the
            # docstring if the yield type is None.
            pass
        elif returnAnnoText != '':
            msg = 'Return annotation exists, but docstring'
            msg += ' "yields" section does not exist or has 0 type(s).'
            violationList.append(violation.appendMoreMsg(moreMsg=msg))


def extractYieldTypeFromGeneratorOrIteratorAnnotation(
        returnAnnoText: str,
        hasGeneratorAsReturnAnnotation: bool,
        hasIteratorOrIterableAsReturnAnnotation: bool,
) -> str:
    """Extract yield type from Generator or Iterator annotations"""
    try:
        # "Yield type" is the 0th element in a Generator
        # type annotation (Generator[YieldType, SendType,
        # ReturnType])
        # https://docs.python.org/3/library/typing.html#typing.Generator
        # Or it's the 0th (only) element in Iterator
        yieldType: str

        if hasGeneratorAsReturnAnnotation:
            if sys.version_info >= (3, 9):
                yieldType = unparseAnnotation(
                    ast.parse(returnAnnoText).body[0].value.slice.elts[0]
                )
            else:
                yieldType = unparseAnnotation(
                    ast.parse(returnAnnoText).body[0].value.slice.value.elts[0]
                )
        elif hasIteratorOrIterableAsReturnAnnotation:
            yieldType = unparseAnnotation(
                ast.parse(returnAnnoText).body[0].value.slice
            )
        else:
            yieldType = returnAnnoText
    except Exception:
        yieldType = returnAnnoText

    return stripQuotes(yieldType)


def extractReturnTypeFromGenerator(returnAnnoText: str) -> str:
    """Extract return type from Generator annotations"""
    try:
        # "Return type" is the last element in a Generator
        # type annotation (Generator[YieldType, SendType,
        # ReturnType])
        # https://docs.python.org/3/library/typing.html#typing.Generator
        returnType: str
        if sys.version_info >= (3, 9):
            returnType = unparseAnnotation(
                ast.parse(returnAnnoText).body[0].value.slice.elts[-1]
            )
        else:
            returnType = unparseAnnotation(
                ast.parse(returnAnnoText).body[0].value.slice.value.elts[-1]
            )
    except Exception:
        returnType = returnAnnoText

    return stripQuotes(returnType)
