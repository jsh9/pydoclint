import abc


class MyClass:
    data: float = 2.1

    @property
    def something(self) -> float:
        """
        Some property.

        It's OK to have no return section in this method, because this
        is a "property method" and is intended to be used as an attribute.
        """
        return self.data

class AbstractClass(abc.ABC):
    def __init__(self):
        pass

    @property
    @abc.abstractmethod
    def something(self) -> float:
        """
        Some abstract property.

        This is also OK; @property does not have to be the inner decorator.
        """
