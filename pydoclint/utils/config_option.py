"""Helpers for configuration-option migration messages."""


def getIgnoreUnderscoreArgsRemovedMessage(*, value: bool) -> str:
    """Return migration guidance for the removed underscore-args option."""
    return (
        'The option `--ignore-underscore-args` no longer works; please use '
        f'`--ignore-underscore-only-args={value}` instead'
    )


def getShouldDocumentPrivateClassAttributesRemovedMessage(
        *,
        value: bool,
) -> str:
    """Return migration guidance for the removed private-attributes option."""
    replacementValue = not value
    return (
        'The option `--should-document-private-class-attributes` no longer '
        'works. To preserve its previous behavior, please use both '
        f'`--ignore-private-class-attributes={replacementValue}` and '
        '`--ignore-underscore-only-class-attributes='
        f'{replacementValue}` instead'
    )
