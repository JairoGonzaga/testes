"""Pytest suite for alvo.naturalsize and the alvo.suffixes tables."""

from decimal import Decimal

import pytest

from alvo import naturalsize, suffixes


# ---------------------------------------------------------------------------
# Constant tables
# ---------------------------------------------------------------------------


def test_suffix_tables_have_exact_contents():
    assert set(suffixes) == {"decimal", "binary", "gnu"}
    assert suffixes["decimal"] == (
        "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB", "RB", "QB",
    )
    assert suffixes["binary"] == (
        "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB", "RiB", "QiB",
    )
    assert suffixes["gnu"] == "KMGTPEZYRQ"


# ---------------------------------------------------------------------------
# Default mode: decimal units (base 1000), "%.1f", space before the unit
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value, expected",
    [
        # Byte-count branch: exact 1 gives singular "Byte", everything else "Bytes".
        (0, "0 Bytes"),
        (-0.0, "0 Bytes"),
        (False, "0 Bytes"),
        (1, "1 Byte"),
        (-1, "-1 Byte"),
        (1.0, "1 Byte"),
        (True, "1 Byte"),
        (1.0000001, "1 Bytes"),
        (1.5, "1 Bytes"),
        (2, "2 Bytes"),
        (-2, "-2 Bytes"),
        (0.9, "0 Bytes"),
        (-0.5, "0 Bytes"),
        (999, "999 Bytes"),
        (999.9, "999 Bytes"),
        (-999, "-999 Bytes"),
        (-999.9, "-999 Bytes"),
        # Boundary at the base (1000).
        (1000, "1.0 kB"),
        (-1000, "-1.0 kB"),
        (1001, "1.0 kB"),
        (1500, "1.5 kB"),
        (-1500, "-1.5 kB"),
        (2500, "2.5 kB"),
        (999_949, "999.9 kB"),  # rounds to 999.9, so no bump
        # Rounding pushes the mantissa to 1000.0, which bumps to the next unit.
        (999_999, "1.0 MB"),
        (999_999_999, "1.0 GB"),
        (1_000_000, "1.0 MB"),
        (1_234_567, "1.2 MB"),
        (1_500_000, "1.5 MB"),
        (-1_500_000, "-1.5 MB"),
        (2_000_000_000_000, "2.0 TB"),
        (1e9, "1.0 GB"),
        (1e12, "1.0 TB"),
        (1e15, "1.0 PB"),
        (1e18, "1.0 EB"),
        (1e21, "1.0 ZB"),
        (1e24, "1.0 YB"),
        (1e27, "1.0 RB"),
        (1e30, "1.0 QB"),
        (-1e30, "-1.0 QB"),
        # Exponent is capped at the largest available suffix.
        (1e33, "1000.0 QB"),
        (-1e33, "-1000.0 QB"),
    ],
)
def test_decimal_default_mode(value, expected):
    assert naturalsize(value) == expected


# ---------------------------------------------------------------------------
# Binary mode: base 1024, "KiB"-style suffixes, space before the unit
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, "1 Byte"),
        (-1, "-1 Byte"),
        (2, "2 Bytes"),
        (1000, "1000 Bytes"),  # below 1024, so still bytes (distinguishes base)
        (1023, "1023 Bytes"),
        (-1023, "-1023 Bytes"),
        (1024, "1.0 KiB"),
        (-1024, "-1.0 KiB"),
        (1500, "1.5 KiB"),
        (1536, "1.5 KiB"),
        (-1536, "-1.5 KiB"),
        (1048575, "1.0 MiB"),  # 1023.999 KiB rounds to 1024.0, so bump
        (1048576, "1.0 MiB"),
        (1024**3, "1.0 GiB"),
        (1024**4, "1.0 TiB"),
        (1024**5, "1.0 PiB"),
        (1024**6, "1.0 EiB"),
        (1024**7, "1.0 ZiB"),
        (1024**8, "1.0 YiB"),
        (1024**9, "1.0 RiB"),
        (1024**10, "1.0 QiB"),
        (-(1024**10), "-1.0 QiB"),
        (1024**11, "1024.0 QiB"),  # exponent capped
    ],
)
def test_binary_mode(value, expected):
    assert naturalsize(value, binary=True) == expected


# ---------------------------------------------------------------------------
# GNU mode: base 1024, single-letter suffixes, no space, bytes shown as "NB"
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0B"),
        (1, "1B"),  # no singular special case in gnu mode
        (-1, "-1B"),
        (1.5, "1B"),
        (500, "500B"),
        (1000, "1000B"),
        (1023, "1023B"),
        (-1023, "-1023B"),
        (1024, "1.0K"),
        (-1024, "-1.0K"),
        (1536, "1.5K"),
        (-1536, "-1.5K"),
        (1048575, "1.0M"),  # rounding bump
        (1048576, "1.0M"),
        (1572864, "1.5M"),
        (1024**3, "1.0G"),
        (1024**4, "1.0T"),
        (1024**5, "1.0P"),
        (1024**6, "1.0E"),
        (1024**7, "1.0Z"),
        (1024**8, "1.0Y"),
        (1024**9, "1.0R"),
        (1024**10, "1.0Q"),
        (1024**11, "1024.0Q"),  # exponent capped
    ],
)
def test_gnu_mode(value, expected):
    assert naturalsize(value, gnu=True) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, "1B"),
        (1536, "1.5K"),
        (1000, "1000B"),
        (1024**2, "1.0M"),
    ],
)
def test_gnu_takes_precedence_over_binary(value, expected):
    assert naturalsize(value, binary=True, gnu=True) == expected


# ---------------------------------------------------------------------------
# Argument handling
# ---------------------------------------------------------------------------


def test_default_arguments_are_decimal_with_one_decimal_place():
    assert naturalsize(1500) == "1.5 kB"


def test_explicit_false_flags_select_decimal():
    assert naturalsize(1024, binary=False, gnu=False) == "1.0 kB"


def test_positional_arguments_map_to_binary_gnu_format():
    assert naturalsize(1024, True) == "1.0 KiB"
    assert naturalsize(1024, False, True) == "1.0K"
    assert naturalsize(1024, False, False, "%.2f") == "1.02 kB"
    assert naturalsize(1024, True, False, "%.2f") == "1.00 KiB"


def test_value_can_be_passed_by_keyword():
    assert naturalsize(value=1500) == "1.5 kB"


# ---------------------------------------------------------------------------
# Custom format string
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value, kwargs, expected",
    [
        (1500, {"format": "%.2f"}, "1.50 kB"),
        (1500, {"format": "%.0f"}, "2 kB"),  # 1.5 rounds to 2
        (1234, {"format": "%.3f"}, "1.234 kB"),
        (999_940, {"format": "%.1f"}, "999.9 kB"),  # no bump
        (999_600, {"format": "%.0f"}, "1 MB"),  # 999.6 rounds to 1000, so bump
        (1500, {"format": "%d"}, "1 kB"),
        (999_999, {"format": "%d"}, "999 kB"),  # truncation, no bump
        (1, {"format": "%.2f"}, "1 Byte"),  # format not applied to byte counts
        (500, {"format": "%.2f"}, "500 Bytes"),
        (1536, {"format": "%.2f", "gnu": True}, "1.50K"),
        (1048575, {"format": "%.0f", "gnu": True}, "1M"),
        (1536, {"format": "%.3f", "binary": True}, "1.500 KiB"),
        (1024**2, {"format": "%.3f", "binary": True}, "1.000 MiB"),
    ],
)
def test_custom_format(value, kwargs, expected):
    assert naturalsize(value, **kwargs) == expected


def test_format_is_not_evaluated_for_plain_byte_counts():
    assert naturalsize(1, format="[%.1f]") == "1 Byte"
    assert naturalsize(500, format="[%.1f]") == "500 Bytes"


def test_format_is_not_evaluated_when_exponent_is_capped():
    assert naturalsize(1e33, format="[%.1f]") == "[1000.0] QB"


def test_non_numeric_format_breaks_the_bump_check():
    # The bump check calls float() on the formatted mantissa, so a format
    # that wraps the number in text raises ValueError.
    with pytest.raises(ValueError):
        naturalsize(1500, format="[%.1f]")


# ---------------------------------------------------------------------------
# Exact powers and values just below them
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("k", range(1, 11))
def test_exact_decimal_powers_select_matching_unit(k):
    assert naturalsize(1000**k) == f"1.0 {suffixes['decimal'][k - 1]}"


@pytest.mark.parametrize("k", range(1, 11))
def test_exact_binary_powers_select_matching_unit(k):
    assert naturalsize(1024**k, binary=True) == f"1.0 {suffixes['binary'][k - 1]}"


@pytest.mark.parametrize("k", range(1, 11))
def test_exact_gnu_powers_select_matching_unit(k):
    assert naturalsize(1024**k, gnu=True) == f"1.0{suffixes['gnu'][k - 1]}"


@pytest.mark.parametrize("k", range(2, 11))
def test_one_below_decimal_power_rounds_up_to_next_unit(k):
    assert naturalsize(1000**k - 1) == f"1.0 {suffixes['decimal'][k - 1]}"


@pytest.mark.parametrize("k", range(2, 11))
def test_one_below_binary_power_rounds_up_to_next_unit(k):
    assert naturalsize(1024**k - 1, binary=True) == f"1.0 {suffixes['binary'][k - 1]}"


@pytest.mark.parametrize("k", range(2, 11))
def test_one_below_gnu_power_rounds_up_to_next_unit(k):
    assert naturalsize(1024**k - 1, gnu=True) == f"1.0{suffixes['gnu'][k - 1]}"


# ---------------------------------------------------------------------------
# Input types
# ---------------------------------------------------------------------------


def test_numeric_strings_are_parsed():
    assert naturalsize("1500") == "1.5 kB"
    assert naturalsize(" 1500 ") == "1.5 kB"
    assert naturalsize("1e3") == "1.0 kB"
    assert naturalsize("-1500") == "-1.5 kB"
    assert naturalsize("1") == "1 Byte"


def test_decimal_input_is_accepted():
    assert naturalsize(Decimal("1500")) == "1.5 kB"
    assert naturalsize(Decimal("-1048576"), binary=True) == "-1.0 MiB"


def test_return_type_is_str():
    assert isinstance(naturalsize(1), str)
    assert isinstance(naturalsize(1500), str)


# ---------------------------------------------------------------------------
# Special float values
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value, kwargs, expected",
    [
        (float("inf"), {}, "inf QB"),
        (float("-inf"), {}, "-inf QB"),
        (float("inf"), {"binary": True}, "inf QiB"),
        (float("inf"), {"gnu": True}, "infQ"),
        (float("-inf"), {"gnu": True}, "-infQ"),
    ],
)
def test_infinities_saturate_at_largest_unit(value, kwargs, expected):
    assert naturalsize(value, **kwargs) == expected


@pytest.mark.parametrize("kwargs", [{}, {"binary": True}, {"gnu": True}])
def test_nan_raises_value_error(kwargs):
    # NaN fails every comparison, so the exponent computation calls int(nan).
    with pytest.raises(ValueError):
        naturalsize(float("nan"), **kwargs)


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("value", ["abc", "", "1.2.3", "12 kB", "1,5"])
def test_unparseable_strings_raise_value_error(value):
    with pytest.raises(ValueError):
        naturalsize(value)


@pytest.mark.parametrize("value", [None, [], {}, object()])
def test_unsupported_types_raise_type_error(value):
    with pytest.raises(TypeError):
        naturalsize(value)
