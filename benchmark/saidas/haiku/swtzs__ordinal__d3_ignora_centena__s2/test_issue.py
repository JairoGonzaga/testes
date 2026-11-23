import pytest

from alvo import ordinal


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0th"),
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (10, "10th"),
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (14, "14th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (121, "121st"),
        (211, "211th"),
        (311, "311th"),
        (1011, "1011th"),
        (1012, "1012th"),
        (1111, "1111th"),
    ],
)
def test_ordinal_suffix(value, expected):
    assert ordinal(value) == expected


def test_issue_ordinal_111_is_111th():
    assert ordinal(111) == "111th"


@pytest.mark.parametrize(
    "value",
    [h * 100 + t for h in range(1, 10) for t in (11, 12, 13)],
)
def test_hundreds_digit_does_not_change_teen_suffix(value):
    assert ordinal(value) == f"{value}th"
