import pytest
from alvo import intword


def test_intword_negative_million():
    assert intword(-1000000) == '-1.0 million'


def test_intword_negative_thousand():
    assert intword(-2500) == '-2.5 thousand'


def test_intword_negative_small():
    assert intword(-999) == '-999'


def test_intword_positive_unchanged():
    assert intword(1000000) == '1.0 million'


@pytest.mark.parametrize(
    "value,expected",
    [
        (-1000000, '-1.0 million'),
        (-1000, '-1.0 thousand'),
        (-1500000000, '-1.5 billion'),
        (-42, '-42'),
    ],
)
def test_intword_negative_values(value, expected):
    assert intword(value) == expected
