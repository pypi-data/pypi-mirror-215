# irregular-chars

irregular-chars is a library for cleaning text, such as removing zero-width characters or converting full-width characters to half-width.

## Installation

You can install the package via pip:
```bash
pip install irregular_chars
```

## Usage

### remove zero width space
```py
from irregular_chars import remove_zero_width_spaces

text = "Hello\u200BWorld"
clean_text = remove_zero_width(text)
print(clean_text)  # Outputs: HelloWorld
```

### change width
- convert alphanumerics width full to small
```py
from irregular_chars import full_to_small_width_alphanumerics
assert full_to_small_width_alphanumerics("０") == "0"  # True
```
- convert kana width small to full
```py
from irregular_chars import half_to_full_width_kanas
assert half_to_full_width_kanas("ｱ") == "ア"  # True
```
- normalize kana and alphanumerics width
```py
from irregular_chars import normalize_width_all
assert normalize_width_all("ｱ０") == "ア0"  # True
```
### combine sound symbols

```py
from irregular_chars import combine_sound_symbols
assert combine_sound_symbols("ガギグゲゴ") == "ガギグゲゴ"  # True
```

### ivs
- detect ivs (unicode ivs)
The Unicode code point of the character is
in the range of the variant selector (E0100-E01EF).
You can just ignore this kind of variant selectors.

```py
from irregular_chars.ivs import is_unicode_ivs
assert is_unicode_ivs(0xE0100)  # True
```
- detect ivs (cjk or supplementary ivs)
The range of CJK unified ideographs extension B-F
and supplementary ideographic plane (20000-2FA1F).

They are strongly combined with the previous character.
So you can not remove or replace just only this characters...
```py
from irregular_chars.ivs import is_cjk_or_supplementary_ivs
assert is_cjk_or_supplementary_ivs(0x20000)  # True
```
- ignore unicode ivs and raise if a cjk or supplementary ivs is found.
```py
from irregular_chars.ivs import remove_ivs
assert remove_ivs("test\U000E0100") == "test"  # True
```
