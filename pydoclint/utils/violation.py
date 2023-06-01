import types
from typing import Tuple

from pydoclint.utils.internal_error import InternalError

VIOLATION_CODES = types.MappingProxyType({
    1: 'Potential formatting errors in docstring. Error message:',

    101: 'Docstring contains fewer arguments than in function signature.',
    102: 'Docstring contains more arguments than in function signature.',
    103: (  # noqa: PAR001
        'Docstring arguments are different from function arguments.'
        ' (Or could be other formatting issues: https://github.com/jsh9/pydoclint#notes-on-doc103).'
    ),
    104: 'Arguments are the same in the docstring and the function signature, but are in a different order.',
    105: 'Argument names match, but type hints do not match',

    201: 'does not have a return section in docstring',
    202: 'has a return section in docstring, but there are no return statements or annotations',

    301: '__init__() should not have a docstring; please combine it with the docstring of the class',
    302: 'The class docstring does not need a "Returns" section, because __init__() cannot return anything',
    303: 'The __init__() docstring does not need a "Returns" section, because it cannot return anything',
    304: 'Class docstring has an argument/parameter section; please put it in the __init__() docstring',
    305: 'Class docstring has a "Raises" section; please put it in the __init__() docstring',
    306: 'The class docstring does not need a "Yields" section, because __init__() cannot yield anything',
    307: 'The __init__() docstring does not need a "Yields" section, because __init__() cannot yield anything',

    401: 'returns a Generator, but the docstring does not have a "Yields" section',
    402: 'has "yield" statements, but the docstring does not have a "Yields" section',
    403: 'has a "Yields" section in the docstring, but there are no "yield" statements or a Generator return annotation',

    501: 'has "raise" statements, but the docstring does not have a "Raises" section',
    502: 'has a "Raises" section in the docstring, but there are not "raise" statements in the body',
})


class Violation:
    """A class to hold information of a style violation"""

    def __init__(
            self,
            line: int,
            code: int,
            msgPrefix: str = '',
            msgPostfix: str = '',
    ) -> None:
        if code not in VIOLATION_CODES:
            raise InternalError('Invalid violation code')

        self.line = line
        self.code = code
        self.msg = msgPrefix + ' ' + VIOLATION_CODES[code] + ' ' + msgPostfix

    @property
    def fullErrorCode(self) -> str:
        """Full error code, including the 'DOC' prefix"""
        return 'DOC' + f'{self.code}'.zfill(3)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'{self.fullErrorCode}: {self.msg}'

    def _str(self, showLineNum: bool = False) -> str:
        if not showLineNum:
            return self.__str__()

        return f'{self.line}: {self.__str__()}'

    def getInfoForFlake8(self) -> Tuple[int, int, str]:
        """Get the violation info for flake8"""
        colOffset: int = 0  # we don't need column offset to locate the issue
        return self.line, colOffset, self.__str__()
