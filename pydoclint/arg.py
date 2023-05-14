import ast

from numpydoc.docscrape import Parameter

from pydoclint.utils.annotation import parseAnnotation


class Arg:
    def __init__(self, name: str, typeHint: str) -> None:
        if len(name) == 0:
            raise ValueError('`name` cannot be an empty string')

        self.name: str= name
        self.typeHint: str = typeHint

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'{self.name}: {self.typeHint}'

    def __eq__(self, other: 'Arg') -> bool:
        if not isinstance(other, Arg):
            return False

        return self.name == other.name and self.typeHint == other.typeHint

    def __lt__(self, other: 'Arg') -> bool:
        if not isinstance(other, Arg):
            raise TypeError(f'Cannot compare; `other` is not of "Arg" type')

        if self.name < other.name:
            return True

        if self.name > other.name:
            return False

        return self.typeHint < other.typeHint

    def __le__(self, other: 'Arg') -> bool:
        return self < other or self == other

    def __hash__(self) -> int:
        return hash((self.name, self.typeHint))

    def nameEquals(self, other: 'Arg') -> bool:
        """More lenient equality: only compare names"""
        return self.name == other.name

    @classmethod
    def fromNumpydocParam(cls, param: Parameter) -> 'Arg':
        return Arg(name=param.name, typeHint=param.type)

    @classmethod
    def fromAstArg(cls, astArg: ast.arg) -> 'Arg':
        anno = astArg.annotation
        typeHint: str = '' if anno is None else parseAnnotation(anno)
        return Arg(name=astArg.arg, typeHint=typeHint)


class ArgList:
    def __init__(self, infoList: list[Arg]):
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

    def length(self) -> int:
        return len(self.infoList)

    def contains(self, arg: Arg) -> bool:
        return arg.name in self.lookup

    def get(self, argName: str) -> Arg:
        if argName not in self.lookup:
            raise KeyError(f'argName "{argName}" not in this object')

        return Arg(name=argName, typeHint=self.lookup[argName])

    def equals(
            self,
            other: 'ArgList',
            checkTypeHint: bool = True,
            orderMatters: bool = True,
    ) -> bool:
        if not isinstance(other, ArgList):
            return False

        if self.length() != other.length():
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

        return verdict

    def subtract(self, other: 'ArgList') -> set[Arg]:
        return set(self.infoList) - set(other.infoList)
