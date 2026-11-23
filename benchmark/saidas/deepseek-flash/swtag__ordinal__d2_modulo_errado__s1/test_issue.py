import pytest

from alvo import ordinal


def test_ordinal_11_is_th():
    assert ordinal(11) == "11th"


def test_ordinal_12_is_th():
    assert ordinal(12) == "12th"


def test_ordinal_13_is_th():
    assert ordinal(13) == "13th"


@pytest.mark.parametrize("value", [111, 112, 113, 1011, 1012, 1013])
def test_ordinal_teen_endings_are_th(value):
    assert ordinal(value) == f"{value}th"


@pytest.mark.parametrize(
    "value,expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (10, "10th"),
        (14, "14th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (24, "24th"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
        (104, "104th"),
        (1001, "1001st"),
    ],
)
def test_ordinal_non_teen_endings(value, expected):
    assert ordinal(value) == expected


def test_ordinal_teen_endings_do_not_use_st_nd_rd():
    for value in (11, 12, 13, 111, 112, 113):
        result = ordinal(value)
        assert result.endswith("th"), result
        assert not result.endswith(("st", "nd", "rd")), result
