"""
Expected text and output helpers shared by configuration tests.

The migration messages are written out independently of
``pydoclint.utils.config_option_removal_messages`` so that tests fail when the
user-facing guidance changes unexpectedly.
"""

IGNORE_UNDERSCORE_ARGS_DEFAULT_MESSAGE = (
    'The option `--ignore-underscore-args` no longer works; remove it. Its'
    ' replacement, `--ignore-underscore-only-args`, defaults to `True`'
    ' (`ignore-underscore-only-args = true` in TOML/Flake8), which preserves'
    ' this behavior.'
)

IGNORE_UNDERSCORE_ARGS_NONDEFAULT_MESSAGE = (
    'The option `--ignore-underscore-args` no longer works. Replace it with'
    ' `--ignore-underscore-only-args=False` on the command line or'
    ' `ignore-underscore-only-args = false` in TOML/Flake8 config.'
)

SHOULD_DOCUMENT_PRIVATE_CLASS_ATTRIBUTES_DEFAULT_MESSAGE = (
    'The option `--should-document-private-class-attributes` no longer works;'
    ' remove it. Its replacements, `--ignore-private-class-attributes`,'
    ' `--ignore-underscore-only-class-attributes`, and'
    ' `--ignore-special-dunder-class-attributes`, all default to `True`'
    ' (`ignore-private-class-attributes = true`,'
    ' `ignore-underscore-only-class-attributes = true`, and'
    ' `ignore-special-dunder-class-attributes = true` in TOML/Flake8), which'
    ' preserves this behavior.'
)

SHOULD_DOCUMENT_PRIVATE_CLASS_ATTRIBUTES_ENABLED_MESSAGE = (
    'The option `--should-document-private-class-attributes` no longer works.'
    ' Use `--ignore-private-class-attributes=False`,'
    ' `--ignore-underscore-only-class-attributes=False`, and'
    ' `--ignore-special-dunder-class-attributes=False` on the command line, or'
    ' `ignore-private-class-attributes = false`,'
    ' `ignore-underscore-only-class-attributes = false`, and'
    ' `ignore-special-dunder-class-attributes = false` in TOML/Flake8 config.'
)


def extractListedNames(text: str, marker: str) -> list[str]:
    """Return the comma-separated names listed right after ``marker``."""
    return (
        text
        .split(marker, maxsplit=1)[1]
        .split('].', maxsplit=1)[0]
        .split(', ')
    )
