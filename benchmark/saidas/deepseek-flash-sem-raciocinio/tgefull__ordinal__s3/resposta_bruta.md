```python
import math

import pytest

from alvo import _format_not_finite, _SUFIXOS, ordinal


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
        assert _format_not_finite(-42.0) == ""


class TestSufixos:
    def test_sufixos_content(self):
        assert _SUFIXOS == ("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th")


class TestOrdinalBasic:
    @pytest.mark.parametrize(
        "value,expected",
        [
            (0, "0th"),
            (1, "1st"),
            (2, "2nd"),
            (3, "3rd"),
            (4, "4th"),
            (5, "5th"),
            (6, "6th"),
            (7, "7th"),
            (8, "8th"),
            (9, "9th"),
            (10, "10th"),
            (11, "11th"),
            (12, "12th"),
            (13, "13th"),
            (14, "14th"),
            (15, "15th"),
            (19, "19th"),
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
            (1000, "1000th"),
            (1001, "1001st"),
            (1011, "1011th"),
        ],
    )
    def test_ordinal(self, value, expected):
        assert ordinal(value) == expected

    def test_negative_numbers(self):
        # -1 % 10 == 9 -> "th"
        assert ordinal(-1) == "-1th"
        # -2 % 10 == 8 -> "th"
        assert ordinal(-2) == "-2th"
        # -3 % 10 == 7 -> "th"
        assert ordinal(-3) == "-3th"
        # -11 % 100 == 89 -> digit -11 % 10 == 9 -> "th"
        assert ordinal(-11) == "-11th"

    def test_negative_with_th_suffix(self):
        # -21 % 10 == 9 -> "th"
        assert ordinal(-21) == "-21th"
        # Verify the 11,12,13 rule with negatives is not triggered
        assert ordinal(-13) == "-13th"


class TestOrdinalFloat:
    def test_float_truncates(self):
        assert ordinal(1.9) == "1st"
        assert ordinal(2.1) == "2nd"
        assert ordinal(3.99) == "3rd"
        assert ordinal(11.5) == "11th"
        assert ordinal(0.9) == "0th"

    def test_nan(self):
        assert ordinal(float("nan")) == "NaN"

    def test_positive_inf(self):
        assert ordinal(float("inf")) == "+Inf"

    def test_negative_inf(self):
        assert ordinal(float("-inf")) == "-Inf"


class TestOrdinalString:
    def test_numeric_strings(self):
        assert ordinal("1") == "1st"
        assert ordinal("2") == "2nd"
        assert ordinal("3") == "3rd"
        assert ordinal("11") == "11th"
        assert ordinal("21") == "21st"
        assert ordinal(" 22 ") == "22nd"

    def test_non_numeric_string_returns_str(self):
        assert ordinal("hello") == "hello"
        assert ordinal("abc") == "abc"
        assert ordinal("") == ""

    def test_float_string(self):
        assert ordinal("1.9") == "1st"
        assert ordinal("2.0") == "2nd"

    def test_nan_string(self):
        assert ordinal("nan") == "NaN"

    def test_inf_string(self):
        assert ordinal("inf") == "+Inf"
        assert ordinal("-inf") == "-Inf"


class TestOrdinalTypeError:
    def test_none(self):
        assert ordinal(None) == "None"

    def test_list(self):
        assert ordinal([1, 2]) == "[1, 2]"

    def test_object(self):
        class Foo:
            def __str__(self):
                return "foo!"

        assert ordinal(Foo()) == "foo!"

    def test_dict(self):
        assert ordinal({"a": 1}) == "{'a': 1}"


class TestOrdinalGender:
    def test_gender_ignored(self):
        assert ordinal(1, gender="female") == "1st"
        assert ordinal(2, gender="male") == "2nd"
        assert ordinal(1, "female") == "1st"
        assert ordinal(3, "anything") == "3rd"
```