import pytest

from alvo import ordinal


def test_ordinal_11_is_11th():
    assert ordinal(11) == "11th"


@pytest.mark.parametrize("value,expected", [
    (1, "1st"),
    (2, "2nd"),
    (3, "3rd"),
    (4, "4th"),
    (11, "11th"),
    (12, "12th"),
    (13, "13th"),
    (21, "21st"),
    (22, "22nd"),
    (23, "23rd"),
    (111, "111th"),
    (112, "112th"),
    (113, "113th"),
])
def test_ordinal_suffixes(value, expected):
    assert ordinal(value) == expected
