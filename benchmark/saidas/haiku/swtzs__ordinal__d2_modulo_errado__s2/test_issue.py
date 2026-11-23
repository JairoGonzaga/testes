import pytest

from alvo import ordinal


def test_ordinal_11_is_11th():
    # Issue: ordinal(11) returned '11st' instead of '11th'.
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
    ],
)
def test_ordinal_teens_use_th(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
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
def test_ordinal_regular_suffixes_unchanged(value, expected):
    assert ordinal(value) == expected
