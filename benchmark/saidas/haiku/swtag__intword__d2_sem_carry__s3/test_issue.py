import pytest

from alvo import intword


@pytest.mark.parametrize(
    "value, expected",
    [
        (999999, "1.0 million"),
        (-999999, "-1.0 million"),
        (999999999, "1.0 billion"),
        (999999999999, "1.0 trillion"),
    ],
)
def test_intword_promotes_suffix_when_rounding_reaches_next_power(value, expected):
    assert intword(value) == expected


def test_intword_promotes_suffix_with_custom_format():
    assert intword(999999, format="%.2f") == "1.00 million"
