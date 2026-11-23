import pytest

from alvo import naturalsize, suffixes


def test_suffixes():
    assert suffixes["gnu"] == "KMGTPEZYRQ"
    assert suffixes["decimal"] == ("kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB", "RB", "QB")
    assert suffixes["binary"] == ("KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB", "RiB", "QiB")


def test_zero():
    assert naturalsize(0) == "0 Bytes"


def test_one_byte():
    assert naturalsize(1) == "1 Byte"


def test_negative_one_byte():
    assert naturalsize(-1) == "-1 Byte"


def test_one_byte_binary():
    assert naturalsize(1, binary=True) == "1 Byte"


def test_below_base():
    assert naturalsize(999) == "999 Bytes"


def test_negative_below_base():
    assert naturalsize(-999) == "-999 Bytes"


def test_fractional_below_base():
    assert naturalsize(1.9) == "1 Bytes"


def test_float_below_base():
    assert naturalsize(1.5) == "1 Bytes"


def test_base():
    assert naturalsize(1000) == "1.0 kB"


def test_negative_base():
    assert naturalsize(-1000) == "-1.0 kB"


def test_kilobyte():
    assert naturalsize(1500) == "1.5 kB"


def test_million():
    assert naturalsize(1000000) == "1.0 MB"


def test_gigabyte():
    assert naturalsize(10**9) == "1.0 GB"


def test_trillion():
    assert naturalsize(10**12) == "1.0 TB"


def test_rounding_promotes():
    # 999999/1000 = 999.999 -> "%.1f" gives "1000.0" -> exponent bumped
    assert naturalsize(999999) == "1.0 MB"


def test_rounding_promotes_exact():
    assert naturalsize(999950) == "1.0 MB"


def test_no_promotion_needed():
    assert naturalsize(999949) == "999.9 kB"


def test_format_custom():
    assert naturalsize(1500, format="%.2f") == "1.50 kB"


def test_format_int():
    assert naturalsize(2500, format="%d") == "2 kB"


def test_string_input():
    assert naturalsize("1500") == "1.5 kB"


def test_float_input():
    assert naturalsize(1500.0) == "1.5 kB"


def test_binary_base():
    assert naturalsize(1024, binary=True) == "1.0 KiB"


def test_binary_negative():
    assert naturalsize(-1024, binary=True) == "-1.0 KiB"


def test_binary_below_base():
    assert naturalsize(1023, binary=True) == "1023 Bytes"


def test_binary_mebibyte():
    assert naturalsize(1024**2, binary=True) == "1.0 MiB"


def test_binary_promotes():
    assert naturalsize(1024 * 1024 - 1, binary=True) == "1.0 MiB"


def test_binary_no_promotion():
    assert naturalsize(1024 * 1024 - 200, binary=True) == "1023.8 KiB"


def test_gnu_zero():
    assert naturalsize(0, gnu=True) == "0B"


def test_gnu_below_base():
    assert naturalsize(999, gnu=True) == "999B"


def test_gnu_negative_below_base():
    assert naturalsize(-999, gnu=True) == "-999B"


def test_gnu_one():
    assert naturalsize(1, gnu=True) == "1B"


def test_gnu_negative_one():
    assert naturalsize(-1, gnu=True) == "-1B"


def test_gnu_base():
    assert naturalsize(1024, gnu=True) == "1.0K"


def test_gnu_mega():
    assert naturalsize(1024**2, gnu=True) == "1.0M"


def test_gnu_negative_base():
    assert naturalsize(-1024, gnu=True) == "-1.0K"


def test_gnu_ignores_binary():
    assert naturalsize(1024, binary=True, gnu=True) == "1.0K"


def test_gnu_custom_format():
    assert naturalsize(1536, gnu=True, format="%.2f") == "1.50K"


def test_huge_value_clamped():
    # exponent capped at len(suffix) = 10 -> suffix index 9 = "QB"
    assert naturalsize(1000 ** 20) == "999999999999999879147136483328.0 QB"


def test_huge_value_binary():
    assert naturalsize(1024 ** 20, binary=True) == "1267650600228229401496703205376.0 QiB"


def test_huge_negative():
    assert naturalsize(-(10 ** 40)) == "-10000000000.0 QB"


def test_last_suffix_exact():
    assert naturalsize(1000 ** 10) == "1.0 QB"


def test_last_suffix_binary():
    assert naturalsize(1024 ** 10, binary=True) == "1.0 QiB"


def test_gnu_last_suffix():
    assert naturalsize(1024 ** 10, gnu=True) == "1.0Q"
