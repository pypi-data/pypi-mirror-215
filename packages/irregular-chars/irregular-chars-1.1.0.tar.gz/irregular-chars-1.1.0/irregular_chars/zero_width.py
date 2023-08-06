ZERO_WIDTH_SPACES = {
    "ZERO WIDTH SPACE": u"\u200B",
    "ZERO WIDTH NON-JOINER": u"\u200C",
    "ZERO WIDTH JOINER": u"\u200D",
    "ZERO WIDTH NO-BREAK SPACE": u"\uFEFF",
    "RIGHT-TO-LEFT MARK": u"\u200F",
    "LEFT-TO-RIGHT MARK": u"\u200E",
    "FUNCTION APPLICATION": u"\u2061",
    "SOFT HYPHEN": u"\u00AD",
    "MONGOLIAN VOWEL SEPARATOR": u"\u180E",
    "HAIR SPACE": u"\u200A",
    "NARROW NO-BREAK SPACE": u"\u202F",
    "MEDIUM MATHEMATICAL SPACE": u"\u205F",
    "WORD JOINER": u"\u2060",
    "COMBINING GRAPHEME JOINER": u"\u034F",
}


def remove_zero_width(text: str) -> str:
    for char in ZERO_WIDTH_SPACES.values():
        text = text.replace(char, "")
    return text
