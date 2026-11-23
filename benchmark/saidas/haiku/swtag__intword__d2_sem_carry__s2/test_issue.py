import pytest

from alvo import intword


def test_intword_999999_promotes_suffix_when_rounding_overflows():
    # 999999 -> 999.999 thousand, which rounds to 1000.0 thousand.
    # The suffix must be promoted to the next power: '1.0 million'.
    assert intword(999999) == "1.0 million"


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (999999, "1.0 million"),
        (999999999, "1.0 billion"),
        (999999999999, "1.0 trillion"),
        (-999999, "-1.0 million"),
    ],
)
def test_intword_rounding_overflow_promotes_suffix(value, expected):
    assert intword(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (1000, "1.0 thousand"),
        (999400, "999.4 thousand"),
        (1500000, "1.5 million"),
    ],
)
def test_intword_without_rounding_overflow_is_unchanged(value, expected):
    assert intword(value) == expected
