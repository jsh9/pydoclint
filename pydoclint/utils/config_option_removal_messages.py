"""Migration messages for removed configuration options."""


def getIgnoreUnderscoreArgsRemovedMessage(*, value: bool) -> str:
    """Return migration guidance for the removed underscore-args option."""
    if value:
        return (
            'The option `--ignore-underscore-args` no longer works; remove it.'
            ' Its replacement, `--ignore-underscore-only-args`, defaults to'
            ' `True` (`ignore-underscore-only-args = true` in TOML/Flake8),'
            ' which preserves this behavior.'
        )

    return (
        'The option `--ignore-underscore-args` no longer works. Replace it'
        ' with `--ignore-underscore-only-args=False` on the command line or'
        ' `ignore-underscore-only-args = false` in TOML/Flake8 config.'
    )


def getShouldDocumentPrivateClassAttributesRemovedMessage(
        *,
        value: bool,
) -> str:
    """Return migration guidance for the removed private-attributes option."""
    if not value:
        return (
            'The option `--should-document-private-class-attributes` no longer'
            ' works; remove it. Its replacements,'
            ' `--ignore-private-class-attributes`,'
            ' `--ignore-underscore-only-class-attributes`, and'
            ' `--ignore-special-dunder-class-attributes`, all default to'
            ' `True` (`ignore-private-class-attributes = true`,'
            ' `ignore-underscore-only-class-attributes = true`, and'
            ' `ignore-special-dunder-class-attributes = true` in'
            ' TOML/Flake8), which preserves this behavior.'
        )

    return (
        'The option `--should-document-private-class-attributes` no longer'
        ' works. Use `--ignore-private-class-attributes=False`,'
        ' `--ignore-underscore-only-class-attributes=False`, and'
        ' `--ignore-special-dunder-class-attributes=False` on the command'
        ' line, or `ignore-private-class-attributes = false`,'
        ' `ignore-underscore-only-class-attributes = false`, and'
        ' `ignore-special-dunder-class-attributes = false` in TOML/Flake8'
        ' config.'
    )
