import pytest

from alvo import ordinal


def test_non_numeric_string_returned_as_is():
    assert ordinal("something else") == "something else"


@pytest.mark.parametrize("value", ["abc", "4x", "hello world", "1.2.3", " ", "th"])
def test_various_non_numeric_strings(value):
    assert ordinal(value) == str(value)


def test_none_returned_as_string():
    assert ordinal(None) == str(None)


def test_list_returned_as_string():
    assert ordinal([1, 2]) == str([1, 2])


def test_numeric_strings_still_work():
    assert ordinal("1") == "1st"
    assert ordinal("2") == "2nd"
    assert ordinal("3") == "3rd"
    assert ordinal("11") == "11th"
    assert ordinal("22") == "22nd"
    assert ordinal(11) == "11th"
    assert ordinal(1) == "1st"


def test_non_finite_values_still_work():
    assert ordinal(float("nan")) == "NaN"
    assert ordinal(float("inf")) == "+Inf"
    assert ordinal(float("-inf")) == "-Inf"
