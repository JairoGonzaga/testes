import pytest

from alvo import apnumber


def test_none_is_returned_as_string():
    # Issue: apnumber(None) raises TypeError instead of returning 'None'.
    assert apnumber(None) == "None"


@pytest.mark.parametrize("value", [None, [], {}])
def test_unconvertible_values_are_returned_as_str(value):
    # Values that cannot be converted to a number are returned as str(value).
    assert apnumber(value) == str(value)


def test_non_numeric_string_is_returned_unchanged():
    # Existing behaviour that must keep working.
    assert apnumber("abc") == "abc"
