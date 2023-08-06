from irregular_chars.ivs import is_cjk_or_supplementary_ivs, is_unicode_ivs, remove_ivs


def test_is_unicode_ivs():
    assert is_unicode_ivs(0xE0100)
    assert is_unicode_ivs(0xE0101)
    assert is_unicode_ivs(0xE0102)
    assert is_unicode_ivs(0xE0103)
    assert is_unicode_ivs(0xE0104)
    assert is_unicode_ivs(0xE0105)
    assert is_unicode_ivs(0xE0106)
    assert is_unicode_ivs(0xE0107)
    assert is_unicode_ivs(0xE0108)
    assert is_unicode_ivs(0xE0109)
    assert is_unicode_ivs(0xE010A)
    assert is_unicode_ivs(0xE010B)
    assert is_unicode_ivs(0xE010C)
    assert is_unicode_ivs(0xE010D)
    assert is_unicode_ivs(0xE010E)
    assert is_unicode_ivs(0xE010F)
    assert is_unicode_ivs(0xE0110)
    assert is_unicode_ivs(0xE0111)
    assert is_unicode_ivs(0xE0112)
    assert is_unicode_ivs(0xE0113)
    assert is_unicode_ivs(0xE0114)
    assert is_unicode_ivs(0xE0115)
    assert is_unicode_ivs(0xE0116)
    assert is_unicode_ivs(0xE0117)
    assert is_unicode_ivs(0xE0118)
    assert is_unicode_ivs(0xE0119)
    assert is_unicode_ivs(0xE011A)
    assert is_unicode_ivs(0xE011B)
    assert is_unicode_ivs(0xE011C)
    assert is_unicode_ivs(0xE011D)
    assert is_unicode_ivs(0xE011E)
    assert is_unicode_ivs(0xE011F)
    assert is_unicode_ivs(0xE0120)
    assert is_unicode_ivs(0xE0121)
    assert is_unicode_ivs(0xE0122)
    assert is_unicode_ivs(0xE0123)
    assert is_unicode_ivs(0xE0124)
    assert is_unicode_ivs(0xE0125)
    assert is_unicode_ivs(0xE0126)
    assert is_unicode_ivs(0xE0127)
    assert is_unicode_ivs(0xE0128)


def test_is_cjk_or_supplementary_ivs():
    # 0x20000 <= code_point <= 0x2FA1F
    assert is_cjk_or_supplementary_ivs(0x20000)
    assert is_cjk_or_supplementary_ivs(0x20001)
    assert is_cjk_or_supplementary_ivs(0x20002)
    assert is_cjk_or_supplementary_ivs(0x20003)
    assert is_cjk_or_supplementary_ivs(0x20004)
    assert is_cjk_or_supplementary_ivs(0x20005)
    assert is_cjk_or_supplementary_ivs(0x20006)
    assert is_cjk_or_supplementary_ivs(0x20007)
    assert is_cjk_or_supplementary_ivs(0x20008)
    assert is_cjk_or_supplementary_ivs(0x20009)
    assert is_cjk_or_supplementary_ivs(0x2000A)
    assert is_cjk_or_supplementary_ivs(0x2000B)
    assert is_cjk_or_supplementary_ivs(0x2000C)
    assert is_cjk_or_supplementary_ivs(0x2000D)
    assert is_cjk_or_supplementary_ivs(0x2000E)
    assert is_cjk_or_supplementary_ivs(0x2000F)
    assert is_cjk_or_supplementary_ivs(0x20010)
    assert is_cjk_or_supplementary_ivs(0x20011)
    assert is_cjk_or_supplementary_ivs(0x20012)
    assert is_cjk_or_supplementary_ivs(0x20013)
    assert is_cjk_or_supplementary_ivs(0x20014)
    assert is_cjk_or_supplementary_ivs(0x20015)
    assert is_cjk_or_supplementary_ivs(0x20016)
    assert is_cjk_or_supplementary_ivs(0x20017)
    assert is_cjk_or_supplementary_ivs(0x20018)
    assert is_cjk_or_supplementary_ivs(0x20019)
    assert is_cjk_or_supplementary_ivs(0x2001A)
    assert is_cjk_or_supplementary_ivs(0x2001B)
    assert is_cjk_or_supplementary_ivs(0x2001C)
    assert is_cjk_or_supplementary_ivs(0x2001D)


def test_remove_ivs():
    assert remove_ivs("test") == "test"
    assert remove_ivs("test\U000E0100") == "test"
    assert remove_ivs("test\U000E0100\U000E0101") == "test"
    assert remove_ivs("test\U000E0100\U000E0101\U000E0102") == "test"
    assert remove_ivs("test\U000E0100\U000E0101\U000E0102\U000E0103") == "test"
    assert (
        remove_ivs("test\U000E0100\U000E0101\U000E0102\U000E0103\U000E0104") == "test"
    )
    assert (
        remove_ivs("test\U000E0100\U000E0101\U000E0102\U000E0103\U000E0104\U000E0105")
        == "test"
    )
    assert (
        remove_ivs(
            "test\U000E0100\U000E0101\U000E0102\U000E0103\U000E0104\U000E0105\U000E0106"
        )
        == "test"
    )
    assert (
        remove_ivs(
            "test\U000E0100\U000E0101\U000E0102\U000E0103\U000E0104\U000E0105\U000E0106\U000E0107"
        )
        == "test"
    )
    assert (
        remove_ivs(
            "test\U000E0100\U000E0101\U000E0102\U000E0103\U000E0104\U000E0105\U000E0106\U000E0107\U000E0108"
        )
        == "test"
    )
