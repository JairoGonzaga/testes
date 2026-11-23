import pytest

from alvo import ordinal


def test_ordinal_11_is_th():
    assert ordinal(11) == "11th"


def test_ordinal_12_is_th():
    assert ordinal(12) == "12th"


def test_ordinal_13_is_th():
    # Reproduces the reported bug: currently returns '13rd'.
    assert ordinal(13) == "13th"


@pytest.mark.parametrize(
    "value,expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
    ],
)
def test_ordinal_basic_suffixes(value, expected):
    assert ordinal(value) == expected
