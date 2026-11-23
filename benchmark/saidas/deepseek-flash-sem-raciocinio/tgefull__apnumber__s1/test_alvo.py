import math
import pytest

from alvo import (
    _format_not_finite,
    _APNUMBER_WORDS,
    apnumber,
)


class TestFormatNotFinite:
    def test_nan(self):
        assert _format_not_finite(math.nan) == "NaN"

    def test_negative_inf(self):
        assert _format_not_finite(float("-inf")) == "-Inf"

    def test_positive_inf(self):
        assert _format_not_finite(float("inf")) == "+Inf"

    def test_finite_returns_empty(self):
        assert _format_not_finite(0.0) == ""
        assert _format_not_finite(5.0) == ""
        assert _format_not_finite(-3.5) == ""


class TestApnumberWords:
    @pytest.mark.parametrize("i, word", list(enumerate(_APNUMBER_WORDS)))
    def test_single_digits(self, i, word):
        assert apnumber(i) == word
        assert apnumber(str(i)) == word
        assert apnumber(float(i)) == word

    def test_zero_negative_zero(self):
        assert apnumber(0) == "zero"
        assert apnumber(-0) == "zero"
        assert apnumber(-0.0) == "zero"

    def test_words_content(self):
        assert _APNUMBER_WORDS == (
            "zero", "one", "two", "three", "four",
            "five", "six", "seven", "eight", "nine",
        )


class TestApnumberOutOfRange:
    @pytest.mark.parametrize("value", [10, 11, 100, -1, -10, -5])
    def test_returns_str(self, value):
        assert apnumber(value) == str(value)

    def test_boundaries(self):
        assert apnumber(9) == "nine"
        assert apnumber(10) == "10"
        assert apnumber(-1) == "-1"
        assert apnumber(0) == "zero"

    def test_large_int(self):
        assert apnumber(12345) == "12345"

    def test_float_truncation(self):
        assert apnumber(3.7) == "three"
        assert apnumber(9.9) == "nine"
        assert apnumber(10.0) == "10"
        assert apnumber(-0.5) == "zero"
        assert apnumber(9.999) == "nine"
        assert apnumber(10.1) == "10"

    def test_numeric_strings(self):
        assert apnumber("3") == "three"
        assert apnumber("9") == "nine"
        assert apnumber("10") == "10"
        assert apnumber("-2") == "-2"
        assert apnumber("3.9") == "three"


class TestApnumberNotFinite:
    def test_nan(self):
        assert apnumber(float("nan")) == "NaN"
        assert apnumber("nan") == "NaN"

    def test_positive_inf(self):
        assert apnumber(float("inf")) == "+Inf"
        assert apnumber("inf") == "+Inf"

    def test_negative_inf(self):
        assert apnumber(float("-inf")) == "-Inf"
        assert apnumber("-inf") == "-Inf"


class TestApnumberErrors:
    def test_non_numeric_string(self):
        assert apnumber("hello") == "hello"

    def test_non_numeric_string_with_digits(self):
        assert apnumber("1abc") == "1abc"

    def test_empty_string(self):
        assert apnumber("") == ""

    def test_none(self):
        assert apnumber(None) == "None"

    def test_object(self):
        class Dummy:
            def __str__(self):
                return "dummy"

        assert apnumber(Dummy()) == "dummy"

    def test_list(self):
        assert apnumber([1, 2]) == "[1, 2]"
