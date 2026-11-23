import re
from decimal import Decimal

import pytest

from alvo import naturalsize, suffixes

DECIMAL_UNITS = ("kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB", "RB", "QB")
BINARY_UNITS = ("KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB", "RiB", "QiB")
GNU_UNITS = "KMGTPEZYRQ"

_LEADING_NUMBER = re.compile(r"-?\d+(?:\.\d+)?")


def _leading_number(text):
    match = _LEADING_NUMBER.match(text)
    assert match is not None, f"no leading number in {text!r}"
    return float(match.group())


# ---------------------------------------------------------------------------
# Module data
# ---------------------------------------------------------------------------

def test_suffix_tables_have_exact_contents():
    assert suffixes["decimal"] == DECIMAL_UNITS
    assert suffixes["binary"] == BINARY_UNITS
    assert suffixes["gnu"] == GNU_UNITS


def test_suffix_tables_have_exactly_three_keys():
    assert set(suffixes) == {"decimal", "binary", "gnu"}


# ---------------------------------------------------------------------------
# Decimal (default) mode
# ---------------------------------------------------------------------------

DECIMAL_CASES = [
    # Byte branch: singular, plural, zero, truncation toward zero.
    (0, "0 Bytes"),
    (1, "1 Byte"),
    (2, "2 Bytes"),
    (999, "999 Bytes"),
    (999.9, "999 Bytes"),
    # Scaling and rounding.
    (1000, "1.0 kB"),
    (1260, "1.3 kB"),
    (1500, "1.5 kB"),
    (999_900, "999.9 kB"),
    (2_500_000, "2.5 MB"),
    (1_234_567_890, "1.2 GB"),
    (1_500_000_000_000, "1.5 TB"),
    # Rounding that carries into the next unit.
    (999_999, "1.0 MB"),
    (999_999_999, "1.0 GB"),
    # Exact unit boundaries for every decimal unit.
    (1_000_000, "1.0 MB"),
    (10**12, "1.0 TB"),
    (10**15, "1.0 PB"),
    (10**18, "1.0 EB"),
    (10**21, "1.0 ZB"),
    (10**24, "1.0 YB"),
    (10**27, "1.0 RB"),
    (10**30, "1.0 QB"),
    # Exponent is capped at the largest unit.
    (10**33, "1000.0 QB"),
    # Negative values: magnitude drives scaling, sign is preserved.
    (-1, "-1 Byte"),
    (-999, "-999 Bytes"),
    (-1000, "-1.0 kB"),
    (-1260, "-1.3 kB"),
    (-1500, "-1.5 kB"),
    (-999_999, "-1.0 MB"),
    (-1_000_000, "-1.0 MB"),
]


@pytest.mark.parametrize("value, expected", DECIMAL_CASES)
def test_decimal_default_output(value, expected):
    assert naturalsize(value) == expected


def test_decimal_is_the_default_mode():
    assert naturalsize(1024) == "1.0 kB"
    assert naturalsize(1024, binary=False, gnu=False) == "1.0 kB"


# ---------------------------------------------------------------------------
# Binary (IEC) mode
# ---------------------------------------------------------------------------

BINARY_CASES = [
    (0, "0 Bytes"),
    (1, "1 Byte"),
    (1000, "1000 Bytes"),
    (1023, "1023 Bytes"),
    (1024, "1.0 KiB"),
    (1536, "1.5 KiB"),
    (1_048_575, "1.0 MiB"),
    (1_048_576, "1.0 MiB"),
    (2**30, "1.0 GiB"),
    (2**40, "1.0 TiB"),
    (2**50, "1.0 PiB"),
    (2**60, "1.0 EiB"),
    (2**70, "1.0 ZiB"),
    (2**80, "1.0 YiB"),
    (2**90, "1.0 RiB"),
    (2**100, "1.0 QiB"),
    (2**110, "1024.0 QiB"),
    (-1, "-1 Byte"),
    (-1024, "-1.0 KiB"),
    (-1_048_575, "-1.0 MiB"),
]


@pytest.mark.parametrize("value, expected", BINARY_CASES)
def test_binary_output(value, expected):
    assert naturalsize(value, binary=True) == expected


# ---------------------------------------------------------------------------
# GNU mode
# ---------------------------------------------------------------------------

GNU_CASES = [
    (0, "0B"),
    (1, "1B"),
    (1.5, "1B"),
    (1000, "1000B"),
    (1023, "1023B"),
    (1024, "1.0K"),
    (1536, "1.5K"),
    (1_048_000, "1023.4K"),
    (1_048_575, "1.0M"),
    (5 * 1024**2, "5.0M"),
    (1024**3, "1.0G"),
    (1024**4, "1.0T"),
    (1024**5, "1.0P"),
    (1024**6, "1.0E"),
    (1024**7, "1.0Z"),
    (1024**8, "1.0Y"),
    (1024**9, "1.0R"),
    (1024**10, "1.0Q"),
    (1024**11, "1024.0Q"),
    (-1, "-1B"),
    (-1024, "-1.0K"),
    (-1536, "-1.5K"),
]


@pytest.mark.parametrize("value, expected", GNU_CASES)
def test_gnu_output(value, expected):
    assert naturalsize(value, gnu=True) == expected


def test_gnu_takes_precedence_over_binary():
    assert naturalsize(1024, binary=True, gnu=True) == "1.0K"
    assert naturalsize(1, binary=True, gnu=True) == "1B"
    assert naturalsize(1000, binary=True, gnu=True) == "1000B"


# ---------------------------------------------------------------------------
# Custom format string
# ---------------------------------------------------------------------------

FORMAT_CASES = [
    (1500, "%.2f", "1.50 kB"),
    (1500, "%.3f", "1.500 kB"),
    (1500, "%.2e", "1.50e+00 kB"),
    (1500, "%d", "1 kB"),
    (1600, "%.0f", "2 kB"),
    (1_000_000, "%.0f", "1 MB"),
    (999_999, "%.2f", "1.00 MB"),
    (999_999, "%.0f", "1 MB"),
    (500, "%.2f", "500 Bytes"),
    (1, "%.3f", "1 Byte"),
]


@pytest.mark.parametrize("value, fmt, expected", FORMAT_CASES)
def test_custom_format_applies_to_scaled_values_only(value, fmt, expected):
    assert naturalsize(value, format=fmt) == expected


def test_default_format_is_one_decimal_place():
    assert naturalsize(1500) == naturalsize(1500, format="%.1f") == "1.5 kB"


def test_custom_format_with_gnu_and_binary():
    assert naturalsize(1024, gnu=True, format="%.2f") == "1.00K"
    assert naturalsize(1024, binary=True, format="%.3f") == "1.000 KiB"


def test_invalid_format_spec_only_fails_when_used():
    assert naturalsize(500, format="%y") == "500 Bytes"
    with pytest.raises(ValueError):
        naturalsize(1500, format="%y")


# ---------------------------------------------------------------------------
# Positional arguments and parameter order
# ---------------------------------------------------------------------------

def test_positional_parameters_follow_declared_order():
    assert naturalsize(1024, False, False, "%.2f") == "1.02 kB"
    assert naturalsize(1024, True, False, "%.2f") == "1.00 KiB"
    assert naturalsize(1024, False, True) == "1.0K"


# ---------------------------------------------------------------------------
# Unit-boundary sweeps: scaled number must stay in [1, base)
# ---------------------------------------------------------------------------

MODES = [
    pytest.param(1000, {}, id="decimal"),
    pytest.param(1024, {"binary": True}, id="binary"),
    pytest.param(1024, {"gnu": True}, id="gnu"),
]


@pytest.mark.parametrize("base, flags", MODES)
@pytest.mark.parametrize("exponent", range(1, 11))
def test_unit_boundaries_never_show_a_number_of_base_or_more(base, flags, exponent):
    for magnitude in (base**exponent - 1, base**exponent):
        for value in (magnitude, -magnitude):
            out = naturalsize(value, **flags)
            number = abs(_leading_number(out))
            assert 1 <= number < base, f"{value!r} -> {out!r}"
            if value < 0:
                assert out.startswith("-"), out


# ---------------------------------------------------------------------------
# Input conversion and errors
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("value, expected", [
    ("1500", "1.5 kB"),
    (" 1500 ", "1.5 kB"),
    (Decimal("1500"), "1.5 kB"),
    (1500.0, "1.5 kB"),
    (True, "1 Byte"),
])
def test_numeric_like_inputs_are_converted_with_float(value, expected):
    assert naturalsize(value) == expected


@pytest.mark.parametrize("value", [None, [1000], (1000,), object()])
def test_non_convertible_types_raise_type_error(value):
    with pytest.raises(TypeError):
        naturalsize(value)


@pytest.mark.parametrize("value", ["abc", "", "1.2.3", "1,5"])
def test_unparseable_strings_raise_value_error(value):
    with pytest.raises(ValueError):
        naturalsize(value)


@pytest.mark.parametrize("flags", [{}, {"binary": True}, {"gnu": True}])
def test_nan_raises_value_error(flags):
    with pytest.raises(ValueError):
        naturalsize(float("nan"), **flags)


def test_positive_infinity_is_reported_in_largest_unit():
    assert naturalsize(float("inf")) == "inf QB"


def test_negative_infinity_is_reported_in_largest_unit():
    assert naturalsize(float("-inf")) == "-inf QB"
