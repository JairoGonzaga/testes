```python
import pytest

from alvo import ordinal, _format_not_finite


@pytest.mark.parametrize(
    "value, expected",
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
        (16, "16th"),
        (17, "17th"),
        (18, "18th"),
        (19, "19th"),
        (20, "20th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (24, "24th"),
        (25, "25th"),
        (30, "30th"),
        (31, "31st"),
        (32, "32nd"),
        (33, "33rd"),
        (40, "40th"),
        (100, "100th"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
        (104, "104th"),
        (110, "110th"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (114, "114th"),
        (120, "120th"),
        (121, "121st"),
        (122, "122nd"),
        (123, "123rd"),
        (124, "124th"),
        (200, "200th"),
        (201, "201st"),
        (202, "202nd"),
        (203, "203rd"),
        (211, "211th"),
        (212, "212th"),
        (213, "213th"),
        (1000, "1000th"),
        (1001, "1001st"),
        (1002, "1002nd"),
        (1003, "1003rd"),
        (1011, "1011th"),
        (1012, "1012th"),
        (1013, "1013th"),
        (1014, "1014th"),
        (1021, "1021st"),
        (1022, "1022nd"),
        (1023, "1023rd"),
        (1024, "1024th"),
    ],
)
def test_ordinal_positive_integers(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (-1, "-1th"),
        (-2, "-2th"),
        (-3, "-3th"),
        (-4, "-4th"),
        (-5, "-5th"),
        (-6, "-6th"),
        (-7, "-7rd"),
        (-8, "-8nd"),
        (-9, "-9st"),
        (-10, "-10th"),
        (-11, "-11th"),
        (-12, "-12th"),
        (-13, "-13th"),
        (-14, "-14th"),
        (-17, "-17rd"),
        (-18, "-18nd"),
        (-19, "-19st"),
        (-20, "-20th"),
        (-21, "-21th"),
        (-87, "-87th"),
        (-88, "-88th"),
        (-89, "-89th"),
        (-98, "-98nd"),
        (-99, "-99st"),
        (-100, "-100th"),
        (-101, "-101th"),
        (-109, "-109st"),
        (-111, "-111th"),
        (-189, "-189th"),
    ],
)
def test_ordinal_negative_integers(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0.0, "0th"),
        (0.9, "0th"),
        (-0.1, "0th"),
        (-0.9, "0th"),
        (1.0, "1st"),
        (1.1, "1st"),
        (1.9, "1st"),
        (2.0, "2nd"),
        (2.9, "2nd"),
        (3.1, "3rd"),
        (3.9, "3rd"),
        (4.9, "4th"),
        (9.9, "9th"),
        (10.9, "10th"),
        (11.1, "11th"),
        (11.9, "11th"),
        (12.1, "12th"),
        (12.9, "12th"),
        (13.1, "13th"),
        (13.9, "13th"),
        (14.9, "14th"),
        (20.9, "20th"),
        (21.1, "21st"),
        (21.9, "21st"),
        (22.9, "22nd"),
        (23.9, "23rd"),
        (24.9, "24th"),
        (-1.1, "-1th"),
        (-1.9, "-1th"),
        (-7.9, "-7rd"),
        (-8.1, "-8nd"),
        (-9.1, "-9st"),
        (-9.9, "-9st"),
        (-10.1, "-10th"),
    ],
)
def test_ordinal_float_values(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("0", "0th"),
        ("1", "1st"),
        ("2", "2nd"),
        ("3", "3rd"),
        ("4", "4th"),
        ("10", "10th"),
        ("11", "11th"),
        ("12", "12th"),
        ("13", "13th"),
        ("14", "14th"),
        ("21", "21st"),
        ("22", "22nd"),
        ("23", "23rd"),
        ("24", "24th"),
        ("101", "101st"),
        ("111", "111th"),
        ("112", "112th"),
        ("113", "113th"),
        ("121", "121st"),
        (" 1 ", "1st"),
        ("01", "1st"),
        ("+1", "1st"),
        ("-0", "0th"),
        ("-1", "-1th"),
        ("-9", "-9st"),
        ("-89", "-89th"),
    ],
)
def test_ordinal_numeric_strings(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("abc", "abc"),
        ("", ""),
        (" ", " "),
        ("1.5", "1.5"),
        ("1e3", "1e3"),
        ("0x10", "0x10"),
        (None, "None"),
        ([1, 2], "[1, 2]"),
        ((1, 2), "(1, 2)"),
        ({}, "{}"),
        (1 + 2j, "(1+2j)"),
    ],
)
def test_ordinal_invalid_values_return_string_representation(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (float("nan"), "NaN"),
        (float("inf"), "+Inf"),
        (float("-inf"), "-Inf"),
        ("nan", "NaN"),
        ("NaN", "NaN"),
        ("inf", "+Inf"),
        ("+inf", "+Inf"),
        ("Infinity", "+Inf"),
        ("-inf", "-Inf"),
        ("-Infinity", "-Inf"),
    ],
)
def test_ordinal_non_finite_values(value, expected):
    assert ordinal(value) == expected


def test_ordinal_bool_values():
    assert ordinal(True) == "1st"
    assert ordinal(False) == "0th"


def test_ordinal_gender_argument_is_accepted_and_ignored():
    assert ordinal(1, gender="female") == "1st"
    assert ordinal(2, "female") == "2nd"
    assert ordinal(11, gender="male") == "11th"
    assert ordinal(21, "anything") == "21st"


@pytest.mark.parametrize(
    "value, expected",
    [
        (float("nan"), "NaN"),
        (float("inf"), "+Inf"),
        (float("-inf"), "-Inf"),
        (0.0, ""),
        (-0.0, ""),
        (1.0, ""),
        (-1.0, ""),
        (123.456, ""),
    ],
)
def test_format_not_finite_directly(value, expected):
    assert _format_not_finite(value) == expected
```