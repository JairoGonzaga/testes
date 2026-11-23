import pytest

from alvo import apnumber


def test_apnumber_none_returns_str_none():
    assert apnumber(None) == "None"


@pytest.mark.parametrize("value", [None, [1, 2], (3,)])
def test_apnumber_uncastable_values_return_str(value):
    assert apnumber(value) == str(value)


def test_apnumber_non_numeric_string_returned_unchanged():
    assert apnumber("abc") == "abc"
