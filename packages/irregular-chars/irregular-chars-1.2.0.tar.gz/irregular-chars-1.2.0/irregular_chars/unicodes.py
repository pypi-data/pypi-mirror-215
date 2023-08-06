import unicodedata


def to_unicode(text: str):
    return unicodedata.normalize("NFKC", text)
