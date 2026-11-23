"""Unit tests for alvo.ordinal and alvo._format_not_finite."""

import inspect
import math
from decimal import Decimal
from fractions import Fraction

import pytest

import alvo
from alvo import _SUFIXOS, _format_not_finite, ordinal


def _english_suffix(n):
    """Independent reference rule for non-negative integers."""
    if n % 100 in (11, 12, 13):
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


class _FloatOnly:
    """Supports float() but not int(), so ordinal must fall back to str()."""

    def __float__(self):
        return 5.0

    def __str__(self):
        return "float-only"


class _RaisesTypeInFloat:
    def __float__(self):
        raise TypeError("no float")

    def __str__(self):
        return "raises-type"


class _RaisesValueInFloat:
    def __float__(self):
        raise ValueError("bad float")

    def __str__(self):
        return "raises-value"


class _RaisesRuntimeInFloat:
    def __float__(self):
        raise RuntimeError("boom")


class _Plain:
    def __str__(self):
        return "plain-object"


# ---------------------------------------------------------------------------
# _SUFIXOS table
# ---------------------------------------------------------------------------

def test_sufixos_table_contents():
    assert _SUFIXOS == ("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th")


def test_sufixos_has_one_entry_per_decimal_digit():
    assert len(_SUFIXOS) == 10


def test_ordinal_reads_suffix_from_sufixos_table(monkeypatch):
    monkeypatch.setattr(alvo, "_SUFIXOS", tuple("abcdefghij"))
    assert ordinal(3) == "3d"
    assert ordinal(11) == "11a"
    assert ordinal(19) == "19j"


# ---------------------------------------------------------------------------
# _format_not_finite
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        (math.nan, "NaN"),
        (float("nan"), "NaN"),
        (math.inf, "+Inf"),
        (float("inf"), "+Inf"),
        (-math.inf, "-Inf"),
        (float("-inf"), "-Inf"),
    ],
)
def test_format_not_finite_special_values(value, expected):
    assert _format_not_finite(value) == expected


@pytest.mark.parametrize(
    "value",
    [0, 0.0, -0.0, 1, -1, 1.5, -2.75, 1e308, -1e308, 10 ** 20],
)
def test_format_not_finite_returns_empty_string_for_finite(value):
    assert _format_not_finite(value) == ""


def test_format_not_finite_rejects_non_numbers():
    with pytest.raises(TypeError):
        _format_not_finite("nan")


# ---------------------------------------------------------------------------
# ordinal: digit rules for non-negative integers
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0th"), (1, "1st"), (2, "2nd"), (3, "3rd"), (4, "4th"),
        (5, "5th"), (6, "6th"), (7, "7th"), (8, "8th"), (9, "9th"),
        (10, "10th"), (11, "11th"), (12, "12th"), (13, "13th"), (14, "14th"),
        (20, "20th"), (21, "21st"), (22, "22nd"), (23, "23rd"), (24, "24th"),
        (100, "100th"), (101, "101st"), (102, "102nd"), (103, "103rd"),
        (110, "110th"), (111, "111th"), (112, "112th"), (113, "113th"),
        (114, "114th"), (121, "121st"), (122, "122nd"), (123, "123rd"),
        (999, "999th"),
        (1000, "1000th"), (1001, "1001st"), (1002, "1002nd"), (1003, "1003rd"),
        (1011, "1011th"), (1012, "1012th"), (1013, "1013th"),
        (1021, "1021st"), (1022, "1022nd"), (1023, "1023rd"),
    ],
)
def test_ordinal_positive_integers(value, expected):
    assert ordinal(value) == expected


def test_ordinal_matches_english_rule_for_0_to_2999():
    for n in range(3000):
        assert ordinal(n) == f"{n}{_english_suffix(n)}", f"mismatch at {n}"


def test_ordinal_teen_exception_is_applied_modulo_100_not_modulo_10():
    # 11, 12, 13 and their hundreds/thousands variants all take "th"
    for n in (11, 12, 13, 111, 112, 113, 211, 212, 213, 1011, 1012, 1013):
        assert ordinal(n).endswith("th"), n
    # Numbers whose last two digits are not 11-13 keep the unit-digit suffix
    assert ordinal(101) == "101st"
    assert ordinal(121) == "121st"
    assert ordinal(114) == "114th"


# ---------------------------------------------------------------------------
# ordinal: negative integers (Python modulo semantics)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        (-1, "-1th"), (-2, "-2th"), (-3, "-3th"), (-4, "-4th"), (-5, "-5th"),
        (-6, "-6th"), (-7, "-7rd"), (-8, "-8nd"), (-9, "-9st"), (-10, "-10th"),
        (-11, "-11th"), (-12, "-12th"), (-13, "-13th"),
        (-87, "-87th"), (-88, "-88th"), (-89, "-89th"), (-90, "-90th"),
        (-97, "-97rd"), (-98, "-98nd"), (-99, "-99st"), (-100, "-100th"),
        (-101, "-101th"), (-111, "-111th"),
    ],
)
def test_ordinal_negative_integers_use_python_modulo(value, expected):
    assert ordinal(value) == expected


# ---------------------------------------------------------------------------
# ordinal: floats are truncated toward zero by int()
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        (0.0, "0th"), (-0.0, "0th"), (1.0, "1st"), (2.0, "2nd"), (3.0, "3rd"),
        (11.0, "11th"), (21.0, "21st"), (1.9, "1st"), (2.999, "2nd"),
        (7.9, "7th"), (-0.5, "0th"), (-2.7, "-2th"), (-7.5, "-7rd"),
        (1e20, "100000000000000000000th"),
    ],
)
def test_ordinal_float_values_are_truncated_toward_zero(value, expected):
    assert ordinal(value) == expected


def test_ordinal_booleans_behave_as_ints():
    assert ordinal(True) == "1st"
    assert ordinal(False) == "0th"


def test_ordinal_large_int_uses_exact_integer_value():
    # float(2**53 + 1) rounds, but the suffix must come from the exact int
    assert ordinal(2 ** 53 + 1) == "9007199254740993rd"


def test_ordinal_very_large_int_within_float_range():
    assert ordinal(10 ** 308) == "1" + "0" * 308 + "th"


def test_ordinal_int_beyond_float_range_raises_overflow_error():
    # float() overflows before int() is reached; OverflowError is not caught
    with pytest.raises(OverflowError):
        ordinal(10 ** 400)


# ---------------------------------------------------------------------------
# ordinal: decimal, fraction and other numeric types
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        (Decimal("7.9"), "7th"),
        (Decimal("21"), "21st"),
        (Decimal("-7.5"), "-7rd"),
        (Fraction(22, 7), "3rd"),
        (Fraction(-15, 2), "-7rd"),
    ],
)
def test_ordinal_decimal_and_fraction_values(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (Decimal("NaN"), "NaN"),
        (Decimal("Infinity"), "+Inf"),
        (Decimal("-Infinity"), "-Inf"),
    ],
)
def test_ordinal_decimal_non_finite_values(value, expected):
    assert ordinal(value) == expected


# ---------------------------------------------------------------------------
# ordinal: numeric strings
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        ("0", "0th"), ("1", "1st"), ("2", "2nd"), ("3", "3rd"), ("11", "11th"),
        ("21", "21st"), ("22", "22nd"), ("111", "111th"), ("007", "7th"),
        (" 12 ", "12th"), ("+3", "3rd"), ("-7", "-7rd"), ("-3", "-3th"),
        ("1" * 30, "1" * 30 + "th"),
    ],
)
def test_ordinal_numeric_strings_are_converted_to_int(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("1.5", "1.5"),
        ("2.0", "2.0"),
        ("1e3", "1e3"),
        (" 3.5 ", " 3.5 "),
        ("-0.0", "-0.0"),
    ],
)
def test_ordinal_float_strings_are_returned_unchanged(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize("value", ["abc", "", " ", "1st", "twelve"])
def test_ordinal_non_numeric_strings_are_returned_unchanged(value):
    assert ordinal(value) == value


# ---------------------------------------------------------------------------
# ordinal: non-finite values
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        (math.nan, "NaN"),
        (float("nan"), "NaN"),
        (math.inf, "+Inf"),
        (-math.inf, "-Inf"),
        (1e309, "+Inf"),
        (-1e309, "-Inf"),
        ("nan", "NaN"),
        ("NaN", "NaN"),
        (" nan ", "NaN"),
        ("inf", "+Inf"),
        ("+inf", "+Inf"),
        ("Infinity", "+Inf"),
        ("-inf", "-Inf"),
        ("-Infinity", "-Inf"),
        ("1e400", "+Inf"),
        ("-1e400", "-Inf"),
    ],
)
def test_ordinal_non_finite_values(value, expected):
    assert ordinal(value) == expected


# ---------------------------------------------------------------------------
# ordinal: non-numeric objects fall back to str(value)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        (None, "None"),
        ([], "[]"),
        ([1, 2], "[1, 2]"),
        ((1, 2), "(1, 2)"),
        ({"a": 1}, "{'a': 1}"),
        (1 + 2j, "(1+2j)"),
        (_Plain(), "plain-object"),
        (_RaisesTypeInFloat(), "raises-type"),
        (_RaisesValueInFloat(), "raises-value"),
        (_FloatOnly(), "float-only"),
    ],
)
def test_ordinal_non_numeric_objects_fall_back_to_str(value, expected):
    assert ordinal(value) == expected


def test_ordinal_propagates_unexpected_exception_from_float():
    with pytest.raises(RuntimeError, match="boom"):
        ordinal(_RaisesRuntimeInFloat())


# ---------------------------------------------------------------------------
# ordinal: gender argument and signature
# ---------------------------------------------------------------------------

def test_gender_default_is_male():
    default = inspect.signature(ordinal).parameters["gender"].default
    assert default == "male"
    assert ordinal(1) == ordinal(1, gender="male")


@pytest.mark.parametrize("gender", ["male", "female", "", None, "neutral", 0])
def test_gender_argument_does_not_change_result(gender):
    assert ordinal(22, gender) == "22nd"
    assert ordinal(float("nan"), gender) == "NaN"
    assert ordinal("abc", gender) == "abc"


def test_keyword_value_argument():
    assert ordinal(value=3) == "3rd"
    assert ordinal(3, gender="female") == "3rd"


@pytest.mark.parametrize(
    "value",
    [0, -7, 1.5, "1", "abc", None, math.nan, math.inf, Decimal("1")],
)
def test_ordinal_always_returns_str(value):
    assert isinstance(ordinal(value), str)
