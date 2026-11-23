import pytest

from alvo import ordinal


@pytest.mark.parametrize("value", [11, 12, 13, 111, 112, 113, 211, 212, 213, 1011, 1012, 1013])
def test_eleventh_twelfth_thirteenth_family(value):
    assert ordinal(value) == f"{value}th"


@pytest.mark.parametrize(
    "value,expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (110, "110th"),
        (121, "121st"),
        (122, "122nd"),
        (123, "123rd"),
    ],
)
def test_regular_ordinals(value, expected):
    assert ordinal(value) == expected
