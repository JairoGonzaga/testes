import pytest

from alvo import ordinal


@pytest.mark.parametrize(
    "number, expected",
    [
        (111, "111th"),  # example from the issue report
        (112, "112th"),
        (113, "113th"),
        (211, "211th"),
        (1011, "1011th"),
        (1012, "1012th"),
        (1013, "1013th"),
    ],
)
def test_numbers_ending_in_11_12_13_get_th_suffix(number, expected):
    assert ordinal(number) == expected


@pytest.mark.parametrize(
    "number, expected",
    [
        (0, "0th"),
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
        (100, "100th"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
    ],
)
def test_small_and_regular_numbers_keep_correct_suffix(number, expected):
    assert ordinal(number) == expected
