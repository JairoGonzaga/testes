import pytest

from alvo import ordinal


@pytest.mark.parametrize(
    "number, expected",
    [
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
    ],
)
def test_teens_always_take_th(number, expected):
    assert ordinal(number) == expected


def test_ordinal_13_reported_case():
    assert ordinal(13) == "13th"


@pytest.mark.parametrize(
    "number, expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
    ],
)
def test_non_teens_keep_regular_suffixes(number, expected):
    assert ordinal(number) == expected
