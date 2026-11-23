import pytest

from alvo import ordinal


def test_non_numeric_string_is_returned_as_is():
    assert ordinal('something else') == 'something else'


@pytest.mark.parametrize("value", ["abc", "3rd", "1.5", "2 apples"])
def test_value_not_convertible_to_int_is_returned_as_str(value):
    assert ordinal(value) == str(value)


def test_none_is_returned_as_str():
    assert ordinal(None) == 'None'
