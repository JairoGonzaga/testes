import pytest

from alvo import ordinal


def test_non_numeric_string_is_returned_unchanged():
    assert ordinal('something else') == 'something else'


@pytest.mark.parametrize('value', ['abc', 'twelfth', 'one', 'not a number'])
def test_non_numeric_strings_are_returned_as_str(value):
    result = ordinal(value)
    assert result == str(value)
    assert result != ''


def test_none_is_returned_as_str_of_none():
    assert ordinal(None) == 'None'
