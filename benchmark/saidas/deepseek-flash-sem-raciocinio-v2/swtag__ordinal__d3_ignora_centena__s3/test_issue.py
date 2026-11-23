import pytest

from alvo import ordinal


@pytest.mark.parametrize(
    "value,expected",
    [
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (211, "211th"),
        (1011, "1011th"),
        (1012, "1012th"),
        (1013, "1013th"),
        (1111, "1111th"),
    ],
)
def test_ordinal_teens_suffix(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
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
        (101, "101st"),
    ],
)
def test_ordinal_unchanged_cases(value, expected):
    assert ordinal(value) == expected
