import pytest

import alvo
from alvo import (
    InvalidChecksum,
    InvalidFormat,
    InvalidLength,
    ValidationError,
    _calc_check_digits,
    clean,
    compact,
    isdigits,
    validate,
)


# --------------------------------------------------------------------------
# Exceptions / hierarchy
# --------------------------------------------------------------------------
def test_exception_hierarchy():
    assert issubclass(ValidationError, ValueError)
    assert issubclass(InvalidFormat, ValidationError)
    assert issubclass(InvalidChecksum, ValidationError)
    assert issubclass(InvalidLength, InvalidFormat)
    assert not issubclass(InvalidChecksum, InvalidFormat)
    assert not issubclass(InvalidFormat, InvalidLength)


def test_exceptions_are_value_errors():
    with pytest.raises(ValueError):
        raise InvalidFormat()
    with pytest.raises(ValueError):
        raise InvalidChecksum()
    with pytest.raises(ValueError):
        raise InvalidLength()


# --------------------------------------------------------------------------
# clean
# --------------------------------------------------------------------------
def test_clean_no_deletechars():
    assert clean("abc") == "abc"
    assert clean("") == ""
    assert clean("  abc  ") == "  abc  "


def test_clean_deletechars():
    assert clean("abc-def", "ab") == "c-def"
    assert clean("123.456.789-01", ".-") == "12345678901"
    assert clean("hello", "l") == "heo"
    assert clean("aaaa", "a") == ""
    assert clean("abc", "") == "abc"


def test_clean_accepts_lists():
    assert clean(["a", "b"], "a") == "b"
    assert clean(["1", "2", "3"]) == "123"
    assert clean([]) == ""


def test_clean_invalid_iterable():
    with pytest.raises(InvalidFormat):
        clean(123)
    with pytest.raises(InvalidFormat):
        clean(None)
    with pytest.raises(InvalidFormat):
        clean([1, 2])


def test_clean_raises_invalid_format_instance():
    with pytest.raises(InvalidFormat) as excinfo:
        clean(1.5)
    assert isinstance(excinfo.value, ValidationError)


# --------------------------------------------------------------------------
# isdigits
# --------------------------------------------------------------------------
def test_isdigits_true():
    assert isdigits("123") is True
    assert isdigits("0") is True
    assert isdigits("0000") is True


def test_isdigits_false():
    assert isdigits("") is False
    assert isdigits("12a") is False
    assert isdigits("a12") is False
    assert isdigits("1 2") is False
    assert isdigits("-12") is False
    assert isdigits("１２３") is False


def test_isdigits_trailing_newline_matches():
    # regex "$" also matches before a trailing newline
    assert isdigits("123\n") is True


# --------------------------------------------------------------------------
# compact
# --------------------------------------------------------------------------
def test_compact():
    assert compact("123.456.789-01") == "12345678901"
    assert compact("123 456 789 01") == "12345678901"
    assert compact("123-456-789-01") == "12345678901"
    assert compact("  12345678901  ") == "12345678901"
    assert compact(" \t") == ""
    assert compact("") == ""


def test_compact_keeps_other_chars():
    assert compact("123a456") == "123a456"
    assert compact("1\t2") == "1\t2"


def test_compact_accepts_list():
    assert compact(["1", "2", "3"]) == "123"


def test_compact_invalid_type():
    with pytest.raises(InvalidFormat):
        compact(12345678901)


# --------------------------------------------------------------------------
# _calc_check_digits
# --------------------------------------------------------------------------
def test_calc_check_digits_examples():
    assert _calc_check_digits("123456789") == "09"
    assert _calc_check_digits("000000000") == "00"
    assert _calc_check_digits("111111111") == "11"
    assert _calc_check_digits("100000000") == "19"
    assert _calc_check_digits("100000001") == "08"


def test_calc_check_digits_returns_two_chars():
    result = _calc_check_digits("123456789")
    assert isinstance(result, str)
    assert len(result) == 2


# --------------------------------------------------------------------------
# validate
# --------------------------------------------------------------------------
def test_validate_valid_numbers():
    assert validate("11111111111") == "11111111111"
    assert validate("111.111.111-11") == "11111111111"
    assert validate("111 111 111 11") == "11111111111"
    assert validate(" 11111111111 ") == "11111111111"
    assert validate("10000000019") == "10000000019"
    assert validate("10000000108") == "10000000108"


def test_validate_returns_compact_number():
    assert validate("100.000.000-19") == "10000000019"


def test_validate_built_numbers():
    for base in ("123456789", "987654321", "000000001"):
        full = base + _calc_check_digits(base)
        assert validate(full) == full


def test_validate_empty_is_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("")


def test_validate_non_digits_is_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("abcdefghijk")
    with pytest.raises(InvalidFormat):
        validate("1111111111a")


def test_validate_zero_is_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("00000000000")
    with pytest.raises(InvalidFormat):
        validate("000.000.000-00")


def test_validate_non_string_is_invalid_format():
    with pytest.raises(InvalidFormat):
        validate(None)
    with pytest.raises(InvalidFormat):
        validate(11111111111)


def test_validate_short_is_invalid_length():
    with pytest.raises(InvalidLength):
        validate("1234567890")
    with pytest.raises(InvalidLength):
        validate("1")


def test_validate_long_is_invalid_length():
    with pytest.raises(InvalidLength):
        validate("123456789012")


def test_validate_invalid_length_is_invalid_format_subclass():
    with pytest.raises(InvalidFormat):
        validate("1234567890")


def test_validate_bad_checksum():
    with pytest.raises(InvalidChecksum):
        validate("11111111112")
    with pytest.raises(InvalidChecksum):
        validate("12345678901")
    with pytest.raises(InvalidChecksum):
        validate("12345678900")


def test_validate_bad_checksum_with_mask():
    with pytest.raises(InvalidChecksum):
        validate("111.111.111-12")


def test_validate_check_order_format_before_length():
    # non-digit short string -> InvalidFormat, not InvalidLength
    with pytest.raises(InvalidFormat) as excinfo:
        validate("abc")
    assert not isinstance(excinfo.value, InvalidLength)


def test_validate_all_digits_around():
    # digits-only strings of wrong checksum never raise InvalidFormat/Length
    with pytest.raises(InvalidChecksum):
        validate("00000000001")
