import pytest

from alvo import ordinal


def test_issue_example_ordinal_11_is_11th():
    assert ordinal(11) == "11th"


@pytest.mark.parametrize(
    "value, expected",
    [
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (1011, "1011th"),
        (1012, "1012th"),
        (1013, "1013th"),
    ],
)
def test_teen_numbers_use_th_suffix(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (10, "10th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
    ],
)
def test_non_teen_numbers_keep_regular_suffixes(value, expected):
    assert ordinal(value) == expected
