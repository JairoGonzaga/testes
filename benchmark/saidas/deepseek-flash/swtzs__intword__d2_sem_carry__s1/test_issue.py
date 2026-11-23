import pytest

from alvo import intword


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (999_999, "1.0 million"),
        (999_999_999, "1.0 billion"),
        (999_999_999_999, "1.0 trillion"),
        (-999_999, "-1.0 million"),
    ],
)
def test_intword_promotes_suffix_when_rounding_overflows(value, expected):
    assert intword(value) == expected
