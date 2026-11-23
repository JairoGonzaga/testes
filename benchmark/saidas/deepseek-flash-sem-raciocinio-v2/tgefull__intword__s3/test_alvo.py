import math

import pytest

from alvo import _format_not_finite, human_powers, intword, powers


def test_module_constants():
    assert powers == [
        10 ** 3, 10 ** 6, 10 ** 9, 10 ** 12, 10 ** 15, 10 ** 18,
        10 ** 21, 10 ** 24, 10 ** 27, 10 ** 30, 10 ** 33, 10 ** 100,
    ]
    assert human_powers == (
        "thousand", "million", "billion", "trillion", "quadrillion", "quintillion",
        "sextillion", "septillion", "octillion", "nonillion", "decillion", "googol",
    )
    assert len(powers) == len(human_powers) == 12


@pytest.mark.parametrize("value", [float("nan"), float("-nan")])
def test_format_not_finite_nan(value):
    assert _format_not_finite(value) == "NaN"


def test_format_not_finite_inf():
    assert _format_not_finite(float("-inf")) == "-Inf"
    assert _format_not_finite(float("inf")) == "+Inf"


def test_format_not_finite_returns_empty_for_finite():
    assert _format_not_finite(0.0) == ""
    assert _format_not_finite(-5.5) == ""


def test_intword_nan():
    assert intword(float("nan")) == "NaN"


def test_intword_positive_inf():
    assert intword(float("inf")) == "+Inf"


def test_intword_negative_inf():
    assert intword(float("-inf")) == "-Inf"


def test_intword_not_finite_ignores_format():
    assert intword(float("inf"), "%d") == "+Inf"
    assert intword(float("-inf"), "%d") == "-Inf"
    assert intword(float("nan"), "%d") == "NaN"


def test_intword_inf_string_is_not_finite():
    assert intword("inf") == "+Inf"
    assert intword("-inf") == "-Inf"
    assert intword("Infinity") == "+Inf"


def test_intword_nan_string_is_not_finite():
    assert intword("nan") == "NaN"


@pytest.mark.parametrize(
    "value,expected",
    [
        (0, "0"),
        (1, "1"),
        (2, "2"),
        (5, "5"),
        (42, "42"),
        (999, "999"),
        (500, "500"),
    ],
)
def test_intword_below_thousand(value, expected):
    assert intword(value) == expected


def test_intword_negative_below_thousand():
    assert intword(-1) == "-1"
    assert intword(-7) == "-7"
    assert intword(-999) == "-999"


def test_intword_zero_with_format():
    assert intword(0, "%.2f") == "0"


@pytest.mark.parametrize(
    "value,expected",
    [
        (1000, "1.0 thousand"),
        (1234, "1.2 thousand"),
        (1500, "1.5 thousand"),
        (1001, "1.0 thousand"),
        (1999, "2.0 thousand"),
        (999999, "1.0 million"),
    ],
)
def test_intword_thousand(value, expected):
    assert intword(value) == expected


def test_intword_rounding_up_promotes_unit():
    # 999999 chops to 999.999 thousand -> 1000.0 would overflow: ordinal bumped
    assert intword(999999) == "1.0 million"


@pytest.mark.parametrize(
    "value,expected",
    [
        (1000000, "1.0 million"),
        (1234567, "1.2 million"),
        (999999999, "1.0 billion"),
        (1000000000, "1.0 billion"),
        (1234567890, "1.2 billion"),
        (10 ** 12, "1.0 trillion"),
        (10 ** 15, "1.0 quadrillion"),
        (10 ** 18, "1.0 quintillion"),
        (10 ** 21, "1.0 sextillion"),
        (10 ** 24, "1.0 septillion"),
        (10 ** 27, "1.0 octillion"),
        (10 ** 30, "1.0 nonillion"),
        (10 ** 33, "1.0 decillion"),
        (2 * 10 ** 33, "2.0 decillion"),
    ],
)
def test_intword_units(value, expected):
    assert intword(value) == expected


def test_intword_largest_ordinal_small():
    # above the biggest power but with no next unit to promote to
    assert intword(10 ** 36) == "1000.0 decillion"


def test_intword_largest_ordinal_above_decillion_power():
    assert intword(999 * 10 ** 33) == "999.0 decillion"


def test_intword_googol_scale():
    assert intword(10 ** 100) == "1.0 googol"
    assert intword(2 * 10 ** 100) == "2.0 googol"
    assert intword(10 ** 101) == "10.0 googol"
    assert intword(10 ** 105) == "100000.0 googol"


def test_intword_largest_ordinal_uses_float_division():
    # chopped = value / 10**100 uses true division on huge ints -> float
    assert intword(10 ** 205) == (
        "999999999999999938258300825281978540327027364472124478294416212538871491"
        "824599713636820527503908255301632.0 googol"
    )


@pytest.mark.parametrize(
    "value,expected",
    [
        (-1000, "-1.0 thousand"),
        (-1234, "-1.2 thousand"),
        (-1500, "-1.5 thousand"),
        (-1000000, "-1.0 million"),
        (-1234567, "-1.2 million"),
    ],
)
def test_intword_negative(value, expected):
    assert intword(value) == expected


def test_intword_negative_round_trip():
    assert intword(-999999) == "-1.0 million"


def test_intword_custom_format_precision():
    assert intword(1234, "%.2f") == "1.23 thousand"
    assert intword(1234567, "%.3f") == "1.235 million"
    assert intword(1000, "%.3f") == "1.000 thousand"


def test_intword_custom_format_integer():
    assert intword(1234, "%d") == "1 thousand"
    assert intword(1234, "%.0f") == "1 thousand"
    assert intword(1999, "%.0f") == "2 thousand"
    assert intword(1500, "%.0f") == "2 thousand"
    assert intword(2500, "%.0f") == "2 thousand"


def test_intword_custom_format_promotion_to_next_unit():
    assert intword(999999, "%.0f") == "1 million"
    assert intword(1499999, "%.0f") == "1 million"
    assert intword(1499999, "%.1f") == "1.5 million"


def test_intword_custom_format_negative():
    assert intword(-1000, "%.0f") == "-1 thousand"
    assert intword(-1234, "%.2f") == "-1.23 thousand"
    assert intword(-999, "%.0f") == "-999"


def test_intword_googol_custom_format():
    assert intword(10 ** 100, "%.0f") == "1 googol"
    assert intword(2 * 10 ** 100, "%.0f") == "2 googol"
    assert intword(999000000000000000000000000000000000, "%.2f") == "999.00 decillion"


def test_intword_largest_ordinal_integer_format():
    assert intword(10 ** 205, "%d") == (
        "999999999999999938258300825281978540327027364472124478294416212538871491"
        "824599713636820527503908255301632 googol"
    )


def test_intword_decimal_value_truncated():
    assert intword(1234.9) == "1.2 thousand"
    assert intword(1000.9) == "1.0 thousand"
    assert intword(999.9) == "999"
    assert intword(1234.9, "%.0f") == "1 thousand"
    assert intword(-0.0) == "0"


def test_intword_float_value():
    assert intword(1e100) == "1.0 googol"
    assert intword(1.5e6) == "1.5 million"


def test_intword_bool():
    assert intword(True) == "1"
    assert intword(False) == "0"


def test_intword_numeric_string():
    assert intword("1234") == "1.2 thousand"
    assert intword("-1234") == "-1.2 thousand"
    assert intword("  12 ") == "12"


def test_intword_non_integer_string_returned():
    assert intword("1.5") == "1.5"
    assert intword("foo") == "foo"
    assert intword("") == ""


def test_intword_none_returned_as_str():
    assert intword(None) == "None"


def test_intword_list_returned_as_str():
    assert intword([1]) == "[1]"


def test_intword_object_returned_as_str():
    obj = object()
    assert intword(obj) == str(obj)


def test_intword_bad_format_raises():
    with pytest.raises(TypeError):
        intword(10 ** 100, None)


def test_intword_overflow_for_huge_int():
    with pytest.raises(OverflowError):
        intword(10 ** 500)
