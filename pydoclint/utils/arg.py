import ast
from typing import List, Optional, Set

from docstring_parser.common import DocstringParam
from numpydoc.docscrape import Parameter

from pydoclint.utils.annotation import unparseAnnotation


class Arg:
    """
    A class to hold function input/return arguments.

    This class also defines some essential behaviors of an argument, such
    as comparison, equality, hashing, etc.
    """

    def __init__(self, name: str, typeHint: str) -> None:
        if len(name) == 0:
            raise ValueError('`name` cannot be an empty string')

        self.name: str = name
        self.typeHint: str = typeHint

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'{self.name}: {self.typeHint}'

    def __eq__(self, o: 'Arg') -> bool:
        if not isinstance(o, Arg):
            return False

        return self.name == o.name and self._eq(self.typeHint, o.typeHint)

    def __lt__(self, other: 'Arg') -> bool:
        if not isinstance(other, Arg):
            raise TypeError('Cannot compare; `other` is not of "Arg" type')

        if self.name < other.name:
            return True

        if self.name > other.name:
            return False

        return self.typeHint < other.typeHint

    def __le__(self, other: 'Arg') -> bool:
        return self < other or self == other

    def __hash__(self) -> int:
        return hash((self.name, self._stripQuotes(self.typeHint)))

    def nameEquals(self, other: 'Arg') -> bool:
        """More lenient equality: only compare names"""
        return self.name == other.name

    @classmethod
    def fromNumpydocParam(cls, param: Parameter) -> 'Arg':
        """Construct an Arg object from a Numpydoc Parameter object"""
        return Arg(name=param.name, typeHint=param.type)

    @classmethod
    def fromGoogleParsedParam(cls, param: DocstringParam) -> 'Arg':
        """Construct an Arg object from a GoogleParser Parameter object"""
        return Arg(name=param.arg_name, typeHint=cls._str(param.type_name))

    @classmethod
    def fromAstArg(cls, astArg: ast.arg) -> 'Arg':
        """Construct an Arg object from a Python AST argument object"""
        anno = astArg.annotation
        typeHint: str = '' if anno is None else unparseAnnotation(anno)
        return Arg(name=astArg.arg, typeHint=typeHint)

    @classmethod
    def _str(cls, typeName: Optional[str]) -> str:
        return '' if typeName is None else typeName

    @classmethod
    def _eq(cls, str1: str, str2: str) -> bool:
        return cls._stripQuotes(str1) == cls._stripQuotes(str2)

    @classmethod
    def _stripQuotes(cls, string: str) -> str:
        return string.replace('"', '').replace("'", '')


class ArgList:
    """
    A class to hold a list of `Arg` objects.

    This class also defines some behaviors of an argument list, such as
    equality, length calculation, etc.
    """

    def __init__(self, infoList: List[Arg]):
        if not all(isinstance(_, Arg) for _ in infoList):
            raise TypeError('All elements of `infoList` must be Arg.')

        self.infoList = infoList
        self.lookup = {_.name: _.typeHint for _ in infoList}

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return '[' + ', '.join(str(_) for _ in self.infoList) + ']'

    def __eq__(self, other: 'ArgList') -> bool:
        if not isinstance(other, ArgList):
            return False

        return self.infoList == other.infoList

    @property
    def isEmpty(self) -> bool:
        """Whether the arg list is empty"""
        return self.length == 0

    @property
    def nonEmpty(self) -> bool:
        """Whether the arg list is non-empty"""
        return not self.isEmpty

    @property
    def length(self) -> int:
        """Calculate the length of the list"""
        return len(self.infoList)

    @classmethod
    def fromNumpydocParam(cls, params: List[Parameter]) -> 'ArgList':
        """Construct an Arglist from a list of Parameter objects"""
        return ArgList([Arg.fromNumpydocParam(_) for _ in params])

    @classmethod
    def fromGoogleParsedParam(cls, params: List[DocstringParam]) -> 'ArgList':
        """Construct an ArgList from a list of DocstringParam objects"""
        infoList = [
            Arg.fromGoogleParsedParam(_)
            for _ in params
            if _.args[0] != 'attribute'  # we only need 'param' not 'attribute'
        ]
        return ArgList(infoList=infoList)

    def contains(self, arg: Arg) -> bool:
        """Whether a given `Arg` object exists in the list"""
        return arg.name in self.lookup

    def get(self, argName: str) -> Arg:
        """Retrieve an element from the list using `argName` as identifier"""
        if argName not in self.lookup:
            raise KeyError(f'argName "{argName}" not in this object')

        return Arg(name=argName, typeHint=self.lookup[argName])

    def equals(
            self,
            other: 'ArgList',
            checkTypeHint: bool = True,
            orderMatters: bool = True,
    ) -> bool:
        """
        Check whether this object is equal to `other`.

        Parameters
        ----------
        other : ArgList
            The other object
        checkTypeHint : bool
            If True, the two objects are only considered equal when type hints
            are also equal.
        orderMatters : bool
            If True, the two objects are only considered equal when the order
            of the arguments are identical.

        Returns
        -------
        bool
            Whether the two objects are equal.
        """
        if not isinstance(other, ArgList):
            return False

        if self.length != other.length:
            return False

        verdict: bool

        if checkTypeHint:
            if orderMatters:  # most strict case
                verdict = self == other
            else:
                verdict = set(self.infoList) == set(other.infoList)
        else:
            self_names = [_.name for _ in self.infoList]
            other_names = [_.name for _ in other.infoList]
            if orderMatters:
                verdict = self_names == other_names
            else:
                verdict = set(self_names) == set(other_names)

        return verdict  # noqa: R504

    def subtract(self, other: 'ArgList') -> Set[Arg]:
        """Find the args that are in this object but not in `other`."""
        return set(self.infoList) - set(other.infoList)
