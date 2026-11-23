import pytest

import alvo
from alvo import _format_not_finite, human_powers, intword, powers


def test_module_constants():
    assert powers == [10 ** x for x in (3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 100)]
    assert len(powers) == 12
    assert human_powers == (
        "thousand", "million", "billion", "trillion", "quadrillion", "quintillion",
        "sextillion", "septillion", "octillion", "nonillion", "decillion", "googol",
    )
    assert len(human_powers) == len(powers)


@pytest.mark.parametrize("value", [float("nan"), "nan", float("NaN")])
def test_format_not_finite_nan(value):
    assert _format_not_finite(float(value)) == "NaN"
    assert intword(value) == "NaN"


@pytest.mark.parametrize("value", [float("inf"), float("Infinity"), "+inf", "inf"])
def test_format_not_finite_pos_inf(value):
    assert _format_not_finite(float(value)) == "+Inf"
    assert intword(value) == "+Inf"


@pytest.mark.parametrize("value", [float("-inf"), float("-Infinity"), "-inf"])
def test_format_not_finite_neg_inf(value):
    assert _format_not_finite(float(value)) == "-Inf"
    assert intword(value) == "-Inf"


def test_format_not_finite_finite_fallback():
    # a finite number is not handled by the helper
    assert _format_not_finite(5.0) == ""
    assert _format_not_finite(0.0) == ""
    assert _format_not_finite(-3.5) == ""


def test_non_finite_detection_uses_float_hook():
    class NanLike(str):
        def __float__(self):
            return float("nan")

    class InfLike(str):
        def __float__(self):
            return float("-inf")

    assert intword(NanLike("whatever")) == "NaN"
    assert intword(InfLike("whatever")) == "-Inf"


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0"),
        (1, "1"),
        (7, "7"),
        (42, "42"),
        (999, "999"),
        (-1, "-1"),
        (-42, "-42"),
        (-999, "-999"),
    ],
)
def test_small_values(value, expected):
    assert intword(value) == expected


def test_below_powers_boundary():
    assert intword(999) == "999"
    assert intword(1000) == "1.0 thousand"


@pytest.mark.parametrize(
    "value, expected",
    [
        (1000, "1.0 thousand"),
        (1500, "1.5 thousand"),
        (1999, "2.0 thousand"),
        (2000, "2.0 thousand"),
        (1049, "1.0 thousand"),
        (1050, "1.1 thousand"),
        (9500, "9.5 thousand"),
        (999999, "1.0 million"),
        (1000000, "1.0 million"),
        (1500000, "1.5 million"),
        (999950, "1.0 million"),
        (999999999, "1.0 billion"),
        (999999999999, "1.0 trillion"),
        (10 ** 12, "1.0 trillion"),
        (10 ** 15, "1.0 quadrillion"),
        (10 ** 18, "1.0 quintillion"),
        (10 ** 21, "1.0 sextillion"),
        (10 ** 24, "1.0 septillion"),
        (10 ** 27, "1.0 octillion"),
        (10 ** 30, "1.0 nonillion"),
        (10 ** 33, "1.0 decillion"),
        (5 * 10 ** 33, "5.0 decillion"),
        (10 ** 36, "1000.0 decillion"),
    ],
)
def test_scaled_values(value, expected):
    assert intword(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (-1000, "-1.0 thousand"),
        (-1500, "-1.5 thousand"),
        (-2000000, "-2.0 million"),
        (-10 ** 12, "-1.0 trillion"),
    ],
)
def test_negative_values(value, expected):
    assert intword(value) == expected


def test_googol_values():
    assert intword(10 ** 100) == "1.0 googol"
    assert intword(2 * 10 ** 100) == "2.0 googol"
    assert intword(10 ** 100 + 1) == "1.0 googol"
    assert intword(10 ** 101) == "10.0 googol"
    assert intword(-(10 ** 100)) == "-1.0 googol"


def test_largest_ordinal_no_rollover():
    # for googol-scale values the value is the largest ordinal: no rollover unit
    assert intword(10 ** 100) == "1.0 googol"
    # the value is chopped by 10**100 and formatted; 10**39 falls back to decillion
    # and since the chopped value (1000000.0) would need the next unit, the
    # non-rollover path keeps the decillion unit
    assert intword(10 ** 39) == "1000000.0 decillion"


def test_truncation_of_floats_and_strings():
    assert intword(1.7) == "1"
    assert intword(1.2) == "1"
    assert intword(999.9) == "999"
    assert intword("1500") == "1.5 thousand"
    assert intword("999") == "999"
    assert intword("-1500") == "-1.5 thousand"


def test_bool_input():
    assert intword(True) == "1"
    assert intword(False) == "0"


@pytest.mark.parametrize("value", ["abc", None, "", "1.5x", [1, 2], {}])
def test_unconvertible_values_return_str(value):
    assert intword(value) == str(value)


def test_type_error_path():
    class Bad:
        def __float__(self):
            raise TypeError("nope")

        def __int__(self):
            raise TypeError("nope")

    b = Bad()
    assert intword(b) == str(b)


def test_value_error_path():
    class Bad:
        def __float__(self):
            raise ValueError("nope")

        def __int__(self):
            raise ValueError("nope")

    b = Bad()
    assert intword(b) == str(b)


def test_custom_format():
    assert intword(1234, format="%d") == "1 thousand"
    assert intword(1500, "%d") == "1 thousand"
    assert intword(1999, "%.0f") == "2 thousand"
    assert intword(10 ** 100, "%d") == "1 googol"
    assert intword(1234, "%.2f") == "1.23 thousand"
    assert intword(1234567, "%.3f") == "1.235 million"


def test_custom_format_keyword():
    assert intword(1500000, format="%.2f") == "1.50 million"


def test_rollover_with_custom_format():
    # a rolled-over value is rendered as 1.0 passed through the format
    assert intword(999999, "%.2f") == "1.00 million"
    assert intword(999999, "%.0f") == "1 million"
    assert intword(999950) == "1.0 million"
    # %d chops the chopped thousand value, so no rollover is detected
    assert intword(999999, "%d") == "999 thousand"


def test_no_rollover_below_threshold():
    # 949999 / 10**3 = 949.999 -> 950.0 (not 1000), so the thousand unit stays
    assert intword(949999) == "950.0 thousand"
    # 995000 -> 995.0 thousand, again no rollover
    assert intword(995000) == "995.0 thousand"
    # 900000 -> 900.0 thousand
    assert intword(900000) == "900.0 thousand"


def test_rollover_uses_floor_division_of_next_power():
    assert intword(9500) == "9.5 thousand"
    # 999999 -> 999.999 -> 1000.0 which equals 10**6 // 10**3 == 1000 -> rollover
    assert intword(999999) == "1.0 million"
    # 1999 -> 1.999 -> 2.0, not equal to 1000, so no rollover
    assert intword(1999) == "2.0 thousand"


def test_negative_rollover():
    assert intword(-999999) == "-1.0 million"
    assert intword(-999950) == "-1.0 million"


def test_default_format_argument():
    assert intword(1500) == intword(1500, "%.1f")


def test_repeated_calls_are_pure():
    assert intword(1500) == "1.5 thousand"
    assert intword(1500) == "1.5 thousand"
    assert intword(-1500) == "-1.5 thousand"
    assert intword(-1500) == "-1.5 thousand"
    assert alvo.powers[0] == 1000
    assert alvo.human_powers[0] == "thousand"
