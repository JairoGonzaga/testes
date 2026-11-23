import pytest

from alvo import ordinal


def test_ordinal_13_is_th():
    assert ordinal(13) == "13th"


@pytest.mark.parametrize("value", [11, 12, 13, 111, 112, 113, 211, 1012, 1013])
def test_teens_always_take_th(value):
    assert ordinal(value) == f"{value}th"


@pytest.mark.parametrize(
    "value,expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (10, "10th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (100, "100th"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
        (111, "111th"),
    ],
)
def test_regular_suffixes_still_work(value, expected):
    assert ordinal(value) == expected
