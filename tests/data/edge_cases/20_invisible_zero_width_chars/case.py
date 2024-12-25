# This script defines a function to demonstrate the inclusion of various invisible and zero-width Unicode characters.

def demonstrate_invisible_chars():
    # Each variable below includes an invisible or zero-width Unicode character.
    zero_width_space = ​1  # Zero Width Space
    zero_width_non_joiner = ‌2  # Zero Width Non-Joiner
    zero_width_joiner = ‍3  # Zero Width Joiner
    byte_order_mark = ﻿4  # Zero Width No-Break Space (Byte Order Mark)
    word_joiner = ⁠5  # Word Joiner
    mongolian_vowel_separator = ᠎6  # Mongolian Vowel Separator
    arabic_letter_mark = 7 ؜  # Arabic Letter Mark
    left_to_right_mark = ‎8  # Left-to-Right Mark
    right_to_left_mark = ‏9  # Right-to-Left Mark
    left_to_right_embedding = ‪10  # Left-to-Right Embedding
    right_to_left_embedding = ‫11  # Right-to-Left Embedding
    pop_directional_formatting = ‬12  # Pop Directional Formatting
    left_to_right_override = ‭13  # Left-to-Right Override
    right_to_left_override = ‮14  # Right-to-Left Override
    function_application = ⁡15  # Function Application
    invisible_times = ⁢16  # Invisible Times
    invisible_separator = ⁣17  # Invisible Separator
    invisible_plus = ⁤18  # Invisible Plus
    combining_grapheme_joiner = ͏  19 # Combining Grapheme Joiner

    # The following dictionary maps character descriptions to their corresponding Unicode characters.
    invisible_chars = {
        "Zero Width Space": zero_width_space,
        "Zero Width Non-Joiner": zero_width_non_joiner,
        "Zero Width Joiner": zero_width_joiner,
        "Byte Order Mark": byte_order_mark,
        "Word Joiner": word_joiner,
        "Mongolian Vowel Separator": mongolian_vowel_separator,
        "Arabic Letter Mark": arabic_letter_mark,
        "Left-to-Right Mark": left_to_right_mark,
        "Right-to-Left Mark": right_to_left_mark,
        "Left-to-Right Embedding": left_to_right_embedding,
        "Right-to-Left Embedding": right_to_left_embedding,
        "Pop Directional Formatting": pop_directional_formatting,
        "Left-to-Right Override": left_to_right_override,
        "Right-to-Left Override": right_to_left_override,
        "Function Application": function_application,
        "Invisible Times": invisible_times,
        "Invisible Separator": invisible_separator,
        "Invisible Plus": invisible_plus,
        "Combining Grapheme Joiner": combining_grapheme_joiner,
    }

    return invisible_chars

# Demonstrate the usage
invisible_chars = demonstrate_invisible_chars()
for name, char in invisible_chars.items():
    print(f"{name}: {repr(char)}")
