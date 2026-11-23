import pytest

from alvo import naturalsize, suffixes


# --------------------------------------------------------------------------
# Module-level suffix tables
# --------------------------------------------------------------------------


def test_suffix_tables_have_expected_keys():
    assert set(suffixes) == {"decimal", "binary", "gnu"}


def test_decimal_suffix_table_is_exact():
    assert suffixes["decimal"] == (
        "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB", "RB", "QB",
    )


def test_binary_suffix_table_is_exact():
    assert suffixes["binary"] == (
        "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB", "RiB", "QiB",
    )


def test_gnu_suffix_table_is_exact():
    assert suffixes["gnu"] == "KMGTPEZYRQ"


# --------------------------------------------------------------------------
# Return type and defaults
# --------------------------------------------------------------------------


def test_returns_str():
    assert isinstance(naturalsize(5000), str)


def test_defaults_match_explicit_decimal_call():
    assert naturalsize(1500) == naturalsize(
        1500, binary=False, gnu=False, format="%.1f"
    )


# --------------------------------------------------------------------------
# Decimal mode: values below 1000 are plain bytes
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0 Bytes"),
        (0.0, "0 Bytes"),
        (-0.0, "0 Bytes"),
        (2, "2 Bytes"),
        (999, "999 Bytes"),
        (-2, "-2 Bytes"),
        (-999, "-999 Bytes"),
    ],
)
def test_decimal_values_below_1000_are_plain_bytes(value, expected):
    assert naturalsize(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, "1 Byte"),
        (1.0, "1 Byte"),
        ("1", "1 Byte"),
        (-1, "-1 Byte"),
        (-1.0, "-1 Byte"),
    ],
)
def test_exactly_one_byte_is_singular(value, expected):
    assert naturalsize(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0.5, "0 Bytes"),
        (-0.5, "0 Bytes"),
        (1.5, "1 Bytes"),
        (1.9, "1 Bytes"),
        (-1.5, "-1 Bytes"),
    ],
)
def test_fractional_bytes_are_truncated_toward_zero(value, expected):
    assert naturalsize(value) == expected


def test_decimal_boundary_999_is_bytes_and_1000_is_kilobytes():
    assert naturalsize(999) == "999 Bytes"
    assert naturalsize(1000) == "1.0 kB"


# --------------------------------------------------------------------------
# Decimal mode: scaled values
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value, expected",
    [
        (1000, "1.0 kB"),
        (1024, "1.0 kB"),
        (1234, "1.2 kB"),
        (1280, "1.3 kB"),
        (1500, "1.5 kB"),
        (700_000, "700.0 kB"),
        (999_000, "999.0 kB"),
        (999_949, "999.9 kB"),
        (-1000, "-1.0 kB"),
        (-1500, "-1.5 kB"),
    ],
)
def test_decimal_kilobytes(value, expected):
    assert naturalsize(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (10**6, "1.0 MB"),
        (1_048_576, "1.0 MB"),
        (2_500_000, "2.5 MB"),
        (10**9, "1.0 GB"),
        (1_500_000_000, "1.5 GB"),
        (10**12, "1.0 TB"),
        (10**15, "1.0 PB"),
        (10**18, "1.0 EB"),
        (10**21, "1.0 ZB"),
        (10**24, "1.0 YB"),
        (10**27, "1.0 RB"),
        (10**30, "1.0 QB"),
    ],
)
def test_decimal_each_unit_at_its_power(value, expected):
    assert naturalsize(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (999_999, "1.0 MB"),
        (999_960, "1.0 MB"),
        (999_999_999, "1.0 GB"),
        (999_999_999_999, "1.0 TB"),
        (-999_999, "-1.0 MB"),
    ],
)
def test_decimal_rounding_up_to_base_promotes_unit(value, expected):
    assert naturalsize(value) == expected


def test_decimal_values_beyond_last_unit_stay_in_qb():
    assert naturalsize(2 * 10**30) == "2.0 QB"
    assert naturalsize(10**33) == "1000.0 QB"


# --------------------------------------------------------------------------
# Binary mode
# --------------------------------------------------------------------------


def test_binary_threshold_1000_is_bytes_and_1024_is_kibibytes():
    assert naturalsize(1000, binary=True) == "1000 Bytes"
    assert naturalsize(1023, binary=True) == "1023 Bytes"
    assert naturalsize(1024, binary=True) == "1.0 KiB"


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, "1 Byte"),
        (-1, "-1 Byte"),
        (0, "0 Bytes"),
        (1536, "1.5 KiB"),
        (-1536, "-1.5 KiB"),
        (1024, "1.0 KiB"),
        (1023, "1023 Bytes"),
        (1_048_500, "1023.9 KiB"),
        (1024**2, "1.0 MiB"),
        (1024**2 - 1, "1.0 MiB"),
        (-(1024**2 - 1), "-1.0 MiB"),
        (2**30, "1.0 GiB"),
        (2**40, "1.0 TiB"),
        (2**50, "1.0 PiB"),
        (2**60, "1.0 EiB"),
        (2**70, "1.0 ZiB"),
        (2**80, "1.0 YiB"),
        (2**90, "1.0 RiB"),
        (2**100, "1.0 QiB"),
        (2**110, "1024.0 QiB"),
    ],
)
def test_binary_units(value, expected):
    assert naturalsize(value, binary=True) == expected


# --------------------------------------------------------------------------
# GNU mode
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0B"),
        (1, "1B"),
        (-1, "-1B"),
        (1.5, "1B"),
        (500, "500B"),
        (1000, "1000B"),
        (1023, "1023B"),
        (1024, "1.0K"),
        (1536, "1.5K"),
        (-1536, "-1.5K"),
        (1048575, "1.0M"),
        (1048576, "1.0M"),
        (2**30, "1.0G"),
        (2**40, "1.0T"),
        (2**50, "1.0P"),
        (2**60, "1.0E"),
        (2**70, "1.0Z"),
        (2**80, "1.0Y"),
        (2**90, "1.0R"),
        (2**100, "1.0Q"),
        (2**110, "1024.0Q"),
    ],
)
def test_gnu_units(value, expected):
    assert naturalsize(value, gnu=True) == expected


def test_gnu_takes_precedence_over_binary():
    assert naturalsize(1024, binary=True, gnu=True) == "1.0K"
    assert naturalsize(1, binary=True, gnu=True) == "1B"
    assert naturalsize(1000, binary=True, gnu=True) == "1000B"


def test_gnu_ignores_decimal_base():
    assert naturalsize(1500, gnu=True, binary=False) == "1.5K"


# --------------------------------------------------------------------------
# Sign symmetry
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value, kwargs",
    [
        (2, {}),
        (999, {}),
        (1000, {}),
        (1500, {}),
        (999_999, {}),
        (10**9, {}),
        (10**33, {}),
        (1023, {"binary": True}),
        (1024, {"binary": True}),
        (1536, {"binary": True}),
        (1048575, {"binary": True}),
        (2**60, {"binary": True}),
        (1023, {"gnu": True}),
        (1024, {"gnu": True}),
        (1048575, {"gnu": True}),
        (2**70, {"gnu": True}),
    ],
)
def test_negative_values_mirror_positive_values(value, kwargs):
    assert naturalsize(-value, **kwargs) == "-" + naturalsize(value, **kwargs)


# --------------------------------------------------------------------------
# Custom format string
# --------------------------------------------------------------------------


def test_custom_format_applies_to_scaled_values():
    assert naturalsize(1500, format="%.2f") == "1.50 kB"
    assert naturalsize(1000, format="%.3f") == "1.000 kB"
    assert naturalsize(1700, format="%.0f") == "2 kB"
    assert naturalsize(1536, binary=True, format="%.2f") == "1.50 KiB"
    assert naturalsize(1500, gnu=True, format="%.2f") == "1.46K"


def test_format_precision_drives_unit_promotion():
    # "%.0f" rounds 999.6 up to 1000, so the value is promoted to MB.
    assert naturalsize(999_600, format="%.0f") == "1 MB"
    # Default "%.1f" keeps 999.6 kB.
    assert naturalsize(999_600) == "999.6 kB"


def test_format_is_ignored_for_plain_byte_values():
    assert naturalsize(500, format="%.3f") == "500 Bytes"
    assert naturalsize(1, format="%.3f") == "1 Byte"
    assert naturalsize(500, gnu=True, format="%.3f") == "500B"


def test_positional_arguments_bind_in_order():
    assert naturalsize(1536, True, False, "%.2f") == "1.50 KiB"
    assert naturalsize(1536, False, True, "%.2f") == "1.50K"
    assert naturalsize(1536, False, False, "%.2f") == "1.54 kB"


# --------------------------------------------------------------------------
# Value coercion and special floats
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value, expected",
    [
        ("1500", "1.5 kB"),
        ("1500.0", "1.5 kB"),
        ("-1500", "-1.5 kB"),
        ("0", "0 Bytes"),
        (1500.0, "1.5 kB"),
        (1500, "1.5 kB"),
    ],
)
def test_value_is_coerced_with_float(value, expected):
    assert naturalsize(value) == expected


def test_positive_infinity_clamps_to_largest_unit():
    assert naturalsize(float("inf")) == "inf QB"
    assert naturalsize(float("inf"), binary=True) == "inf QiB"


def test_negative_infinity_clamps_to_largest_unit():
    assert naturalsize(float("-inf")) == "-inf QB"


# --------------------------------------------------------------------------
# Error handling
# --------------------------------------------------------------------------


@pytest.mark.parametrize("value", ["abc", "", "1,5", "1 kB", "1e"])
def test_non_numeric_strings_raise_value_error(value):
    with pytest.raises(ValueError):
        naturalsize(value)


@pytest.mark.parametrize("value", [None, [], {}, object()])
def test_non_numeric_types_raise_type_error(value):
    with pytest.raises(TypeError):
        naturalsize(value)


def test_integer_too_large_for_float_raises_overflow_error():
    with pytest.raises(OverflowError):
        naturalsize(10**400)
