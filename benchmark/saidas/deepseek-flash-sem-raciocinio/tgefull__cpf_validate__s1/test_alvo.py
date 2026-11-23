import pytest

from alvo import (
    ValidationError,
    InvalidFormat,
    InvalidChecksum,
    InvalidLength,
    clean,
    isdigits,
    compact,
    _calc_check_digits,
    validate,
)


# A few valid CPF-like numbers computed consistently with the algorithm.
# We compute them using the module's own _calc_check_digits to guarantee validity.
def _make_valid(base9):
    return base9 + _calc_check_digits(base9)


VALID_1 = _make_valid("123456789")
VALID_2 = _make_valid("000000001")
VALID_3 = _make_valid("111444777")
VALID_4 = _make_valid("987654321")


def test_exception_hierarchy():
    assert issubclass(ValidationError, ValueError)
    assert issubclass(InvalidFormat, ValidationError)
    assert issubclass(InvalidChecksum, ValidationError)
    assert issubclass(InvalidLength, InvalidFormat)
    assert issubclass(InvalidLength, ValidationError)


def test_clean_removes_chars():
    assert clean("123-456") == "123-456"
    assert clean("123-456", "-") == "123456"
    assert clean("a-b-c", "-") == "abc"
    assert clean("abc", "abc") == ""
    assert clean("", "") == ""


def test_clean_iterates_string():
    # clean turns input into a join of iterated characters
    assert clean(["1", "2", "3"]) == "123"
    assert clean(["1", "2", "3"], "2") == "13"


def test_clean_invalid_iterable_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        clean(12345)
    with pytest.raises(InvalidFormat):
        clean(None)


def test_clean_exception_is_invalid_format_type():
    with pytest.raises(InvalidFormat) as exc:
        clean(42)
    assert isinstance(exc.value, ValidationError)
    assert isinstance(exc.value, InvalidFormat)


def test_isdigits():
    assert isdigits("123") is True
    assert isdigits("0") is True
    assert isdigits("") is False
    assert isdigits("12a") is False
    assert isdigits(" 1") is False
    assert isdigits("1 ") is False
    assert isdigits("1\n") is False


def test_isdigits_returns_bool():
    result = isdigits("123")
    assert result is True
    result = isdigits("abc")
    assert result is False


def test_compact():
    assert compact("123.456.789-01") == "12345678901"
    assert compact(" 123 456 789 01 ") == "12345678901"
    assert compact("123-456.789 01") == "12345678901"
    assert compact("12345678901") == "12345678901"
    assert compact("  ") == ""


def test_compact_keeps_letters():
    assert compact("12a3") == "12a3"


def test_calc_check_digits():
    # For a known base, the computed digits should be two characters
    result = _calc_check_digits("123456789")
    assert isinstance(result, str)
    assert len(result) == 2
    assert isdigits(result)


def test_calc_check_digits_all_zeros():
    assert _calc_check_digits("000000000") == "00"


def test_calc_check_digits_known_value():
    # 111444777 -> 35
    assert _calc_check_digits("111444777") == "35"


def test_calc_check_digits_known_value_2():
    # 123456789 -> 09
    assert _calc_check_digits("123456789") == "09"


def test_calc_check_digits_known_value_3():
    assert _calc_check_digits("987654321") == "00"


def test_calc_check_digits_known_value_4():
    assert _calc_check_digits("000000001") == "95"


def test_validate_valid_number():
    assert validate(VALID_1) == VALID_1
    assert validate(VALID_2) == VALID_2
    assert validate(VALID_3) == VALID_3


def test_validate_returns_compacted():
    spaced = " ".join(VALID_3)
    assert validate(spaced) == VALID_3


def test_validate_with_punctuation():
    n = VALID_3
    formatted = n[:3] + "." + n[3:6] + "." + n[6:9] + "-" + n[9:]
    assert validate(formatted) == n


def test_validate_returns_string():
    result = validate(VALID_3)
    assert isinstance(result, str)
    assert len(result) == 11


def test_validate_invalid_format_with_letters():
    with pytest.raises(InvalidFormat):
        validate("123a5678901")


def test_validate_letters_raises_invalid_format_not_length():
    with pytest.raises(InvalidFormat):
        validate("abc")


def test_validate_all_zeros_is_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("00000000000")


def test_validate_zero_is_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("0")


def test_validate_empty_is_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("")


def test_validate_wrong_length_too_short():
    with pytest.raises(InvalidLength):
        validate("1234567890")


def test_validate_wrong_length_too_long():
    with pytest.raises(InvalidLength):
        validate("123456789012")


def test_validate_length_single_digit():
    with pytest.raises(InvalidLength):
        validate("1")


def test_invalid_length_is_invalid_format_too():
    with pytest.raises(InvalidFormat):
        validate("123")


def test_validate_bad_checksum():
    # take valid and mangle last digit
    bad = VALID_3[:-1] + str((int(VALID_3[-1]) + 1) % 10)
    with pytest.raises(InvalidChecksum):
        validate(bad)


def test_validate_bad_checksum_second_digit():
    bad = VALID_3[:-2] + str((int(VALID_3[-2]) + 1) % 10) + VALID_3[-1]
    with pytest.raises(InvalidChecksum):
        validate(bad)


def test_validate_bad_checksum_zero_padded():
    bad = VALID_2[:-1] + "0"
    if bad[-2:] != VALID_2[-2:]:
        with pytest.raises(InvalidChecksum):
            validate(bad)


def test_invalid_checksum_is_validation_error():
    bad = VALID_3[:-1] + str((int(VALID_3[-1]) + 1) % 10)
    with pytest.raises(ValidationError):
        validate(bad)


def test_validate_various_valid():
    for base in ["000000001", "100000000", "529982247", "111444777",
                 "390533447", "862883667", "123456789"]:
        num = _make_valid(base)
        assert validate(num) == num


def test_all_valid_numbers_are_consistent():
    for base in ["000000000", "000000001", "999999999", "123456789"]:
        num = _make_valid(base)
        if int(num) > 0:
            assert validate(num) == num


def test_validate_number_with_spaces_valid():
    spaced = "   " + VALID_1 + "   "
    assert validate(spaced) == VALID_1
