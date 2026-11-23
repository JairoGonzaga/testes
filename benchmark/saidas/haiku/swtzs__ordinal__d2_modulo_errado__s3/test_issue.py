import pytest

from alvo import ordinal


def test_issue_ordinal_11_returns_11th():
    assert ordinal(11) == "11th"


@pytest.mark.parametrize(
    "number, expected",
    [
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (1011, "1011th"),
        (1012, "1012th"),
    ],
)
def test_teens_use_th_suffix(number, expected):
    assert ordinal(number) == expected


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
        (102, "102nd"),
        (103, "103rd"),
    ],
)
def test_non_teens_keep_regular_suffixes(number, expected):
    assert ordinal(number) == expected
