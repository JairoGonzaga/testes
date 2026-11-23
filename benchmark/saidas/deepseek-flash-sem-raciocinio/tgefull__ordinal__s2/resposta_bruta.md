```python
import math
import pytest

from alvo import ordinal, _format_not_finite, _SUFIXOS


def test_sufixos_constant():
    assert _SUFIXOS == ("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th")


def test_format_not_finite_nan():
    assert _format_not_finite(float("nan")) == "NaN"


def test_format_not_finite_neg_inf():
    assert _format_not_finite(float("-inf")) == "-Inf"


def test_format_not_finite_pos_inf():
    assert _format_not_finite(float("inf")) == "+Inf"


def test_format_not_finite_returns_empty_for_finite():
    assert _format_not_finite(1.5) == ""
    assert _format_not_finite(0.0) == ""
    assert _format_not_finite(-3.0) == ""


@pytest.mark.parametrize("value, expected", [
    (1, "1st"),
    (2, "2nd"),
    (3, "3rd"),
    (4, "4th"),
    (5, "5th"),
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
    (104, "104th"),
    (111, "111th"),
    (112, "112th"),
    (113, "113th"),
    (121, "121st"),
    (0, "0th"),
    (-1, "-1th"),
    (-2, "-2th"),
    (-3, "-3th"),
])
def test_ordinal_integers(value, expected):
    assert ordinal(value) == expected


def test_ordinal_nan():
    assert ordinal(float("nan")) == "NaN"


def test_ordinal_pos_inf():
    assert ordinal(float("inf")) == "+Inf"


def test_ordinal_neg_inf():
    assert ordinal(float("-inf")) == "-Inf"


def test_ordinal_string_number():
    assert ordinal("1") == "1st"
    assert ordinal("12") == "12th"
    assert ordinal("23") == "23rd"


def test_ordinal_float_finite():
    assert ordinal(1.9) == "1st"
    assert ordinal(2.0) == "2nd"
    assert ordinal(22.7) == "22nd"


def test_ordinal_non_numeric_string():
    assert ordinal("foo") == "foo"
    assert ordinal("") == ""


def test_ordinal_none():
    assert ordinal(None) == "None"


def test_ordinal_bad_type():
    assert ordinal([1, 2]) == "[1, 2]"
    assert ordinal({}) == "{}"


def test_ordinal_gender_ignored():
    assert ordinal(1, gender="female") == "1st"
    assert ordinal(2, gender="other") == "2nd"
```
```