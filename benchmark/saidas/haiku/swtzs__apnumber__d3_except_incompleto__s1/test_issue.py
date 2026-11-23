import pytest

from alvo import apnumber


def test_none_is_returned_as_string():
    assert apnumber(None) == "None"


@pytest.mark.parametrize("value", [None, object()])
def test_non_convertible_values_return_str(value):
    assert apnumber(value) == str(value)


def test_non_numeric_string_is_returned_unchanged():
    assert apnumber("abc") == "abc"


@pytest.mark.parametrize(
    "value, expected",
    [(0, "zero"), (1, "one"), (9, "nine"), (10, "10"), (-1, "-1")],
)
def test_small_integers_are_spelled_out(value, expected):
    assert apnumber(value) == expected
