import pytest

from alvo import ordinal


def test_thirteen_takes_th_suffix():
    # Issue: ordinal(13) returned '13rd' instead of '13th'.
    assert ordinal(13) == "13th"


@pytest.mark.parametrize(
    "value, expected",
    [
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (1013, "1013th"),
    ],
)
def test_eleven_twelve_thirteen_always_take_th(value, expected):
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
        (102, "102nd"),
        (103, "103rd"),
    ],
)
def test_other_suffixes_unchanged(value, expected):
    assert ordinal(value) == expected
