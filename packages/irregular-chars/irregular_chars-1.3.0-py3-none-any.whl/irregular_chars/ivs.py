def is_unicode_ivs(code_point: int) -> bool:
    """
    The Unicode code point of the character is
    in the range of the variant selector (E0100-E01EF).
    You can just ignore this kind of variant selectors.
    """
    return 0xE0100 <= code_point <= 0xE01EF
    # q: show me code_point sample here
    # a: https://www.fileformat.info/info/unicode/char/e0100/index.htm


def is_cjk_or_supplementary_ivs(code_point: int) -> bool:
    """
    The range of CJK unified ideographs extension B-F
    and supplementary ideographic plane (20000-2FA1F).

    They are strongly combined with the previous character.
    So you can not remove or replace just only this characters...
    """
    return 0x20000 <= code_point <= 0x2FA1F


def remove_ivs(text: str):
    output_string = ""
    for char in text:
        code_point = ord(char)
        if is_unicode_ivs(code_point):
            continue
        elif is_cjk_or_supplementary_ivs(code_point):
            """
            transelate above comment:
            There are thousands of variant characters,
            and this number will increase as new variant characters are defined.
            -> If this type of variant character is included, an Error will occur.
            """
            raise ValueError(
                f"Variant character is included in the text. "
                f"Please check the text: {text}"
            )
        output_string += char
    return output_string
