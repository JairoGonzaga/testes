import math
from decimal import Decimal
from fractions import Fraction

import pytest

from alvo import _format_not_finite, human_powers, intword, powers


# ---------------------------------------------------------------------------
# Module constants
# ---------------------------------------------------------------------------


def test_powers_exact_values():
    assert powers == [
        10**3, 10**6, 10**9, 10**12, 10**15, 10**18,
        10**21, 10**24, 10**27, 10**30, 10**33, 10**100,
    ]


def test_human_powers_exact_names():
    assert human_powers == (
        "thousand", "million", "billion", "trillion", "quadrillion",
        "quintillion", "sextillion", "septillion", "octillion",
        "nonillion", "decillion", "googol",
    )


def test_powers_and_names_are_aligned_and_increasing():
    assert len(powers) == len(human_powers) == 12
    assert all(lo < hi for lo, hi in zip(powers, powers[1:]))


# ---------------------------------------------------------------------------
# _format_not_finite
# ---------------------------------------------------------------------------


def test_format_not_finite_nan():
    assert _format_not_finite(math.nan) == "NaN"


def test_format_not_finite_positive_infinity():
    assert _format_not_finite(math.inf) == "+Inf"


def test_format_not_finite_negative_infinity():
    assert _format_not_finite(-math.inf) == "-Inf"


@pytest.mark.parametrize("value", [0.0, -0.0, 1.0, -1.0, 1e308, -1e-300])
def test_format_not_finite_empty_for_finite(value):
    assert _format_not_finite(value) == ""


# ---------------------------------------------------------------------------
# Non-finite inputs
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value", [math.nan, -math.nan, float("nan"), "nan", "NaN", Decimal("NaN")]
)
def test_nan_inputs(value):
    assert intword(value) == "NaN"


@pytest.mark.parametrize(
    "value",
    [math.inf, float("inf"), "inf", "+inf", "Infinity", Decimal("Infinity"), "1e400"],
)
def test_positive_infinity_inputs(value):
    assert intword(value) == "+Inf"


@pytest.mark.parametrize(
    "value", [-math.inf, "-inf", "-Infinity", Decimal("-Infinity"), "-1e400"]
)
def test_negative_infinity_inputs(value):
    assert intword(value) == "-Inf"


def test_non_finite_ignores_format_argument():
    assert intword(math.nan, "%.3f") == "NaN"
    assert intword(-math.inf, "%.3f") == "-Inf"


# ---------------------------------------------------------------------------
# Values below one thousand: plain integer, truncated toward zero
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0"),
        (1, "1"),
        (999, "999"),
        (-1, "-1"),
        (-999, "-999"),
        (0.0, "0"),
        (-0.0, "0"),
        (999.9, "999"),
        (-999.9, "-999"),
        (-0.5, "0"),
        (True, "1"),
        (False, "0"),
        ("42", "42"),
        (" 42 ", "42"),
        (Decimal("12.9"), "12"),
        (Fraction(7, 2), "3"),
    ],
)
def test_values_below_one_thousand_are_plain_integers(value, expected):
    assert intword(value) == expected


# ---------------------------------------------------------------------------
# Named magnitudes
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value, expected",
    [
        (1000, "1.0 thousand"),
        (1000.0, "1.0 thousand"),
        (1234, "1.2 thousand"),
        (1500, "1.5 thousand"),
        (1999, "2.0 thousand"),
        (1999.99, "2.0 thousand"),
        (999_940, "999.9 thousand"),
        (-1000, "-1.0 thousand"),
        (-1500, "-1.5 thousand"),
        (-1000.9, "-1.0 thousand"),
        (-1999.5, "-2.0 thousand"),
        (1_000_000, "1.0 million"),
        (1_240_000, "1.2 million"),
        (1_260_000, "1.3 million"),
        (1_234_567, "1.2 million"),
        (2_500_000, "2.5 million"),
        (999_940_000, "999.9 million"),
        (-2_500_000, "-2.5 million"),
        (1_000_000_000, "1.0 billion"),
        (3_200_000_000, "3.2 billion"),
        (999_940_000_000, "999.9 billion"),
        (10**12, "1.0 trillion"),
        (1_500_000_000_000, "1.5 trillion"),
        (10**40, "10000000.0 decillion"),
    ],
)
def test_named_magnitudes(value, expected):
    assert intword(value) == expected


@pytest.mark.parametrize("index", range(len(powers)))
def test_exact_power_uses_its_own_unit(index):
    assert intword(powers[index]) == f"1.0 {human_powers[index]}"


@pytest.mark.parametrize("index", range(len(powers)))
def test_negative_exact_power_uses_its_own_unit(index):
    assert intword(-powers[index]) == f"-1.0 {human_powers[index]}"


@pytest.mark.parametrize("index", range(len(powers)))
def test_two_and_a_half_units_for_every_unit(index):
    value = 25 * powers[index] // 10
    assert intword(value) == f"2.5 {human_powers[index]}"


# ---------------------------------------------------------------------------
# Rounding and unit promotion
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("index", range(1, 11))
def test_rounding_up_to_1000_promotes_to_next_unit(index):
    # Just below the next unit, the scaled value rounds to 1000.0 and is promoted.
    assert intword(powers[index] - 1) == f"1.0 {human_powers[index]}"


@pytest.mark.parametrize(
    "value, expected",
    [
        (999_960, "1.0 million"),
        (999_949, "999.9 thousand"),
        (999_940, "999.9 thousand"),
        (999_940_000, "999.9 million"),
        (999_949_999_999, "999.9 billion"),
        (999_999_999_999_999, "1.0 quadrillion"),
    ],
)
def test_rounding_boundaries(value, expected):
    assert intword(value) == expected


def test_googol_is_top_unit_without_promotion():
    assert intword(10**100) == "1.0 googol"
    assert intword(2 * 10**100) == "2.0 googol"
    assert intword(10**103) == "1000.0 googol"
    assert intword(999_960 * 10**97) == "1000.0 googol"
    assert intword(-(10**103)) == "-1000.0 googol"


def test_value_just_below_googol_stays_in_decillion():
    result = intword(10**100 - 1)
    assert result.endswith(" decillion")
    assert float(result.split()[0]) == pytest.approx(1e67)


def test_huge_int_below_float_overflow_uses_googol():
    result = intword(10**308)
    assert result.endswith(" googol")
    assert float(result.split()[0]) == pytest.approx(1e208)


def test_huge_float_uses_googol():
    result = intword(1e300)
    assert result.endswith(" googol")
    assert float(result.split()[0]) == pytest.approx(1e200)


def test_integer_too_large_for_float_propagates_overflow_error():
    with pytest.raises(OverflowError):
        intword(10**400)
    with pytest.raises(OverflowError):
        intword(-(10**400))


# ---------------------------------------------------------------------------
# Format argument
# ---------------------------------------------------------------------------


def test_default_format_is_one_decimal():
    assert intword(1_234_567) == "1.2 million"
    assert intword(1_234_567, "%.1f") == "1.2 million"


def test_format_keyword_argument():
    assert intword(1_234_567, format="%.2f") == "1.23 million"


@pytest.mark.parametrize(
    "fmt, value, expected",
    [
        ("%.2f", 1_234_567, "1.23 million"),
        ("%.3f", 1_234_567, "1.235 million"),
        ("%.0f", 1_234_567, "1 million"),
        ("%.0f", 1_600_000, "2 million"),
        ("%.3f", 1500, "1.500 thousand"),
        ("%.2f", -1_234_567, "-1.23 million"),
        ("%.2f", 999_999, "1.00 million"),
        ("%.0f", 999_999, "1 million"),
    ],
)
def test_format_is_applied_to_scaled_value(fmt, value, expected):
    assert intword(value, fmt) == expected


@pytest.mark.parametrize("value", [0, 5, -5, 999])
def test_format_not_applied_below_one_thousand(value):
    assert intword(value, "%.3f") == str(value)


def test_format_producing_non_float_raises_value_error():
    with pytest.raises(ValueError):
        intword(1500, "%.1f units")
    assert intword(5, "%.1f units") == "5"


# ---------------------------------------------------------------------------
# Non-numeric and string inputs
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value, expected",
    [
        ("1500", "1.5 thousand"),
        ("-2500000", "-2.5 million"),
        ("10000000000", "10.0 billion"),
    ],
)
def test_numeric_strings_are_scaled(value, expected):
    assert intword(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("abc", "abc"),
        ("", ""),
        ("12abc", "12abc"),
        ("1500.5", "1500.5"),
        ("1e6", "1e6"),
        (None, "None"),
        ([1, 2], "[1, 2]"),
        ((), "()"),
    ],
)
def test_non_numeric_input_returns_str(value, expected):
    assert intword(value) == expected


def test_arbitrary_object_returns_its_str():
    obj = object()
    assert intword(obj) == str(obj)


class _FloatOnly:
    def __float__(self):
        return 2500.0

    def __str__(self):
        return "float-only"


class _FloatRaises:
    def __float__(self):
        raise ValueError("no float")

    def __str__(self):
        return "float-raises"


class _IntAndFloat:
    def __float__(self):
        return 1234.0

    def __int__(self):
        return 1234


def test_object_convertible_only_to_float_falls_back_to_str():
    # float() succeeds but int() raises TypeError, so str(value) is returned.
    assert intword(_FloatOnly()) == "float-only"


def test_object_whose_float_raises_falls_back_to_str():
    assert intword(_FloatRaises()) == "float-raises"


def test_object_with_int_is_scaled():
    assert intword(_IntAndFloat()) == "1.2 thousand"


def test_return_type_is_str():
    assert isinstance(intword(1500), str)
    assert isinstance(intword("abc"), str)
    assert isinstance(intword(math.nan), str)
