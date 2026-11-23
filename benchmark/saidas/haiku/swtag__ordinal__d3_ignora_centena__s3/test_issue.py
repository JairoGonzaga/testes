import pytest

from alvo import ordinal


def test_issue_example_111_gets_th_suffix():
    # Reported in ISSUE.md: ordinal(111) returns '111st', expected '111th'.
    assert ordinal(111) == "111th"


@pytest.mark.parametrize(
    "value, expected",
    [
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (211, "211th"),
        (212, "212th"),
        (1011, "1011th"),
        (1012, "1012th"),
        (1113, "1113th"),
    ],
)
def test_numbers_ending_in_11_12_13_use_th_suffix(value, expected):
    assert ordinal(value) == expected


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
        (20, "20th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (100, "100th"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
        (1000, "1000th"),
    ],
)
def test_regular_ordinal_suffixes_are_unchanged(value, expected):
    assert ordinal(value) == expected
