```python
import math
import pytest

from alvo import ordinal, _format_not_finite, _SUFIXOS


class TestFormatNotFinite:
    def test_nan(self):
        assert _format_not_finite(float("nan")) == "NaN"

    def test_neg_inf(self):
        assert _format_not_finite(float("-inf")) == "-Inf"

    def test_pos_inf(self):
        assert _format_not_finite(float("inf")) == "+Inf"

    def test_finite_returns_empty(self):
        assert _format_not_finite(0.0) == ""
        assert _format_not_finite(42.0) == ""
        assert _format_not_finite(-3.5) == ""


class TestOrdinalBasic:
    @pytest.mark.parametrize("value,expected", [
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
        (0, "0th"),
    ])
    def test_small_numbers(self, value, expected):
        assert ordinal(value) == expected

    @pytest.mark.parametrize("value,expected", [
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (211, "211th"),
        (1011, "1011th"),
        (1012, "1012th"),
        (1013, "1013th"),
    ])
    def test_teens_exceptions(self, value, expected):
        assert ordinal(value) == expected

    @pytest.mark.parametrize("value,expected", [
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (24, "24th"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
        (104, "104th"),
        (121, "121st"),
        (1001, "1001st"),
    ])
    def test_large_endings(self, value, expected):
        assert ordinal(value) == expected


class TestOrdinalStringsAndFloats:
    @pytest.mark.parametrize("value,expected", [
        ("1", "1st"),
        ("2", "2nd"),
        ("3", "3rd"),
        ("11", "11th"),
        ("21", "21st"),
        ("-1", "-1st"),
        ("-2", "-2nd"),
        ("-3", "-3rd"),
        ("-4", "-4th"),
        ("-11", "-11th"),
        ("-21", "-21st"),
    ])
    def test_numeric_strings(self, value, expected):
        assert ordinal(value) == expected

    @pytest.mark.parametrize("value,expected", [
        (1.0, "1st"),
        (2.9, "2nd"),
        (3.99, "3rd"),
        (4.5, "4th"),
        (11.9, "11th"),
        (12.5, "12th"),
        (13.7, "13th"),
        (21.7, "21st"),
        (22.2, "22nd"),
        (23.1, "23rd"),
        (0.9, "0th"),
        (-1.5, "-1st"),
        (-2.5, "-2nd"),
        (-11.9, "-11th"),
    ])
    def test_floats_truncate(self, value, expected):
        assert ordinal(value) == expected


class TestOrdinalNonFinite:
    def test_nan(self):
        assert ordinal(float("nan")) == "NaN"

    def test_pos_inf(self):
        assert ordinal(float("inf")) == "+Inf"

    def test_neg_inf(self):
        assert ordinal(float("-inf")) == "-Inf"

    def test_nan_string(self):
        assert ordinal("nan") == "NaN"

    def test_inf_string(self):
        assert ordinal("inf") == "+Inf"

    def test_pos_inf_string(self):
        assert ordinal("+inf") == "+Inf"

    def test_neg_inf_string(self):
        assert ordinal("-inf") == "-Inf"

    def test_float_nan_via_object(self):
        assert ordinal(float("inf") * 0 if False else float("nan")) == "NaN"


class TestOrdinalErrorHandling:
    @pytest.mark.parametrize("value", ["abc", "", "12abc", "nanx", "some"])
    def test_non_numeric_strings_return_str(self, value):
        assert ordinal(value) == value

    @pytest.mark.parametrize("value", [None, [1, 2], {}, object()])
    def test_unsupported_types_return_str(self, value):
        assert ordinal(value) == str(value)


class TestOrdinalGender:
    @pytest.mark.parametrize("gender", ["male", "female", "other", "", None])
    def test_gender_ignored(self, gender):
        assert ordinal(1, gender=gender) == "1st"
        assert ordinal(2, gender) == "2nd"
        assert ordinal(11, gender=gender) == "11th"


def test_sufixos_constant():
    assert _SUFIXOS == ("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th")
    assert len(_SUFIXOS) == 10
```