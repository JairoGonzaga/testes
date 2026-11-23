import pytest

from alvo import ordinal


@pytest.mark.parametrize(
    "number, expected",
    [
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
    ],
)
def test_teen_numbers_use_th_suffix(number, expected):
    assert ordinal(number) == expected


def test_issue_ordinal_11_returns_11th():
    assert ordinal(11) == "11th"


@pytest.mark.parametrize(
    "number, expected",
    [
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
def test_regular_ordinals_still_work(number, expected):
    assert ordinal(number) == expected
