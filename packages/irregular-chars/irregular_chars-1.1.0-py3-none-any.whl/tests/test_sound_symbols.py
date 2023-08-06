from irregular_chars import combine_sound_symbols


def test_combine_sound_symbols():
    assert combine_sound_symbols("ガギグゲゴ") == "ガギグゲゴ"
    assert combine_sound_symbols("がぎぐげご") == "がぎぐげご"
    assert combine_sound_symbols("ザジズゼゾ") == "ザジズゼゾ"
    assert combine_sound_symbols("ざじずぜぞ") == "ざじずぜぞ"
    assert combine_sound_symbols("ダヂヅデド") == "ダヂヅデド"
    assert combine_sound_symbols("だぢづでど") == "だぢづでど"
    assert combine_sound_symbols("バビブベボ") == "バビブベボ"
    assert combine_sound_symbols("ばびぶべぼ") == "ばびぶべぼ"
    assert combine_sound_symbols("パピプペポ") == "パピプペポ"
    assert combine_sound_symbols("ぱぴぷぺぽ") == "ぱぴぷぺぽ"
