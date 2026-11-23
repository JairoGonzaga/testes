import pytest
from alvo import ordinal


@pytest.mark.parametrize("value,expected", [
    (11, "11th"),
    (12, "12th"),
    (13, "13th"),
    (111, "111th"),
    (112, "112th"),
    (113, "113th"),
])
def test_teens_get_th_suffix(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize("value,expected", [
    (1, "1st"),
    (2, "2nd"),
    (3, "3rd"),
    (4, "4th"),
    (21, "21st"),
    (22, "22nd"),
    (23, "23rd"),
    (101, "101st"),
    (102, "102nd"),
    (103, "103rd"),
])
def test_regular_suffixes(value, expected):
    assert ordinal(value) == expected
