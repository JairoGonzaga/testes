import pytest

from alvo import ordinal


def test_ordinal_13_takes_th():
    assert ordinal(13) == "13th"


@pytest.mark.parametrize("n", [11, 12, 13, 111, 112, 113])
def test_teens_always_take_th(n):
    assert ordinal(n) == f"{n}th"


@pytest.mark.parametrize(
    "n, expected",
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
def test_regular_ordinals_unchanged(n, expected):
    assert ordinal(n) == expected
