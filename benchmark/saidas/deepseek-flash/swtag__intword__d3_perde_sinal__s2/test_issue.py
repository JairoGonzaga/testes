import pytest

from alvo import intword


def test_negative_million_keeps_minus_sign():
    assert intword(-1000000) == "-1.0 million"


@pytest.mark.parametrize(
    "value, expected",
    [
        (-999, "-999"),
        (-1500, "-1.5 thousand"),
        (-1000000, "-1.0 million"),
        (-2500000000, "-2.5 billion"),
        (-1234567, "-1.2 million"),
        (-10**15, "-1.0 quadrillion"),
        (-10**100, "-1.0 googol"),
        (-2 * 10**100, "-2.0 googol"),
    ],
)
def test_negative_values_are_prefixed_with_minus(value, expected):
    assert intword(value) == expected


def test_negative_rounding_up_to_next_unit_keeps_minus_sign():
    # 999999 rounds up to 1000 thousand -> 1.0 million, sign must survive rounding
    assert intword(-999999) == "-1.0 million"


@pytest.mark.parametrize("value", [1, 999, 1234, 1500, 999999, 1000000, 123456789, 10**100])
def test_negative_output_is_exactly_positive_output_with_leading_minus(value):
    assert intword(-value) == "-" + intword(value)


@pytest.mark.parametrize(
    "value, expected",
    [
        (-1234567, "-1.23 million"),
        (-9876, "-9.88 thousand"),
    ],
)
def test_negative_values_respect_custom_format(value, expected):
    assert intword(value, format="%.2f") == expected


def test_positive_and_zero_values_unchanged():
    assert intword(1000000) == "1.0 million"
    assert intword(1500) == "1.5 thousand"
    assert intword(0) == "0"
    assert not intword(1500).startswith("-")


def test_non_finite_values():
    assert intword(float("-inf")) == "-Inf"
    assert intword(float("inf")) == "+Inf"
    assert intword(float("nan")) == "NaN"
