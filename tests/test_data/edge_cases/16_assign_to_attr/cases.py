# From https://github.com/jsh9/pydoclint/issues/180


class MyClass:
    def large_drawing(self, obj):
        return self.drawing(obj, size=500, center=False)

    large_drawing.descr_1: str = 'Drawing'

    # Non-self attribute should not be type hinted, because this could lead to
    # potential ambiguities. See more: https://stackoverflow.com/a/77831273
    large_drawing.descr_2: str = 'Drawing'

    # The following is from:
    # https://github.com/matplotlib/matplotlib/blob/c2d502d219c8c0abe8722279b21f817aeae2058a/lib/matplotlib/backends/backend_agg.py#L510-L521
    print_jpg.__doc__, print_tif.__doc__, print_webp.__doc__ = map(
        """
        Write the figure to a {} file.

        Parameters
        ----------
        filename_or_obj : str or path-like or file-like
            The file to write to.
        pil_kwargs : dict, optional
            Additional keyword arguments that are passed to
            `PIL.Image.Image.save` when saving the figure.
        """.format, ["JPEG", "TIFF", "WebP"])
