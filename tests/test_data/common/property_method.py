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

class MyOtherClass:
    def __init__(self):
        pass

    @property
    @something
    @something_else
    @well
    def method_1(self) -> float:
        """
        Some abstract property.

        This is also OK. When @property is the outer-most decorator (i.e., at
        the top), the method is still considered a "property method" and thus 
        does not need a return section.
        """
        pass

    @something
    @property
    @something_else
    @well
    def method_2(self) -> float:
        """
        This is NOT a property method, because @property is not the outer-most
        decorator. Therefore, this method should have a return section.
        """
        pass

    @something
    @something_else
    @well
    @property
    def method_3(self) -> float:
        """
        This is NOT a property method, because @property is not the outer-most
        decorator. Therefore, this method should have a return section.
        """
        pass
