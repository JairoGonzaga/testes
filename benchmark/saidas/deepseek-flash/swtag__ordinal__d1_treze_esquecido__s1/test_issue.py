import pytest

from alvo import ordinal


def test_ordinal_13_is_13th():
    """Core case from the issue report: 13 must take the 'th' suffix."""
    assert ordinal(13) == "13th"


@pytest.mark.parametrize("value", [11, 12, 13])
def test_teens_always_use_th(value):
    assert ordinal(value) == f"{value}th"


@pytest.mark.parametrize("value", [111, 112, 113, 211, 212, 213, 1013, 1011, 1012])
def test_numbers_ending_in_teens_use_th(value):
    """11, 12 and 13 always take 'th', regardless of the preceding digits."""
    assert ordinal(value) == f"{value}th"


@pytest.mark.parametrize(
    "value,expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (10, "10th"),
        (14, "14th"),
        (15, "15th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (24, "24th"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
        (121, "121st"),
        (122, "122nd"),
        (123, "123rd"),
        (1000, "1000th"),
    ],
)
def test_regular_suffixes(value, expected):
    assert ordinal(value) == expected


def test_string_input_with_teens():
    """Digit-only strings are converted to int, so the teen rule still applies."""
    assert ordinal("13") == "13th"
    assert ordinal("111") == "111th"


def test_float_input_with_teens():
    assert ordinal(13.0) == "13th"
    assert ordinal(12.0) == "12th"
    assert ordinal(11.0) == "11th"


def test_gender_argument_does_not_break_teen_rule():
    assert ordinal(13, gender="female") == "13th"
    assert ordinal(1, gender="female") == "1st"


def test_non_numeric_input_still_returned_as_string():
    assert ordinal("abc") == "abc"


def test_not_finite_values():
    assert ordinal(float("nan")) == "NaN"
    assert ordinal(float("inf")) == "+Inf"
    assert ordinal(float("-inf")) == "-Inf"
