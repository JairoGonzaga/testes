import math

import pytest

from alvo import _APNUMBER_WORDS, _format_not_finite, apnumber


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "zero"),
        (1, "one"),
        (2, "two"),
        (3, "three"),
        (4, "four"),
        (5, "five"),
        (6, "six"),
        (7, "seven"),
        (8, "eight"),
        (9, "nine"),
    ],
)
def test_single_digit_integers_are_spelled_out(value, expected):
    assert apnumber(value) == expected


def test_apnumber_words_constant_is_exact():
    assert _APNUMBER_WORDS == (
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    )


@pytest.mark.parametrize(
    "value, expected",
    [
        (0.0, "zero"),
        (-0.0, "zero"),
        (0.1, "zero"),
        (0.999, "zero"),
        (-0.1, "zero"),
        (-0.9, "zero"),
        (1.0, "one"),
        (1.1, "one"),
        (1.999, "one"),
        (8.999, "eight"),
        (9.0, "nine"),
        (9.999, "nine"),
        (-1.1, "-1"),
        (-1.9, "-1"),
        (-2.1, "-2"),
    ],
)
def test_finite_numbers_are_truncated_before_word_lookup(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (10, "10"),
        (11, "11"),
        (100, "100"),
        (10.0, "10"),
        (10.9, "10"),
        (99.9, "99"),
        (-1, "-1"),
        (-2, "-2"),
        (-10, "-10"),
        (-1.0, "-1"),
        (-1.9, "-1"),
        (-10.9, "-10"),
    ],
)
def test_numbers_outside_word_range_are_returned_as_strings(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (True, "one"),
        (False, "zero"),
    ],
)
def test_bool_values_use_their_integer_value(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("0", "zero"),
        ("5", "five"),
        ("09", "nine"),
        (" 5 ", "five"),
        ("+3", "three"),
        ("10", "10"),
        ("-1", "-1"),
        ("1.5", "1.5"),
        ("5.9", "5.9"),
        ("1e2", "1e2"),
    ],
)
def test_numeric_strings_follow_float_check_then_int_on_original_value(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (float("nan"), "NaN"),
        (math.nan, "NaN"),
        (float("inf"), "+Inf"),
        (math.inf, "+Inf"),
        (float("-inf"), "-Inf"),
        (-math.inf, "-Inf"),
        ("nan", "NaN"),
        ("NaN", "NaN"),
        ("inf", "+Inf"),
        ("+inf", "+Inf"),
        ("Infinity", "+Inf"),
        ("-inf", "-Inf"),
        ("-Infinity", "-Inf"),
    ],
)
def test_non_finite_values_are_formatted(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, "None"),
        ("abc", "abc"),
        ("not a number", "not a number"),
        ([1, 2], "[1, 2]"),
        ((1, 2), "(1, 2)"),
        ({"a": 1}, "{'a': 1}"),
        (1 + 2j, "(1+2j)"),
    ],
)
def test_float_conversion_errors_return_string_representation(value, expected):
    assert apnumber(value) == expected


class FloatRaisesValueError:
    def __float__(self):
        raise ValueError("bad float")

    def __str__(self):
        return "float-value-error"


class FloatRaisesTypeError:
    def __float__(self):
        raise TypeError("bad float")

    def __str__(self):
        return "float-type-error"


class IntRaisesValueError:
    def __float__(self):
        return 2.5

    def __int__(self):
        raise ValueError("bad int")

    def __str__(self):
        return "int-value-error"


class IntRaisesTypeError:
    def __float__(self):
        return 2.5

    def __int__(self):
        raise TypeError("bad int")

    def __str__(self):
        return "int-type-error"


def test_float_value_error_object_returns_string():
    assert apnumber(FloatRaisesValueError()) == "float-value-error"


def test_float_type_error_object_returns_string():
    assert apnumber(FloatRaisesTypeError()) == "float-type-error"


def test_int_value_error_after_successful_float_returns_string():
    assert apnumber(IntRaisesValueError()) == "int-value-error"


def test_int_type_error_after_successful_float_returns_string():
    assert apnumber(IntRaisesTypeError()) == "int-type-error"


class FloatAndIntReturnDifferentValues:
    def __float__(self):
        return 5.0

    def __int__(self):
        return 2

    def __str__(self):
        return "different"


def test_int_is_applied_to_original_object_not_to_float_value():
    assert apnumber(FloatAndIntReturnDifferentValues()) == "two"


class ChangingFloatValue:
    def __init__(self):
        self.calls = 0

    def __float__(self):
        self.calls += 1
        if self.calls == 1:
            return math.nan
        return math.inf

    def __str__(self):
        return "changing"


def test_non_finite_float_conversion_happens_again_for_formatting():
    value = ChangingFloatValue()
    assert apnumber(value) == "+Inf"
    assert value.calls == 2


class IntRaisesOverflowError:
    def __float__(self):
        return 1.0

    def __int__(self):
        raise OverflowError("too large")


def test_int_overflow_error_is_not_caught():
    with pytest.raises(OverflowError):
        apnumber(IntRaisesOverflowError())


def test_large_int_overflow_during_float_conversion_is_not_caught():
    with pytest.raises(OverflowError):
        apnumber(10**400)


@pytest.mark.parametrize(
    "value, expected",
    [
        (math.nan, "NaN"),
        (float("nan"), "NaN"),
        (float("inf"), "+Inf"),
        (math.inf, "+Inf"),
        (float("-inf"), "-Inf"),
        (-math.inf, "-Inf"),
        (0, ""),
        (0.0, ""),
        (1.5, ""),
        (-1.5, ""),
    ],
)
def test_format_not_finite_directly(value, expected):
    assert _format_not_finite(value) == expected
