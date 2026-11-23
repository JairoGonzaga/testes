import math

import pytest

from alvo import (
    _format_not_finite,
    human_powers,
    intword,
    powers,
)


class TestModuleConstants:
    def test_powers_values(self):
        assert powers[:11] == [10 ** (3 * i) for i in range(11)]
        assert powers[11] == 10 ** 100

    def test_human_powers_length(self):
        assert len(human_powers) == 12

    def test_human_powers_sample(self):
        assert human_powers[0] == "thousand"
        assert human_powers[1] == "million"
        assert human_powers[10] == "decillion"
        assert human_powers[11] == "googol"


class TestFormatNotFinite:
    def test_nan(self):
        assert _format_not_finite(float("nan")) == "NaN"

    def test_positive_inf(self):
        assert _format_not_finite(float("inf")) == "+Inf"

    def test_negative_inf(self):
        assert _format_not_finite(float("-inf")) == "-Inf"

    def test_finite(self):
        assert _format_not_finite(1.0) == ""
        assert _format_not_finite(-3.5) == ""
        assert _format_not_finite(0) == ""


class TestIntwordBasic:
    def test_small_positive(self):
        assert intword(0) == "0"
        assert intword(1) == "1"
        assert intword(999) == "999"

    def test_small_negative(self):
        assert intword(-1) == "-1"
        assert intword(-999) == "-999"

    def test_thousand(self):
        assert intword(1000) == "1.0 thousand"
        assert intword(1234) == "1.2 thousand"

    def test_million(self):
        assert intword(1_000_000) == "1.0 million"
        assert intword(1_234_567) == "1.2 million"

    def test_billion(self):
        assert intword(1_000_000_000) == "1.0 billion"
        assert intword(1_500_000_000) == "1.5 billion"
        assert intword(2_000_000_000) == "2.0 billion"

    def test_larger_units(self):
        assert intword(10 ** 12) == "1.0 trillion"
        assert intword(10 ** 15) == "1.0 quadrillion"
        assert intword(10 ** 18) == "1.0 quintillion"
        assert intword(10 ** 21) == "1.0 sextillion"
        assert intword(10 ** 24) == "1.0 septillion"
        assert intword(10 ** 27) == "1.0 octillion"
        assert intword(10 ** 30) == "1.0 nonillion"
        assert intword(10 ** 33) == "1.0 decillion"

    def test_googol(self):
        assert intword(10 ** 100) == "1.0 googol"

    def test_negative_big(self):
        assert intword(-1_000_000) == "-1.0 million"
        assert intword(-2_500_000) == "-2.5 million"


class TestIntwordRoundingUp:
    def test_rounds_to_next_unit_thousand(self):
        # 999_949 / 1000 = 999.949 -> rounds to 999.9, not 1000
        # 999_950 / 1000 = 999.95 -> rounds to 1000.0 -> becomes million
        assert intword(999_950) == "1.0 million"

    def test_rounds_to_next_unit_million(self):
        assert intword(999_950_000) == "1.0 billion"

    def test_no_round_when_below_threshold(self):
        assert intword(999_900) == "999.9 thousand"

    def test_largest_ordinal_no_promotion(self):
        # When ordinal == len(powers), no promotion happens.
        result = intword(2 * 10 ** 100)
        assert result == "2.0 googol"


class TestIntwordFormatting:
    def test_custom_format(self):
        assert intword(1500, format="%.0f") == "2 thousand"
        assert intword(1_234_567, format="%.2f") == "1.23 million"
        assert intword(1_000_000, format="%d") == "1 million"

    def test_custom_format_chopped(self):
        assert intword(1500, format="%.3f") == "1.500 thousand"


class TestIntwordNonNumeric:
    def test_string_non_numeric(self):
        assert intword("abc") == "abc"

    def test_none(self):
        assert intword(None) == "None"

    def test_list(self):
        assert intword([1, 2]) == "[1, 2]"

    def test_numeric_string(self):
        # float("1000") is finite -> int("1000") == 1000
        assert intword("1000") == "1.0 thousand"


class TestIntwordNonFinite:
    def test_nan(self):
        assert intword(float("nan")) == "NaN"

    def test_string_nan(self):
        assert intword("nan") == "NaN"

    def test_positive_inf(self):
        assert intword(float("inf")) == "+Inf"

    def test_string_inf(self):
        assert intword("inf") == "+Inf"

    def test_negative_inf(self):
        assert intword(float("-inf")) == "-Inf"

    def test_string_negative_inf(self):
        assert intword("-inf") == "-Inf"


class TestIntwordFloatInput:
    def test_float_truncated(self):
        assert intword(1999.9) == "1.9 thousand"

    def test_negative_float(self):
        assert intword(-1234.9) == "-1.2 thousand"

    def test_float_small(self):
        assert intword(999.9) == "999"

    def test_float_risky_nan(self):
        assert intword(float("NaN")) == "NaN"
