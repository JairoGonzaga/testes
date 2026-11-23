import pytest

from alvo import ordinal


def test_ordinal_13_is_13th():
    # Reported bug: ordinal(13) returned '13rd' instead of '13th'.
    assert ordinal(13) == "13th"


@pytest.mark.parametrize("value", [11, 12, 13, 111, 112, 113, 1011, 1012, 1013])
def test_teens_always_take_th(value):
    # 11, 12 and 13 (and their hundreds/thousands counterparts) always take 'th'.
    assert ordinal(value) == f"{value}th"


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (14, "14th"),
        (19, "19th"),
        (20, "20th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
    ],
)
def test_regular_ordinals_unchanged(value, expected):
    assert ordinal(value) == expected
