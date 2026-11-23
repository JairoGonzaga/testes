import math
from decimal import Decimal

import pytest

from alvo import _format_not_finite, human_powers, intword, powers


EXPECTED_LEVELS = [
    (10**3, "thousand"),
    (10**6, "million"),
    (10**9, "billion"),
    (10**12, "trillion"),
    (10**15, "quadrillion"),
    (10**18, "quintillion"),
    (10**21, "sextillion"),
    (10**24, "septillion"),
    (10**27, "octillion"),
    (10**30, "nonillion"),
    (10**33, "decillion"),
    (10**100, "googol"),
]
LEVEL_IDS = [name for _, name in EXPECTED_LEVELS]


# ---------------------------------------------------------------- lookup tables

def test_powers_table_matches_specification():
    assert powers == [power for power, _ in EXPECTED_LEVELS]


def test_human_powers_table_matches_specification():
    assert tuple(human_powers) == tuple(name for _, name in EXPECTED_LEVELS)


def test_tables_are_aligned_and_strictly_increasing():
    assert len(powers) == len(human_powers) == len(EXPECTED_LEVELS)
    assert all(smaller < larger for smaller, larger in zip(powers, powers[1:]))


# ------------------------------------------------------------ _format_not_finite

def test_format_not_finite_nan():
    assert _format_not_finite(math.nan) == "NaN"


def test_format_not_finite_positive_infinity():
    assert _format_not_finite(math.inf) == "+Inf"


def test_format_not_finite_negative_infinity():
    assert _format_not_finite(-math.inf) == "-Inf"


@pytest.mark.parametrize("value", [0.0, -0.0, 1.0, -1e308, 1e308])
def test_format_not_finite_returns_empty_string_for_finite(value):
    assert _format_not_finite(value) == ""


# ------------------------------------------------------------------ non-finite

@pytest.mark.parametrize("value", [math.nan, float("nan"), "nan", "NaN"])
def test_nan_is_labelled(value):
    assert intword(value) == "NaN"


@pytest.mark.parametrize("value", [math.inf, "inf", "Infinity"])
def test_positive_infinity_is_labelled(value):
    assert intword(value) == "+Inf"


@pytest.mark.parametrize("value", [-math.inf, "-inf"])
def test_negative_infinity_is_labelled(value):
    assert intword(value) == "-Inf"


def test_non_finite_ignores_format_argument():
    assert intword(math.nan, format="%.3f") == "NaN"
    assert intword(-math.inf, format="%.3f") == "-Inf"


# ------------------------------------------------------- small values (< 1000)

@pytest.mark.parametrize("value, expected", [
    (0, "0"),
    (1, "1"),
    (-1, "-1"),
    (999, "999"),
    (-999, "-999"),
])
def test_values_below_one_thousand_are_plain_integers(value, expected):
    assert intword(value) == expected


# ------------------------------------------------------------ general behaviour

@pytest.mark.parametrize("value, expected", [
    (1000, "1.0 thousand"),
    (-1000, "-1.0 thousand"),
    (1234, "1.2 thousand"),
    (1249, "1.2 thousand"),
    (1260, "1.3 thousand"),
    (1500, "1.5 thousand"),
    (-1234, "-1.2 thousand"),
    (1_000_000, "1.0 million"),
    (1_500_000, "1.5 million"),
    (2_345_678, "2.3 million"),
    (-1_234_567, "-1.2 million"),
    (2_000_000_000, "2.0 billion"),
])
def test_typical_values(value, expected):
    assert intword(value) == expected


@pytest.mark.parametrize("value, expected", [
    (999_940, "999.9 thousand"),
    (999_949, "999.9 thousand"),
])
def test_rounding_just_below_carry_stays_on_same_unit(value, expected):
    assert intword(value) == expected


@pytest.mark.parametrize("value, expected", [
    (999_960, "1.0 million"),
    (999_999, "1.0 million"),
    (-999_999, "-1.0 million"),
    (999_999_999, "1.0 billion"),
    (999_999_999_999, "1.0 trillion"),
])
def test_rounding_up_to_1000_carries_into_next_unit(value, expected):
    assert intword(value) == expected


@pytest.mark.parametrize("index", range(10))
def test_one_below_next_unit_rolls_over(index):
    next_power, next_name = EXPECTED_LEVELS[index + 1]
    assert intword(next_power - 1) == f"1.0 {next_name}"


@pytest.mark.parametrize("power, name", EXPECTED_LEVELS, ids=LEVEL_IDS)
def test_exact_power_is_one_unit(power, name):
    assert intword(power) == f"1.0 {name}"
    assert intword(-power) == f"-1.0 {name}"


@pytest.mark.parametrize("power, name", EXPECTED_LEVELS, ids=LEVEL_IDS)
def test_two_and_a_half_units(power, name):
    assert intword(power * 25 // 10) == f"2.5 {name}"


@pytest.mark.parametrize("power, name", EXPECTED_LEVELS, ids=LEVEL_IDS)
def test_just_below_next_unit_stays_on_level(power, name):
    value = 99_994 * power // 100  # 999.94 units
    assert intword(value) == f"999.9 {name}"


def test_googol_scale_values():
    assert intword(10**100) == "1.0 googol"
    assert intword(-10**100) == "-1.0 googol"
    assert intword(10**102) == "100.0 googol"


def test_no_rollover_beyond_largest_unit():
    # Rounds to 1000.0 at the largest unit, so there is no higher unit to carry into.
    assert intword(99_996 * 10**98) == "1000.0 googol"


def test_values_far_above_googol_use_googol_unit():
    result = intword(10**300)
    number, unit = result.split(" ")
    assert unit == "googol"
    assert float(number) == 1e200


def test_returns_str_type():
    assert isinstance(intword(1234), str)


# ---------------------------------------------------------------- format argument

def test_default_format_is_one_decimal():
    assert intword(1234) == intword(1234, "%.1f") == "1.2 thousand"


@pytest.mark.parametrize("value, fmt, expected", [
    (1234, "%.2f", "1.23 thousand"),
    (1234, "%.3f", "1.234 thousand"),
    (1234, "%.0f", "1 thousand"),
    (1_234_567, "%.2f", "1.23 million"),
    (1_600_000, "%.0f", "2 million"),
    (999_600, "%.0f", "1 million"),
    (999_999, "%.2f", "1.00 million"),
])
def test_custom_format_is_applied_and_carry_respects_it(value, fmt, expected):
    assert intword(value, format=fmt) == expected


# ------------------------------------------------------ numeric coercion inputs

@pytest.mark.parametrize("value, expected", [
    (1500.7, "1.5 thousand"),
    (-1500.7, "-1.5 thousand"),
    (999.9, "999"),
    (-0.5, "0"),
    (999_999.9, "1.0 million"),
    (1e6, "1.0 million"),
    (2.5e9, "2.5 billion"),
    (Decimal("1234.5"), "1.2 thousand"),
    ("1000", "1.0 thousand"),
    (" 2500 ", "2.5 thousand"),
])
def test_numeric_inputs_are_coerced_to_int(value, expected):
    assert intword(value) == expected


@pytest.mark.parametrize("value", ["1e3", "12.5"])
def test_numeric_string_that_is_not_an_integer_is_returned_unchanged(value):
    assert intword(value) == value


@pytest.mark.parametrize("value", [None, "abc", "", [1, 2], (3,), {"a": 1}])
def test_non_numeric_input_is_returned_as_str(value):
    assert intword(value) == str(value)


def test_integer_beyond_float_range_raises_overflow():
    with pytest.raises(OverflowError):
        intword(10**400)
    with pytest.raises(OverflowError):
        intword(-10**400)
