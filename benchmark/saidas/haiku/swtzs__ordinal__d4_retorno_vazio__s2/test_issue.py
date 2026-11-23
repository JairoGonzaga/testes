import pytest

from alvo import ordinal


def test_non_numeric_string_is_returned_unchanged():
    assert ordinal('something else') == 'something else'


@pytest.mark.parametrize('value', ['abc', '12abc', None, [1, 2]])
def test_non_convertible_value_is_returned_as_str(value):
    assert ordinal(value) == str(value)
