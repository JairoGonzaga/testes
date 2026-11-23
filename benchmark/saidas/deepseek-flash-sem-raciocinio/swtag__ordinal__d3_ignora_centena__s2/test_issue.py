import pytest

from alvo import ordinal


@pytest.mark.parametrize(
    "value, expected",
    [
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (211, "211th"),
        (1011, "1011th"),
        (1113, "1113th"),
        (10011, "10011th"),
    ],
)
def test_large_numbers_ending_in_teens(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
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
        (121, "121st"),
    ],
)
def test_regular_suffixes(value, expected):
    assert ordinal(value) == expected
