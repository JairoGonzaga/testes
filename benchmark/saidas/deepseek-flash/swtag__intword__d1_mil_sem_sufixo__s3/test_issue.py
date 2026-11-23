import pytest

from alvo import intword


def test_exactly_one_thousand_is_humanized():
    """intword(1000) should be written with a word suffix (issue report)."""
    assert intword(1000) == "1.0 thousand"


def test_exactly_minus_one_thousand_is_humanized():
    assert intword(-1000) == "-1.0 thousand"


def test_one_thousand_as_float_is_humanized():
    assert intword(1000.0) == "1.0 thousand"


def test_smallest_humanized_value_is_the_thousand_boundary():
    # just below the boundary still stays a plain number...
    assert intword(999) == "999"
    # ...and the boundary itself must be humanized.
    assert intword(1000) == "1.0 thousand"


@pytest.mark.parametrize(
    "value, expected",
    [
        (1000, "1.0 thousand"),
        (1500, "1.5 thousand"),
        (1_000_000, "1.0 million"),
        (2_500_000_000, "2.5 billion"),
        (10**100, "1.0 googol"),
        (-1000, "-1.0 thousand"),
        (-1_500_000, "-1.5 million"),
    ],
)
def test_humanized_values(value, expected):
    assert intword(value) == expected
