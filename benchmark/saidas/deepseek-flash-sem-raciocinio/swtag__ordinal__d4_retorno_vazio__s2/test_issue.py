import math

import pytest

from alvo import ordinal


def test_non_numeric_string_returned_as_is():
    assert ordinal('something else') == 'something else'


def test_non_numeric_string_with_gender_returned_as_is():
    assert ordinal('abc', gender='female') == 'abc'


def test_none_returned_as_str():
    assert ordinal(None) == str(None)


@pytest.mark.parametrize('value', ['foo', 'bar baz', '', None, [1, 2], {'a': 1}])
def test_unconvertible_values_return_str(value):
    assert ordinal(value) == str(value)


def test_numeric_strings_still_work():
    assert ordinal('3') == '3rd'
    assert ordinal('11') == '11th'
    assert ordinal('22') == '22nd'


@pytest.mark.parametrize('value,expected', [
    (1, '1st'),
    (2, '2nd'),
    (3, '3rd'),
    (4, '4th'),
    (11, '11th'),
    (12, '12th'),
    (13, '13th'),
    (21, '21st'),
    (101, '101st'),
])
def test_integers_still_work(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize('value,expected', [
    (float('nan'), 'NaN'),
    (float('inf'), '+Inf'),
    (float('-inf'), '-Inf'),
])
def test_not_finite_values(value, expected):
    assert ordinal(value) == expected
