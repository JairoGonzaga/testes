import pytest

from alvo import apnumber

WORDS = (
    "zero", "one", "two", "three", "four",
    "five", "six", "seven", "eight", "nine",
)


@pytest.mark.parametrize("number,word", list(enumerate(WORDS)))
def test_single_digits_are_spelled_out(number, word):
    assert apnumber(number) == word


def test_nine_is_spelled_out():
    # The reported bug: apnumber(9) returned '9' instead of 'nine'.
    assert apnumber(9) == "nine"


def test_nine_as_float_is_spelled_out():
    assert apnumber(9.0) == "nine"


def test_nine_as_string_is_spelled_out():
    assert apnumber("9") == "nine"


def test_ten_is_not_spelled_out():
    # Numbers outside the 0..9 range stay as digits.
    assert apnumber(10) == "10"
    assert apnumber(42) == "42"


def test_non_finite_values_are_unchanged():
    assert apnumber(float("nan")) == "NaN"
    assert apnumber(float("inf")) == "+Inf"
    assert apnumber(float("-inf")) == "-Inf"
