import math
import pytest

from alvo import (
    intword,
    powers,
    human_powers,
    _format_not_finite,
)


class TestFormatNotFinite:
    def test_nan(self):
        assert _format_not_finite(float("nan")) == "NaN"

    def test_negative_inf(self):
        assert _format_not_finite(float("-inf")) == "-Inf"

    def test_positive_inf(self):
        assert _format_not_finite(float("inf")) == "+Inf"

    def test_finite_returns_empty(self):
        assert _format_not_finite(0.0) == ""
        assert _format_not_finite(1.5) == ""
        assert _format_not_finite(-3.0) == ""


class TestNonFinite:
    def test_nan(self):
        assert intword(float("nan")) == "NaN"

    def test_positive_inf(self):
        assert intword(float("inf")) == "+Inf"

    def test_negative_inf(self):
        assert intword(float("-inf")) == "-Inf"

    def test_nan_string(self):
        assert intword("nan") == "NaN"

    def test_inf_string(self):
        assert intword("inf") == "+Inf"

    def test_negative_inf_string(self):
        assert intword("-inf") == "-Inf"


class TestInvalid:
    def test_none(self):
        assert intword(None) == "None"

    def test_non_numeric_string(self):
        assert intword("hello") == "hello"

    def test_empty_string(self):
        assert intword("") == ""

    def test_list(self):
        result = intword([1, 2])
        assert result == "[1, 2]"


class TestSmallValues:
    def test_zero(self):
        assert intword(0) == "0"

    def test_one(self):
        assert intword(1) == "1"

    def test_below_thousand(self):
        assert intword(999) == "999"

    def test_negative_small(self):
        assert intword(-1) == "-1"
        assert intword(-999) == "-999"

    def test_float_truncation(self):
        assert intword(999.9) == "999"
        assert intword(12.7) == "12"


class TestThousands:
    def test_thousand(self):
        assert intword(1000) == "1.0 thousand"

    def test_1500(self):
        assert intword(1500) == "1.5 thousand"

    def test_negative_thousand(self):
        assert intword(-1000) == "-1.0 thousand"

    def test_999999(self):
        assert intword(999999) == "1000.0 thousand"

    def test_million(self):
        assert intword(1000000) == "1.0 million"

    def test_billion(self):
        assert intword(1000000000) == "1.0 billion"

    def test_trillion(self):
        assert intword(10**12) == "1.0 trillion"


class TestRoundingUp:
    def test_rounding_promotes_ordinal(self):
        # 999500 thousand rounds to 1000.0 -> promotes to 1.0 million
        result = intword(999500)
        assert "million" in result
        assert result == "1.0 million"

    def test_border_rounding(self):
        # 999499 rounds to 999.5 thousand
        result = intword(999499)
        assert "thousand" in result

    def test_below_rounding(self):
        result = intword(999499)
        assert result == "999.5 thousand"


class TestCustomFormat:
    def test_no_decimal(self):
        assert intword(1500, "%d") == "1 thousand"

    def test_two_decimals(self):
        assert intword(1500, "%.2f") == "1.50 thousand"

    def test_no_decimals_million(self):
        assert intword(2000000, "%d") == "2 million"


class TestGoogol:
    def test_googol(self):
        assert intword(10**100) == "1.0 googol"

    def test_largest_ordinal(self):
        # googol is largest; no promotion beyond
        assert intword(10**100) == "1.0 googol"

    def test_beyond_googol(self):
        result = intword(10**101)
        assert "googol" in result


class TestPowersAndHuman:
    def test_powers(self):
        assert powers == [10**x for x in (3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 100)]

    def test_human_powers(self):
        assert human_powers[0] == "thousand"
        assert human_powers[-1] == "googol"
        assert len(human_powers) == 12
