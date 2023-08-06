import unicodedata

from irregular_chars import to_unicode


def test_to_unicode():
    assert to_unicode("ハロー") == unicodedata.normalize("NFKC", "ハロー")
    assert to_unicode("１２３４５６７８９０") == unicodedata.normalize("NFKC", "１２３４５６７８９０")
    assert to_unicode("ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ") == unicodedata.normalize(
        "NFKC", "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
    )


def test_to_unicode_with_special_characters():
    assert to_unicode("\u2167") == unicodedata.normalize(
        "NFKC", "\u2167"
    )  # Unicode for Roman numeral VIII
    assert to_unicode("\u00B2") == unicodedata.normalize(
        "NFKC", "\u00B2"
    )  # Unicode for superscript 2
    assert to_unicode("\u00BC") == unicodedata.normalize(
        "NFKC", "\u00BC"
    )  # Unicode for 1/4 fraction
