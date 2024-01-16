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
