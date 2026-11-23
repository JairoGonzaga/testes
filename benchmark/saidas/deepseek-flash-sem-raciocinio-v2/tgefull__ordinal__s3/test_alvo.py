import math

import pytest

from alvo import ordinal, _format_not_finite, _SUFIXOS


class TestSuffixTable:
    def test_suffix_table(self):
        assert _SUFIXOS == ("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th")


class TestFormatNotFinite:
    def test_nan(self):
        assert _format_not_finite(float("nan")) == "NaN"

    def test_negative_inf(self):
        assert _format_not_finite(float("-inf")) == "-Inf"

    def test_positive_inf(self):
        assert _format_not_finite(float("inf")) == "+Inf"

    def test_finite_returns_empty(self):
        assert _format_not_finite(3.0) == ""
        assert _format_not_finite(0.0) == ""


class TestOrdinalBasic:
    @pytest.mark.parametrize(
        "value, expected",
        [
            (1, "1st"),
            (2, "2nd"),
            (3, "3rd"),
            (4, "4th"),
            (5, "5th"),
            (9, "9th"),
            (10, "10th"),
            (11, "11th"),
            (12, "12th"),
            (13, "13th"),
            (14, "14th"),
            (20, "20th"),
            (21, "21st"),
            (22, "22nd"),
            (23, "23rd"),
            (24, "24th"),
            (100, "100th"),
            (101, "101st"),
            (102, "102nd"),
            (103, "103rd"),
            (111, "111th"),
            (112, "112th"),
            (113, "113th"),
            (121, "121st"),
            (0, "0th"),
            # negatives: value % 10 is non-negative in Python (e.g. -1 % 10 == 9)
            (-1, "-1th"),
            (-2, "-2th"),
            (-3, "-3th"),
            (-4, "-4th"),
            (-11, "-11th"),
            (-21, "-21th"),
        ],
    )
    def test_ordinal_int(self, value, expected):
        assert ordinal(value) == expected

    def test_gender_default(self):
        assert ordinal(1) == "1st"

    def test_gender_ignored(self):
        assert ordinal(1, gender="female") == "1st"
        assert ordinal(2, "x") == "2nd"
        assert ordinal(1, gender=None) == "1st"

    def test_kwarg_gender(self):
        assert ordinal(3, gender="male") == "3rd"


class TestOrdinalNumericTypes:
    def test_float_integral(self):
        assert ordinal(1.9) == "1st"
        assert ordinal(2.0) == "2nd"
        assert ordinal(11.99) == "11th"

    def test_negative_float(self):
        assert ordinal(-2.7) == "-2th"

    def test_string_number(self):
        assert ordinal("1") == "1st"
        assert ordinal("22") == "22nd"
        assert ordinal("13") == "13th"
        assert ordinal("+3") == "3rd"

    def test_string_number_whitespace(self):
        assert ordinal("  5  ") == "5th"
        assert ordinal("\t7\n") == "7th"

    def test_bool(self):
        assert ordinal(True) == "1st"
        assert ordinal(False) == "0th"


class TestOrdinalNonFinite:
    def test_nan_float(self):
        assert ordinal(float("nan")) == "NaN"

    def test_inf_float(self):
        assert ordinal(float("inf")) == "+Inf"

    def test_negative_inf_float(self):
        assert ordinal(float("-inf")) == "-Inf"

    def test_inf_string(self):
        assert ordinal("inf") == "+Inf"
        assert ordinal("-inf") == "-Inf"
        assert ordinal("nan") == "NaN"


class TestOrdinalErrors:
    def test_none(self):
        assert ordinal(None) == "None"

    def test_non_numeric_string(self):
        assert ordinal("abc") == "abc"

    def test_empty_string(self):
        assert ordinal("") == ""

    def test_string_float(self):
        # float("3.9") is finite, then int("3.9") raises ValueError
        assert ordinal("3.9") == "3.9"
        assert ordinal("1.0") == "1.0"

    def test_list(self):
        assert ordinal([1, 2]) == "[1, 2]"

    def test_dict(self):
        assert ordinal({"a": 1}) == "{'a': 1}"
