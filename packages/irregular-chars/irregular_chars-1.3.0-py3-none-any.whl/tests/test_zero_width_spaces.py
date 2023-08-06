import pytest

from irregular_chars import remove_zero_width_spaces
from irregular_chars.space import ZERO_WIDTH_SPACES


@pytest.mark.parametrize("name, char", ZERO_WIDTH_SPACES.items())
def test_remove_zero_width_spaces(name, char):
    test_str = f"Hello{char}World"
    expected_str = "HelloWorld"
    assert remove_zero_width_spaces(test_str) == expected_str


def test_remove_zero_width_spaces_multiple_and_mixed():
    test_str = f"Hello{ZERO_WIDTH_SPACES['ZERO WIDTH SPACE']}W{ZERO_WIDTH_SPACES['ZERO WIDTH JOINER']}orld"
    expected_str = "HelloWorld"
    assert remove_zero_width_spaces(test_str) == expected_str


def test_remove_zero_width_spaces_no_change():
    test_str = "Hello World"
    expected_str = "Hello World"
    assert remove_zero_width_spaces(test_str) == expected_str


def test_remove_zero_width_spaces_use_quotations():
    origin = '"​"""⁡""­"'
    expect = '"""""""'
    assert expect == remove_zero_width_spaces(origin)
