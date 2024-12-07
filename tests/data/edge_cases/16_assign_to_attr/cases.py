# From https://github.com/jsh9/pydoclint/issues/180


class MyClass:
    def large_drawing(self, obj):
        return self.drawing(obj, size=500, center=False)

    large_drawing.descr_1: str = 'Drawing'

    # Non-self attribute should not be type hinted, because this could lead to
    # potential ambiguities. See more: https://stackoverflow.com/a/77831273
    large_drawing.descr_2: str = 'Drawing'
