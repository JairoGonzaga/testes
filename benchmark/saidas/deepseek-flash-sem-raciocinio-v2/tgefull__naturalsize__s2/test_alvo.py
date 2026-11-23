import pytest

import alvo
from alvo import naturalsize, suffixes


def test_suffixes_table():
    assert suffixes["decimal"] == (
        "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB", "RB", "QB",
    )
    assert suffixes["binary"] == (
        "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB", "RiB", "QiB",
    )
    assert suffixes["gnu"] == "KMGTPEZYRQ"
    assert alvo.suffixes is suffixes


# --- decimal (default) ------------------------------------------------------

def test_decimal_zero():
    assert naturalsize(0) == "0 Bytes"


def test_decimal_one_singular_byte():
    assert naturalsize(1) == "1 Byte"
    assert naturalsize(1.0) == "1 Byte"


def test_decimal_minus_one_singular_byte():
    assert naturalsize(-1) == "-1 Byte"
    assert naturalsize(-1.0) == "-1 Byte"


def test_decimal_two_plural():
    assert naturalsize(2) == "2 Bytes"


def test_decimal_negative_small():
    assert naturalsize(-2) == "-2 Bytes"
    assert naturalsize(-999) == "-999 Bytes"


def test_decimal_below_base():
    assert naturalsize(999) == "999 Bytes"
    assert naturalsize(12) == "12 Bytes"


def test_decimal_truncates_fraction_small():
    assert naturalsize(0.5) == "0 Bytes"
    assert naturalsize(-0.5) == "0 Bytes"
    assert naturalsize(1.5) == "1 Bytes"
    assert naturalsize(2.9) == "2 Bytes"
    assert naturalsize(999.6) == "999 Bytes"


def test_decimal_exactly_base():
    assert naturalsize(1000) == "1.0 kB"


def test_decimal_kilo():
    assert naturalsize(1500) == "1.5 kB"
    assert naturalsize(1001) == "1.0 kB"
    assert naturalsize(1023) == "1.0 kB"
    assert naturalsize(9999) == "10.0 kB"


def test_decimal_just_above_base_threshold():
    assert naturalsize(999999) == "1.0 MB"
    assert naturalsize(999499) == "999.5 kB"
    assert naturalsize(1000249) == "1.0 MB"


def test_decimal_mega():
    assert naturalsize(1000000) == "1.0 MB"


def test_decimal_giga():
    assert naturalsize(1000 ** 3) == "1.0 GB"


def test_decimal_tera():
    assert naturalsize(10 ** 12) == "1.0 TB"


def test_decimal_peta():
    assert naturalsize(10 ** 15) == "1.0 PB"


def test_decimal_yotta():
    assert naturalsize(1000 ** 8) == "1.0 YB"


def test_decimal_ronna():
    assert naturalsize(1000 ** 9) == "1.0 RB"


def test_decimal_quetta():
    assert naturalsize(1000 ** 10) == "1.0 QB"


def test_decimal_beyond_last_suffix():
    assert naturalsize(1000 ** 11) == "1000.0 QB"
    assert naturalsize(1e40) == "10000000000.0 QB"


def test_decimal_negative_kilo():
    assert naturalsize(-1000) == "-1.0 kB"


def test_decimal_negative_mega():
    assert naturalsize(-10 ** 6) == "-1.0 MB"


def test_decimal_negative_promotion():
    assert naturalsize(-999999) == "-1.0 MB"


# --- binary -----------------------------------------------------------------

def test_binary_byte_forms():
    assert naturalsize(1, binary=True) == "1 Byte"
    assert naturalsize(-1, binary=True) == "-1 Byte"
    assert naturalsize(2, binary=True) == "2 Bytes"
    assert naturalsize(0, binary=True) == "0 Bytes"


def test_binary_below_base():
    assert naturalsize(1023, binary=True) == "1023 Bytes"
    assert naturalsize(1000, binary=True) == "1000 Bytes"
    assert naturalsize(1001, binary=True) == "1001 Bytes"


def test_binary_kibi():
    assert naturalsize(1024, binary=True) == "1.0 KiB"
    assert naturalsize(1536, binary=True) == "1.5 KiB"


def test_binary_mebi():
    assert naturalsize(1024 ** 2, binary=True) == "1.0 MiB"


def test_binary_gibi():
    assert naturalsize(1024 ** 3, binary=True) == "1.0 GiB"


def test_binary_tebi():
    assert naturalsize(1024 ** 4, binary=True) == "1.0 TiB"


def test_binary_threshold_behaviour():
    # 999999 / 1024 = 976.561... KiB -> rounds to 976.6 (no promotion)
    assert naturalsize(999999, binary=True) == "976.6 KiB"
    # 1048575 / 1024 = 1023.999... -> format gives 1024.0 -> promoted to MiB
    assert naturalsize(1024 ** 2 - 1, binary=True) == "1.0 MiB"


def test_binary_beyond_last_suffix():
    assert naturalsize(1024 ** 11, binary=True) == "1024.0 QiB"
    assert naturalsize(1e40, binary=True) == "7888609052.2 QiB"


def test_binary_negative():
    assert naturalsize(-1024, binary=True) == "-1.0 KiB"
    assert naturalsize(-10 ** 6, binary=True) == "-976.6 KiB"
    assert naturalsize(-1024 ** 3, binary=True) == "-1.0 GiB"
    assert naturalsize(-1e40, binary=True) == "-7888609052.2 QiB"


def test_binary_fraction_below_base():
    assert naturalsize(1023.9, binary=True) == "1023 Bytes"


# --- gnu --------------------------------------------------------------------

def test_gnu_small():
    assert naturalsize(0, gnu=True) == "0B"
    assert naturalsize(12, gnu=True) == "12B"
    assert naturalsize(999, gnu=True) == "999B"


def test_gnu_one_has_no_singular_form():
    assert naturalsize(1, gnu=True) == "1B"
    assert naturalsize(-1, gnu=True) == "-1B"


def test_gnu_below_base_uses_base_1024():
    assert naturalsize(1000, gnu=True) == "1000B"
    assert naturalsize(1023, gnu=True) == "1023B"
    assert naturalsize(1024, gnu=True) == "1.0K"


def test_gnu_kilo():
    assert naturalsize(1536, gnu=True) == "1.5K"


def test_gnu_mega():
    assert naturalsize(1024 ** 2, gnu=True) == "1.0M"


def test_gnu_giga_and_tera():
    assert naturalsize(1024 ** 3, gnu=True) == "1.0G"
    assert naturalsize(1024 ** 4, gnu=True) == "1.0T"


def test_gnu_peta_and_exa():
    assert naturalsize(1024 ** 5, gnu=True) == "1.0P"
    assert naturalsize(1024 ** 6, gnu=True) == "1.0E"


def test_gnu_zetta():
    assert naturalsize(1024 ** 7, gnu=True) == "1.0Z"


def test_gnu_yotta():
    assert naturalsize(1024 ** 8, gnu=True) == "1.0Y"


def test_gnu_quetta():
    assert naturalsize(1024 ** 10, gnu=True) == "1.0Q"


def test_gnu_beyond_last_suffix():
    assert naturalsize(1024 ** 11, gnu=True) == "1024.0Q"
    assert naturalsize(1e40, gnu=True) == "7888609052.2Q"


def test_gnu_threshold_behaviour():
    assert naturalsize(1024 ** 2 - 1, gnu=True) == "1.0M"


def test_gnu_negative_kilo():
    assert naturalsize(-1536, gnu=True) == "-1.5K"


def test_gnu_negative_giga():
    assert naturalsize(-1024 ** 3, gnu=True) == "-1.0G"


def test_gnu_negative_beyond_last_suffix():
    assert naturalsize(-1e40, gnu=True) == "-7888609052.2Q"


# --- format parameter -------------------------------------------------------

def test_custom_format_whole():
    assert naturalsize(512, format="%.0f") == "512 Bytes"
    assert naturalsize(1000 ** 10, format="%.0f") == "1 QB"


def test_custom_format_two_decimals():
    assert naturalsize(1500, format="%.2f") == "1.50 kB"


def test_custom_format_two_decimals_binary():
    assert naturalsize(1536, binary=True, format="%.2f") == "1.50 KiB"


def test_custom_format_two_decimals_gnu():
    assert naturalsize(1500, gnu=True, format="%.2f") == "1.46K"


def test_custom_format_affects_promotion():
    # 999999 / 1000 = 999.999; %.0f -> "1000" >= base -> promote to MB
    assert naturalsize(999999, format="%.0f") == "1 MB"


def test_gnu_takes_precedence_over_binary():
    assert naturalsize(1536, gnu=True, binary=True) == "1.5K"
    assert naturalsize(1, gnu=True, binary=True) == "1B"
    assert naturalsize(1023, gnu=True, binary=True) == "1023B"


# --- input conversion / errors ---------------------------------------------

def test_string_input_is_converted():
    assert naturalsize("2048") == "2.0 kB"
    assert naturalsize("512") == "512 Bytes"
    assert naturalsize("1024", binary=True) == "1.0 KiB"


def test_bool_input():
    assert naturalsize(True) == "1 Byte"
    assert naturalsize(False) == "0 Bytes"


def test_invalid_string_raises():
    with pytest.raises(ValueError):
        naturalsize("abc")


def test_none_raises():
    with pytest.raises(TypeError):
        naturalsize(None)
