import math
from decimal import Decimal

import pytest

from alvo import _format_not_finite, human_powers, intword, powers


EXPECTED_POWERS = [
    10**3, 10**6, 10**9, 10**12, 10**15, 10**18,
    10**21, 10**24, 10**27, 10**30, 10**33, 10**100,
]
EXPECTED_NAMES = (
    "thousand", "million", "billion", "trillion", "quadrillion", "quintillion",
    "sextillion", "septillion", "octillion", "nonillion", "decillion", "googol",
)
UNITS = list(zip(EXPECTED_POWERS, EXPECTED_NAMES))


# ---------------------------------------------------------------------------
# Module constants
# ---------------------------------------------------------------------------

def test_powers_exact_values():
    assert powers == EXPECTED_POWERS


def test_human_powers_exact_names():
    assert human_powers == EXPECTED_NAMES


def test_powers_and_names_are_aligned():
    assert len(powers) == len(human_powers) == 12


def test_powers_strictly_ascending():
    assert all(lo < hi for lo, hi in zip(powers, powers[1:]))


def test_intword_does_not_mutate_module_constants():
    for value in (1000, 10**100, -5, 10**33 - 1, float("nan")):
        intword(value)
    assert powers == EXPECTED_POWERS
    assert human_powers == EXPECTED_NAMES


# ---------------------------------------------------------------------------
# _format_not_finite
# ---------------------------------------------------------------------------

def test_format_not_finite_nan():
    assert _format_not_finite(math.nan) == "NaN"


def test_format_not_finite_positive_infinity():
    assert _format_not_finite(math.inf) == "+Inf"


def test_format_not_finite_negative_infinity():
    assert _format_not_finite(-math.inf) == "-Inf"


@pytest.mark.parametrize("value", [0.0, -0.0, 1.0, -1.0, 1e308, -1e308])
def test_format_not_finite_returns_empty_string_for_finite_input(value):
    assert _format_not_finite(value) == ""


# ---------------------------------------------------------------------------
# Values below one thousand
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [(0, "0"), (1, "1"), (42, "42"), (999, "999"), (-1, "-1"), (-999, "-999")],
)
def test_integers_below_one_thousand_are_plain(value, expected):
    assert intword(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0.0, "0"),
        (-0.0, "0"),
        (1.9, "1"),
        (999.9, "999"),
        (999.9999, "999"),
        (-0.5, "0"),
        (-999.9, "-999"),
    ],
)
def test_floats_below_one_thousand_are_truncated_toward_zero(value, expected):
    assert intword(value) == expected


# ---------------------------------------------------------------------------
# Scaled values and unit selection
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        (1000, "1.0 thousand"),
        (1001, "1.0 thousand"),
        (1500, "1.5 thousand"),
        (1999, "2.0 thousand"),
        (12345, "12.3 thousand"),
        (999_949, "999.9 thousand"),
        (25 * 10**5, "2.5 million"),
        (1_460_000, "1.5 million"),
        (2_345_678, "2.3 million"),
        (123_456_789, "123.5 million"),
        (999_949_999, "999.9 million"),
        (15 * 10**8, "1.5 billion"),
        (7_654_321_000, "7.7 billion"),
        (37 * 10**11, "3.7 trillion"),
        (42 * 10**14, "4.2 quadrillion"),
        (51 * 10**17, "5.1 quintillion"),
        (66 * 10**20, "6.6 sextillion"),
        (77 * 10**23, "7.7 septillion"),
        (88 * 10**26, "8.8 octillion"),
        (99 * 10**29, "9.9 nonillion"),
        (45 * 10**32, "4.5 decillion"),
        (10**50, f"{10**17}.0 decillion"),
        (3 * 10**101, "30.0 googol"),
        (10**101, "10.0 googol"),
        (10**103, "1000.0 googol"),
        (999_999 * 10**100, "999999.0 googol"),
    ],
)
def test_scaled_values_render_expected_unit_and_mantissa(value, expected):
    assert intword(value) == expected


@pytest.mark.parametrize("power, name", UNITS)
def test_each_power_renders_as_one_point_zero(power, name):
    assert intword(power) == f"1.0 {name}"


@pytest.mark.parametrize("power, name", UNITS)
def test_one_above_each_power_renders_as_one_point_zero(power, name):
    assert intword(power + 1) == f"1.0 {name}"


@pytest.mark.parametrize("power, name", UNITS)
def test_double_each_power_renders_as_two_point_zero(power, name):
    assert intword(2 * power) == f"2.0 {name}"


@pytest.mark.parametrize("power, name", UNITS)
def test_999_times_each_power_renders_as_999_point_zero(power, name):
    assert intword(999 * power) == f"999.0 {name}"


@pytest.mark.parametrize("power, name", UNITS[1:-1])
def test_one_below_each_power_rolls_over_to_that_power(power, name):
    assert intword(power - 1) == f"1.0 {name}"


@pytest.mark.parametrize(
    "value, expected",
    [
        (999_960, "1.0 million"),
        (999_999, "1.0 million"),
        (999_999_999_999, "1.0 trillion"),
        (10**15 - 1, "1.0 quadrillion"),
        (10**33 - 1, "1.0 decillion"),
    ],
)
def test_rounding_up_to_1000_rolls_over_to_next_unit(value, expected):
    assert intword(value) == expected


# ---------------------------------------------------------------------------
# Custom format argument
# ---------------------------------------------------------------------------

def test_default_format_is_one_decimal_place():
    assert intword(1_500_000) == "1.5 million"
    assert intword(1_500_000) == intword(1_500_000, "%.1f")


def test_format_can_be_passed_by_keyword():
    assert intword(1_234_567, format="%.2f") == "1.23 million"


@pytest.mark.parametrize(
    "value, fmt, expected",
    [
        (1_234_567, "%.2f", "1.23 million"),
        (1_234_567, "%.3f", "1.235 million"),
        (1_500, "%.2f", "1.50 thousand"),
        (1_600, "%.0f", "2 thousand"),
        (5_000, "%.0f", "5 thousand"),
        (999_999, "%.0f", "1 million"),
        (999_999, "%.2f", "1.00 million"),
        (-2_500_000, "%.2f", "-2.50 million"),
        (999, "%.2f", "999"),
        (10**50, "%.0f", f"{10**17} decillion"),
        (10**100, "%.4f", "1.0000 googol"),
        (10**103, "%.3f", "1000.000 googol"),
    ],
)
def test_custom_format_controls_mantissa(value, fmt, expected):
    assert intword(value, fmt) == expected


def test_format_is_not_applied_below_one_thousand():
    assert intword(5, "abc") == "5"


def test_format_without_placeholder_raises_type_error_for_scaled_values():
    with pytest.raises(TypeError):
        intword(5_000, "abc")


def test_format_with_unsupported_conversion_raises_value_error():
    with pytest.raises(ValueError):
        intword(5_000, "%q")


# ---------------------------------------------------------------------------
# Negative values
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        (-1000, "-1.0 thousand"),
        (-999, "-999"),
        (-999_999, "-1.0 million"),
        (-1_500_000, "-1.5 million"),
        (-123_456_789, "-123.5 million"),
        (-2_500_000_000, "-2.5 billion"),
        (-(10**33), "-1.0 decillion"),
        (-(10**103), "-1000.0 googol"),
        (-1500.0, "-1.5 thousand"),
        (-999.9, "-999"),
    ],
)
def test_negative_values_get_single_minus_prefix(value, expected):
    assert intword(value) == expected


# ---------------------------------------------------------------------------
# Numeric types other than int
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        (1500.0, "1.5 thousand"),
        (1.5e6, "1.5 million"),
        (2.5e9, "2.5 billion"),
        (1e21, "1.0 sextillion"),
        (1234.9, "1.2 thousand"),
        (999999.9, "1.0 million"),
    ],
)
def test_float_inputs_are_truncated_before_scaling(value, expected):
    assert intword(value) == expected


def test_decimal_input_is_supported():
    assert intword(Decimal("2500000")) == "2.5 million"


# ---------------------------------------------------------------------------
# String inputs
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        ("999", "999"),
        ("1000", "1.0 thousand"),
        ("  2500000  ", "2.5 million"),
        ("+1500", "1.5 thousand"),
        ("-1000", "-1.0 thousand"),
    ],
)
def test_integer_strings_are_converted(value, expected):
    assert intword(value) == expected


@pytest.mark.parametrize("value", ["abc", "", "12 apples", "1000.5", "1e3"])
def test_unparseable_strings_are_returned_unchanged(value):
    assert intword(value) == value


# ---------------------------------------------------------------------------
# Non-numeric objects (TypeError / ValueError path)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [(None, "None"), ([1, 2], "[1, 2]"), ((3,), "(3,)"), ({"a": 1}, "{'a': 1}")],
)
def test_non_numeric_objects_return_their_str(value, expected):
    assert intword(value) == expected


# ---------------------------------------------------------------------------
# Non-finite values
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        (math.nan, "NaN"),
        (-math.nan, "NaN"),
        (float("nan"), "NaN"),
        (math.inf, "+Inf"),
        (-math.inf, "-Inf"),
        ("nan", "NaN"),
        ("inf", "+Inf"),
        ("-inf", "-Inf"),
        (Decimal("NaN"), "NaN"),
        (Decimal("Infinity"), "+Inf"),
        (Decimal("-Infinity"), "-Inf"),
    ],
)
def test_non_finite_values_are_named(value, expected):
    assert intword(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [(math.nan, "NaN"), (math.inf, "+Inf"), (-math.inf, "-Inf")],
)
def test_non_finite_values_ignore_format_argument(value, expected):
    assert intword(value, "%.4f") == expected


# ---------------------------------------------------------------------------
# Overflow and return type
# ---------------------------------------------------------------------------

def test_integer_too_large_for_float_raises_overflow_error():
    with pytest.raises(OverflowError):
        intword(10**400)


@pytest.mark.parametrize(
    "value", [5, 1000, -1000, 10**100, math.nan, "abc", None]
)
def test_result_is_always_a_string(value):
    assert isinstance(intword(value), str)
