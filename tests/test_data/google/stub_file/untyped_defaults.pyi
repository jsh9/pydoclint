# This fixture is checked with checkArgDefaults=True and with both
# argTypeHintsInSignature and argTypeHintsInDocstring set to False, so its
# arguments have no type hints anywhere. The placeholder defaults (`= ...`) can
# still be documented with any default or none.

def connect(host=..., port=..., verbose=...) -> None:
    """
    Function whose untyped arguments have placeholder defaults.

    Args:
        host (, default='localhost'): Host name. (Any documented default is
            fine.)
        port (, default=8080): Port number. (Any documented default is fine.)
        verbose: Whether to log. (No documented default is also fine.)
    """
    ...
