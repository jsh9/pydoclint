from docstring_parser.google import GoogleParser
from docstring_parser.common import DocstringReturns
from numpydoc.docscrape import NumpyDocString

from pydoclint.utils.arg import Arg, ArgList
from pydoclint.utils.internal_error import InternalError


class Doc:
    """A class to hold docstring and to provide info on the parsed docstring"""

    def __init__(self, docstring: str, style: str = 'numpy') -> None:
        self.docstring = docstring
        self.style = style

        if style == 'numpy':
            # Note: a NumpyDocString object has the following sections:
            # *  {'Signature': '', 'Summary': [''], 'Extended Summary': [],
            # *  'Parameters': [], 'Returns': [], 'Yields': [], 'Receives': [],
            # *  'Raises': [], 'Warns': [], 'Other Parameters': [],
            # *  'Attributes': [], 'Methods': [], 'See Also': [], 'Notes': [],
            # *  'Warnings': [], 'References': '', 'Examples': '', 'index': {}}
            self.parsed = NumpyDocString(docstring)
        elif style == 'google':
            parser = GoogleParser()
            self.parsed = parser.parse(docstring)
        else:
            msg = f'Unknown style {style}; please contact the authors'
            raise InternalError(msg)

    @property
    def isShortDocstring(self) -> bool:
        if self.style == 'numpy':
            return (
                (
                    bool(self.parsed.get('Summary'))
                    or bool(self.parsed.get('Extended Summary'))
                )
                and not bool(self.parsed.get('Parameters'))
                and not bool(self.parsed.get('Returns'))
                and not bool(self.parsed.get('Yields'))
                and not bool(self.parsed.get('Receives'))
                and not bool(self.parsed.get('Raises'))
                and not bool(self.parsed.get('Warns'))
                and not bool(self.parsed.get('Other Parameters'))
                and not bool(self.parsed.get('Attributes'))
                and not bool(self.parsed.get('Methods'))
                and not bool(self.parsed.get('See Also'))
                and not bool(self.parsed.get('Notes'))
                and not bool(self.parsed.get('Warnings'))
                and not bool(self.parsed.get('References'))
                and not bool(self.parsed.get('Examples'))
                and not bool(self.parsed.get('index'))
            )

    @property
    def argList(self) -> ArgList:
        if self.style == 'numpy':
            return ArgList([
                Arg.fromNumpydocParam(_)
                for _ in self.parsed.get('Parameters', [])
            ])

        if self.style == 'google':
            return ArgList([
                Arg.fromGoogleParsedParam(_) for _ in self.parsed.params
            ])

    @property
    def hasReturnsSection(self) -> bool:
        if self.style == 'numpy':
            return bool(self.parsed.get('Returns'))

        if self.style == 'google':
            retSection: DocstringReturns = self.parsed.returns
            return retSection is not None and not retSection.is_generator

    @property
    def hasYieldsSection(self) -> bool:
        if self.style == 'numpy':
            return bool(self.parsed.get('Yields'))

        if self.style == 'google':
            retSection: DocstringReturns = self.parsed.returns
            return retSection is not None and retSection.is_generator

    @property
    def hasRaisesSection(self) -> bool:
        if self.style == 'numpy':
            return bool(self.parsed.get('Raises'))

        if self.style == 'google':
            return len(self.parsed.raises) > 0
