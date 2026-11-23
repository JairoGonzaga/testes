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
        (1012, "1012th"),
        (1013, "1013th"),
    ],
)
def test_ordinal_teen_endings_in_larger_numbers_use_th(value, expected):
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
        (102, "102nd"),
        (103, "103rd"),
        (110, "110th"),
    ],
)
def test_ordinal_small_numbers_are_unchanged(value, expected):
    assert ordinal(value) == expected
