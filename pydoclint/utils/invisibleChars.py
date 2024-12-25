def replaceInvisibleChars(text: str) -> str:
    """Replace invisible characters so that AST can correctly parse the code"""
    invisibleToSpace = {
        '\uFEFF': ' ',  # Byte order mark (zero-width but might act as a separator)
    }

    invisibleToEmpty = {
        '\u200B': '',  # Zero width space
        '\u200C': '',  # Zero width non-joiner
        '\u200D': '',  # Zero width joiner
        '\u2060': '',  # Word joiner
        '\u180E': '',  # Mongolian vowel separator
        '\u061C': '',  # Arabic letter mark
        '\u200E': '',  # Left-to-right mark
        '\u200F': '',  # Right-to-left mark
        '\u202A': '',  # Left-to-right embedding
        '\u202B': '',  # Right-to-left embedding
        '\u202C': '',  # Pop directional formatting
        '\u202D': '',  # Left-to-right override
        '\u202E': '',  # Right-to-left override
        '\u2061': '',  # Function application
        '\u2062': '',  # Invisible times
        '\u2063': '',  # Invisible separator
        '\u2064': '',  # Invisible plus
        '\u034F': '',  # Combining grapheme joiner
    }

    for char, replacement in {**invisibleToSpace, **invisibleToEmpty}.items():
        text = text.replace(char, replacement)

    return text
