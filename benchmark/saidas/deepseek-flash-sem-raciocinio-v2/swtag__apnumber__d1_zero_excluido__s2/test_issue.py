import pytest

from alvo import apnumber


def test_apnumber_zero_is_spelled_out():
    # Issue: apnumber(0) should return 'zero', not '0'.
    assert apnumber(0) == "zero"


def test_apnumber_zero_float_is_spelled_out():
    assert apnumber(0.0) == "zero"


def test_apnumber_zero_numeric_string():
    # Everything else that converts to int 0 should behave the same way.
    assert apnumber("0") == "zero"


@pytest.mark.parametrize(
    "value,expected",
    [(1, "one"), (5, "five"), (9, "nine")],
)
def test_other_single_digits_still_work(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize("value", [10, -1, 42])
def test_numbers_outside_range_are_strings(value):
    assert apnumber(value) == str(value)
