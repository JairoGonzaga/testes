import pytest

from alvo import ordinal


@pytest.mark.parametrize(
    "value, expected",
    [
        (13, "13th"),
        (113, "113th"),
        (213, "213th"),
        (1013, "1013th"),
        ("13", "13th"),
        (13.0, "13th"),
    ],
)
def test_teens_suffix_is_th(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (11, "11th"),
        (12, "12th"),
        (111, "111th"),
        (112, "112th"),
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (101, "101st"),
    ],
)
def test_other_suffixes_still_correct(value, expected):
    assert ordinal(value) == expected
