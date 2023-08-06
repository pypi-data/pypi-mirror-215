from .space import remove_zero_width_spaces
from .splitted import combine_sound_symbols
from .unicodes import to_unicode
from .width import (
    full_to_small_width_alphanumerics,
    half_to_full_width_kanas,
    normalize_width_all,
)


def replace_all(text: str):
    text = to_unicode(text)
    text = remove_zero_width_spaces(text)
    text = combine_sound_symbols(text)
    text = normalize_width_all(text)
    text = full_to_small_width_alphanumerics(text)
    text = half_to_full_width_kanas(text)
    return text
