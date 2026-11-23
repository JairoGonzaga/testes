import pytest

from alvo import ordinal


def test_ordinal_13():
    assert ordinal(13) == "13th"


def test_ordinal_11_and_12():
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"


def test_ordinal_111_112_113():
    assert ordinal(111) == "111th"
    assert ordinal(112) == "112th"
    assert ordinal(113) == "113th"


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
        (101, "101st"),
        (0, "0th"),
    ],
)
def test_ordinal_regular(value, expected):
    assert ordinal(value) == expected
