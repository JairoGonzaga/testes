"""Pytest suite for alvo.ordinal and its private helpers."""

import inspect
import math
import sys
from decimal import Decimal

import pytest

from alvo import _SUFIXOS, _format_not_finite, ordinal


def _english_ordinal(n):
    """Reference oracle for non-negative integers using English ordinal rules."""
    if n % 100 in (11, 12, 13):
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


class _IntLike:
    """Numeric object supporting float() and int() conversion."""

    def __float__(self):
        return 3.0

    def __int__(self):
        return 3


class _RaisingFloat:
    def __float__(self):
        raise RuntimeError("boom")


class _Stringable:
    def __str__(self):
        return "custom text"


# ---------------------------------------------------------------------------
# Module constants and signature
# ---------------------------------------------------------------------------

def test_suffix_table_is_exact():
    assert _SUFIXOS == ("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th")


def test_ordinal_default_gender_is_male():
    assert inspect.signature(ordinal).parameters["gender"].default == "male"


# ---------------------------------------------------------------------------
# Private helper _format_not_finite
# ---------------------------------------------------------------------------

class TestFormatNotFinite:
    def test_nan_is_formatted_as_NaN(self):
        assert _format_not_finite(math.nan) == "NaN"

    def test_positive_infinity_is_formatted_as_plus_Inf(self):
        assert _format_not_finite(math.inf) == "+Inf"

    def test_negative_infinity_is_formatted_as_minus_Inf(self):
        assert _format_not_finite(-math.inf) == "-Inf"

    @pytest.mark.parametrize("value", [0.0, -0.0, 1.0, -1.0, 1e308, -1e308, 0, 7])
    def test_finite_values_yield_empty_string(self, value):
        assert _format_not_finite(value) == ""


# ---------------------------------------------------------------------------
# Integer suffix rules
# ---------------------------------------------------------------------------

class TestSingleDigits:
    @pytest.mark.parametrize(
        "value, expected",
        [
            (0, "0th"), (1, "1st"), (2, "2nd"), (3, "3rd"), (4, "4th"),
            (5, "5th"), (6, "6th"), (7, "7th"), (8, "8th"), (9, "9th"),
            (10, "10th"),
        ],
    )
    def test_units_digit_selects_suffix(self, value, expected):
        assert ordinal(value) == expected

    def test_returns_str_type(self):
        assert isinstance(ordinal(1), str)


class TestTeens:
    @pytest.mark.parametrize(
        "value", [11, 12, 13, 14, 15, 19, 111, 112, 113, 211, 1012, 1013, 1113]
    )
    def test_teens_always_take_th(self, value):
        assert ordinal(value) == f"{value}th"


class TestCompositeNumbers:
    @pytest.mark.parametrize(
        "value, expected",
        [
            (20, "20th"), (21, "21st"), (22, "22nd"), (23, "23rd"), (24, "24th"),
            (31, "31st"), (42, "42nd"), (73, "73rd"), (99, "99th"),
            (100, "100th"), (101, "101st"), (102, "102nd"), (103, "103rd"),
            (104, "104th"), (110, "110th"), (121, "121st"), (122, "122nd"),
            (123, "123rd"), (200, "200th"), (210, "210th"), (1000, "1000th"),
            (1001, "1001st"), (1002, "1002nd"), (1003, "1003rd"),
            (1011, "1011th"), (1111, "1111th"), (1112, "1112th"),
        ],
    )
    def test_explicit_examples(self, value, expected):
        assert ordinal(value) == expected

    def test_exhaustive_agreement_with_reference_rules(self):
        for n in range(2000):
            assert ordinal(n) == _english_ordinal(n), f"mismatch at {n}"

    def test_arbitrarily_large_int_is_exact(self):
        big = 10 ** 100 + 1
        assert ordinal(big) == f"{big}st"
        assert ordinal(10 ** 20) == f"{10 ** 20}th"
        assert ordinal(10 ** 100 + 11) == f"{10 ** 100 + 11}th"


class TestNegativeIntegers:
    # The implementation relies on Python's floored modulo, so suffixes for
    # negative inputs come from 10 - (|n| % 10). These outputs are pinned as the
    # current behaviour of this code.
    @pytest.mark.parametrize(
        "value, expected",
        [
            (-1, "-1th"), (-2, "-2th"), (-3, "-3th"), (-6, "-6th"), (-10, "-10th"),
            (-7, "-7rd"), (-8, "-8nd"), (-9, "-9st"),
            (-11, "-11th"), (-12, "-12th"), (-13, "-13th"),
            (-87, "-87th"), (-88, "-88th"), (-89, "-89th"), (-100, "-100th"),
        ],
    )
    def test_negative_values_use_floored_modulo(self, value, expected):
        assert ordinal(value) == expected


# ---------------------------------------------------------------------------
# Finite floats (truncated toward zero by int())
# ---------------------------------------------------------------------------

class TestFiniteFloats:
    @pytest.mark.parametrize(
        "value, expected",
        [
            (1.0, "1st"), (2.0, "2nd"), (3.0, "3rd"), (4.0, "4th"),
            (11.0, "11th"), (12.0, "12th"), (13.0, "13th"), (21.0, "21st"),
            (100.0, "100th"), (1e16, f"{10 ** 16}th"),
            (1.9, "1st"), (2.999, "2nd"), (11.5, "11th"), (12.99, "12th"),
            (0.0, "0th"), (-0.0, "0th"), (0.5, "0th"),
            (-7.0, "-7rd"), (-1.5, "-1th"), (-0.5, "0th"),
        ],
    )
    def test_floats_truncate_toward_zero_before_suffix(self, value, expected):
        assert ordinal(value) == expected

    def test_largest_finite_float_is_handled(self):
        big = sys.float_info.max
        assert ordinal(big) == _english_ordinal(int(big))


# ---------------------------------------------------------------------------
# Non-finite inputs
# ---------------------------------------------------------------------------

class TestNonFiniteInputs:
    @pytest.mark.parametrize("value", [float("nan"), math.nan, Decimal("NaN")])
    def test_nan_yields_NaN(self, value):
        assert ordinal(value) == "NaN"

    @pytest.mark.parametrize("value", [float("inf"), math.inf, Decimal("Infinity")])
    def test_positive_infinity_yields_plus_Inf(self, value):
        assert ordinal(value) == "+Inf"

    @pytest.mark.parametrize("value", [-math.inf, float("-inf"), Decimal("-Infinity")])
    def test_negative_infinity_yields_minus_Inf(self, value):
        assert ordinal(value) == "-Inf"

    @pytest.mark.parametrize(
        "value, expected",
        [
            ("nan", "NaN"), ("NaN", "NaN"), ("-nan", "NaN"),
            ("inf", "+Inf"), ("+inf", "+Inf"), ("Infinity", "+Inf"),
            ("1e400", "+Inf"),
            ("-inf", "-Inf"), ("-Infinity", "-Inf"), ("-1e400", "-Inf"),
        ],
    )
    def test_non_finite_strings_are_parsed_as_floats(self, value, expected):
        assert ordinal(value) == expected

    def test_gender_is_ignored_for_non_finite(self):
        assert ordinal(math.inf, gender="female") == "+Inf"


# ---------------------------------------------------------------------------
# String inputs
# ---------------------------------------------------------------------------

class TestIntegerStrings:
    @pytest.mark.parametrize(
        "value, expected",
        [
            ("0", "0th"), ("1", "1st"), ("2", "2nd"), ("3", "3rd"), ("11", "11th"),
            ("42", "42nd"), ("007", "7th"), ("  12  ", "12th"), ("+5", "5th"),
            ("-0", "0th"), ("-3", "-3th"), ("-7", "-7rd"),
        ],
    )
    def test_integer_strings_receive_suffix(self, value, expected):
        assert ordinal(value) == expected


class TestFractionalAndNonNumericStrings:
    @pytest.mark.parametrize("value", ["1.5", "2.0", "3.", ".5", "1e3", " 1.5 ", "-2.5"])
    def test_numeric_strings_with_fraction_are_echoed(self, value):
        assert ordinal(value) == value

    @pytest.mark.parametrize(
        "value", ["", " ", "abc", "one", "0x1A", "1,000", "12th", "1 2"]
    )
    def test_non_numeric_strings_are_echoed(self, value):
        assert ordinal(value) == value


# ---------------------------------------------------------------------------
# Other numeric-like types
# ---------------------------------------------------------------------------

class TestOtherNumericTypes:
    def test_bool_is_treated_as_int(self):
        assert ordinal(True) == "1st"
        assert ordinal(False) == "0th"

    @pytest.mark.parametrize(
        "value, expected",
        [(Decimal("2"), "2nd"), (Decimal("12.7"), "12th"), (Decimal("-7"), "-7rd")],
    )
    def test_decimal_values(self, value, expected):
        assert ordinal(value) == expected

    def test_object_implementing_float_and_int(self):
        assert ordinal(_IntLike()) == "3rd"


# ---------------------------------------------------------------------------
# Fallback path: TypeError / ValueError return str(value)
# ---------------------------------------------------------------------------

class TestUnconvertibleValues:
    @pytest.mark.parametrize(
        "value, expected",
        [
            (None, "None"),
            ([1, 2], "[1, 2]"),
            ((3,), "(3,)"),
            ({"a": 1}, "{'a': 1}"),
            (1 + 0j, "(1+0j)"),
        ],
    )
    def test_type_error_falls_back_to_str(self, value, expected):
        assert ordinal(value) == expected

    def test_fallback_uses_custom_str(self):
        assert ordinal(_Stringable()) == "custom text"


# ---------------------------------------------------------------------------
# Errors that are not caught must propagate
# ---------------------------------------------------------------------------

class TestErrorPropagation:
    def test_int_too_large_for_float_raises_overflow(self):
        # float(value) runs before int(value), so ints beyond float range overflow.
        with pytest.raises(OverflowError):
            ordinal(10 ** 400)

    def test_negative_int_too_large_for_float_raises_overflow(self):
        with pytest.raises(OverflowError):
            ordinal(-(10 ** 400))

    def test_unexpected_exception_from_float_is_not_swallowed(self):
        with pytest.raises(RuntimeError, match="boom"):
            ordinal(_RaisingFloat())


# ---------------------------------------------------------------------------
# gender parameter is accepted but does not alter output
# ---------------------------------------------------------------------------

class TestGenderParameter:
    @pytest.mark.parametrize("gender", ["male", "female", "neuter", "", None])
    @pytest.mark.parametrize(
        "value, expected", [(1, "1st"), (12, "12th"), (23, "23rd"), (104, "104th")]
    )
    def test_gender_does_not_change_result(self, gender, value, expected):
        assert ordinal(value, gender=gender) == expected

    def test_gender_accepted_positionally(self):
        assert ordinal(2, "female") == "2nd"

    def test_gender_does_not_change_fallback(self):
        assert ordinal("abc", gender="female") == "abc"
