import pytest

from alvo import intword


def test_googol_is_humanized_as_one_googol():
    # Issue: intword(10**100) returned a huge number with the 'decillion'
    # suffix instead of '1.0 googol'.
    assert intword(10**100) == "1.0 googol"


def test_negative_googol_is_humanized_as_one_googol():
    assert intword(-(10**100)) == "-1.0 googol"


def test_multiple_of_googol_uses_googol_unit():
    assert intword(2 * 10**100) == "2.0 googol"


@pytest.mark.parametrize(
    "value, expected",
    [
        (1000, "1.0 thousand"),
        (10**6, "1.0 million"),
    ],
)
def test_small_powers_are_unchanged(value, expected):
    assert intword(value) == expected
