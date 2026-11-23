import math

import pytest

from alvo import naturalsize


class TestBytes:
    def test_zero_decimal(self):
        assert naturalsize(0) == "0 Bytes"

    def test_single_byte_decimal(self):
        assert naturalsize(1) == "1 Byte"

    def test_single_byte_binary(self):
        assert naturalsize(1, binary=True) == "1 Byte"

    def test_minus_one_byte(self):
        assert naturalsize(-1) == "-1 Byte"

    def test_small_bytes_decimal(self):
        assert naturalsize(500) == "500 Bytes"

    def test_small_bytes_binary(self):
        assert naturalsize(500, binary=True) == "500 Bytes"

    def test_boundary_just_below_kilo(self):
        assert naturalsize(999) == "999 Bytes"

    def test_boundary_binary_just_below_kibi(self):
        assert naturalsize(1023, binary=True) == "1023 Bytes"

    def test_negative_small(self):
        assert naturalsize(-999) == "-999 Bytes"

    def test_negative_close_to_one(self):
        assert naturalsize(-2) == "-2 Bytes"


class TestGnu:
    def test_gnu_single_byte(self):
        assert naturalsize(1, gnu=True) == "1B"

    def test_gnu_zero(self):
        assert naturalsize(0, gnu=True) == "0B"

    def test_gnu_small(self):
        assert naturalsize(512, gnu=True) == "512B"

    def test_gnu_negative_single(self):
        # gnu skips the "1 Byte" special case
        assert naturalsize(-1, gnu=True) == "-1B"

    def test_gnu_kilo(self):
        assert naturalsize(1024, gnu=True) == "1.0K"

    def test_gnu_mega(self):
        assert naturalsize(1024 * 1024, gnu=True) == "1.0M"

    def test_gnu_no_space(self):
        result = naturalsize(2048, gnu=True)
        assert result == "2.0K"

    def test_gnu_overrides_binary(self):
        assert naturalsize(1024, gnu=True, binary=True) == "1.0K"


class TestDecimal:
    def test_kilo(self):
        assert naturalsize(1000) == "1.0 kB"

    def test_negative_kilo(self):
        assert naturalsize(-1000) == "-1.0 kB"

    def test_mega(self):
        assert naturalsize(1000 ** 2) == "1.0 MB"

    def test_giga(self):
        assert naturalsize(1000 ** 3) == "1.0 GB"

    def test_terra(self):
        assert naturalsize(1000 ** 4) == "1.0 TB"

    def test_partial_kilo(self):
        assert naturalsize(1500) == "1.5 kB"

    def test_negative_partial(self):
        assert naturalsize(-1500) == "-1.5 kB"

    def test_rounding_up_at_boundary(self):
        # 999.95 kB should round to 1000.0 -> bumped to 1.0 MB
        assert naturalsize(999950) == "1.0 MB"


class TestBinary:
    def test_kibi(self):
        assert naturalsize(1024, binary=True) == "1.0 KiB"

    def test_mebi(self):
        assert naturalsize(1024 ** 2, binary=True) == "1.0 MiB"

    def test_gibi(self):
        assert naturalsize(1024 ** 3, binary=True) == "1.0 GiB"

    def test_negative_kibi(self):
        assert naturalsize(-1024, binary=True) == "-1.0 KiB"

    def test_partial_kibi(self):
        assert naturalsize(1536, binary=True) == "1.5 KiB"

    def test_binary_rounding_boundary(self):
        # 1023.95 KiB -> rounds to 1024.0 -> bumped to MiB
        val = 1023.95 * 1024
        assert naturalsize(val, binary=True) == "1.0 MiB"


class TestLargeExponents:
    def test_decimal_qb(self):
        # beyond the table; exp should clamp to len(suffix)
        val = 1000 ** 11
        result = naturalsize(val)
        assert result.endswith("QB")
        assert result == "1.0 QB"

    def test_binary_qi(self):
        val = 1024 ** 11
        result = naturalsize(val, binary=True)
        assert result.endswith("QiB")

    def test_gnu_beyond_table(self):
        val = 1024 ** 11
        result = naturalsize(val, gnu=True)
        assert result.endswith("Q")
        assert result == "1.0Q"

    def test_gnu_last_suffix(self):
        val = 1024 ** 10
        assert naturalsize(val, gnu=True) == "1.0Q"

    def test_decimal_last_suffix(self):
        val = 1000 ** 10
        assert naturalsize(val) == "1.0 QB"

    def test_binary_last_suffix(self):
        val = 1024 ** 10
        assert naturalsize(val, binary=True) == "1.0 QiB"

    def test_decimal_rb(self):
        val = 1000 ** 9
        assert naturalsize(val) == "1.0 RB"

    def test_binary_rib(self):
        val = 1024 ** 9
        assert naturalsize(val, binary=True) == "1.0 RiB"


class TestFormat:
    def test_custom_format_zero_decimals(self):
        assert naturalsize(1500, format="%.0f") == "2 kB"

    def test_custom_format_three_decimals(self):
        assert naturalsize(1500, format="%.3f") == "1.500 kB"

    def test_custom_format_gnu(self):
        assert naturalsize(1500, gnu=True, format="%.2f") == "1.46K"

    def test_format_bytes_ignored(self):
        # formatting only applies to scaled output
        assert naturalsize(100, format="%.3f") == "100 Bytes"

    def test_format_negative(self):
        assert naturalsize(-2500, format="%.2f") == "-2.50 kB"


class TestTypeConversion:
    def test_float_input(self):
        assert naturalsize(1500.7) == "1.5 kB"

    def test_string_input(self):
        assert naturalsize("2048") == "2.0 kB"

    def test_fractional_byte_floor(self):
        assert naturalsize(1.9) == "1 Byte"

    def test_fractional_negative_byte(self):
        assert naturalsize(-1.9) == "-1 Byte"
