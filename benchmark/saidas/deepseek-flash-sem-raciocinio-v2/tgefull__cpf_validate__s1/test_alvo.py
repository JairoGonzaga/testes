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

# 11144477735 was produced by _calc_check_digits("111444777" + "00") -> "35"
VALID = "11144477735"


# --------------------------------------------------------------------------
# Exception hierarchy
# --------------------------------------------------------------------------
def test_validation_error_is_value_error():
    assert issubclass(ValidationError, ValueError)


def test_invalid_format_hierarchy():
    assert issubclass(InvalidFormat, ValidationError)
    assert not issubclass(InvalidFormat, InvalidLength)


def test_invalid_checksum_hierarchy():
    assert issubclass(InvalidChecksum, ValidationError)
    assert not issubclass(InvalidChecksum, InvalidFormat)


def test_invalid_length_hierarchy():
    assert issubclass(InvalidLength, InvalidFormat)
    assert issubclass(InvalidLength, ValidationError)


# --------------------------------------------------------------------------
# clean()
# --------------------------------------------------------------------------
def test_clean_default_deletes_nothing():
    assert clean("abc123") == "abc123"


def test_clean_default_on_empty():
    assert clean("") == ""


def test_clean_removes_deletechars():
    assert clean("12-3.4 5", "-. ") == "12345"


def test_clean_keeps_chars_not_in_deletechars():
    assert clean("abc", "a") == "bc"


def test_clean_accepts_list_of_strings():
    assert clean(["1", "2", "3"]) == "123"


def test_clean_accepts_list_with_deletechars():
    assert clean(["1", "2", "-"], "-") == "12"


def test_clean_accepts_dict_iterates_keys():
    assert clean({"a": 1}) == "a"


def test_clean_none_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        clean(None)


def test_clean_int_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        clean(1234)


def test_clean_list_of_ints_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        clean([1, 2, 3])


def test_clean_raises_invalid_format_message_empty():
    with pytest.raises(InvalidFormat) as excinfo:
        clean(None)
    assert excinfo.value.args == ()


# --------------------------------------------------------------------------
# isdigits()
# --------------------------------------------------------------------------
@pytest.mark.parametrize("value", ["0", "123", "00", "9" * 11])
def test_isdigits_true(value):
    assert isdigits(value) is True


@pytest.mark.parametrize(
    "value",
    ["", "12a", "a", " ", "-1", "1.2", "１２", "12 "],
)
def test_isdigits_false(value):
    assert isdigits(value) is False


def test_isdigits_returns_bool_not_match():
    assert isdigits("123") is True


def test_isdigits_trailing_newline_matches_due_to_dollar():
    # re '^[0-9]+$' also matches before one trailing newline
    assert isdigits("12\n") is True


# --------------------------------------------------------------------------
# compact()
# --------------------------------------------------------------------------
def test_compact_strips_spaces_dashes_dots():
    assert compact(" 111.444.777-35 ") == "11144477735"


def test_compact_plain_number():
    assert compact("11144477735") == "11144477735"


def test_compact_mixed_separators():
    assert compact("111 444 777 35") == "11144477735"
    assert compact("111-444-777-35") == "11144477735"
    assert compact("111.444.777.35") == "11144477735"


def test_compact_keeps_other_characters():
    assert compact(" 1a2 ") == "1a2"


def test_compact_empty_string():
    assert compact("") == ""


def test_compact_whitespace_only():
    assert compact("   ") == ""


def test_compact_none_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        compact(None)


# --------------------------------------------------------------------------
# _calc_check_digits()
# --------------------------------------------------------------------------
def test_calc_check_digits_valid_number():
    assert _calc_check_digits("11144477700") == "35"


def test_calc_check_digits_zeroes():
    assert _calc_check_digits("00000000000") == "00"


def test_calc_check_digits_sequence():
    assert _calc_check_digits("12345678900") == "09"


def test_calc_check_digits_returns_two_char_string():
    result = _calc_check_digits("10000000000")
    assert isinstance(result, str)
    assert len(result) == 2


def test_calc_check_digits_typical():
    # traced through the function
    assert _calc_check_digits("52998224700") == "25"


# --------------------------------------------------------------------------
# validate()
# --------------------------------------------------------------------------
def test_validate_valid_plain():
    assert validate(VALID) == VALID


def test_validate_valid_formatted():
    assert validate("111.444.777-35") == VALID


def test_validate_valid_with_spaces():
    assert validate(" 111 444 777 35 ") == VALID


def test_validate_other_valid_number():
    assert validate("99999999050") == "99999999050"


def test_validate_another_valid_number():
    assert validate("10000000019") == "10000000019"


def test_validate_empty_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("")


def test_validate_whitespace_only_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("   ")


def test_validate_single_zero_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("0")


def test_validate_all_zeroes_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("00000000000")


def test_validate_all_zeroes_formatted_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("000.000.000-00")


def test_validate_letters_raise_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("abc")


def test_validate_none_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate(None)


def test_validate_int_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate(11144477735)


def test_validate_trailing_letter_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("111.444.777-35x")


@pytest.mark.parametrize("number", ["1114447773", "111444777355", "1", "1234567890"])
def test_validate_wrong_length_raises_invalid_length(number):
    with pytest.raises(InvalidLength):
        validate(number)


def test_validate_invalid_length_is_invalid_format_instance():
    with pytest.raises(InvalidFormat) as excinfo:
        validate("1114447773")
    assert isinstance(excinfo.value, InvalidLength)


def test_validate_negative_raises_invalid_length():
    # "-1" compacts to "-1" (minus not deleted), so digits check fails first
    with pytest.raises(InvalidFormat):
        validate("-1")


def test_validate_wrong_check_digits_raises_invalid_checksum():
    with pytest.raises(InvalidChecksum):
        validate("11144477736")


def test_validate_wrong_check_digits_formatted_raises_invalid_checksum():
    with pytest.raises(InvalidChecksum):
        validate("111.444.777-36")


def test_validate_wrong_first_check_digit_raises_invalid_checksum():
    with pytest.raises(InvalidChecksum):
        validate("11144477705")


def test_validate_wrong_second_check_digit_raises_invalid_checksum():
    with pytest.raises(InvalidChecksum):
        validate("11144477730")


def test_validate_checksum_error_is_a_value_error():
    with pytest.raises(ValueError):
        validate("11144477736")


def test_validate_returns_compacted_value():
    assert validate(" 111.444.777-35 ") == "11144477735"


# --------------------------------------------------------------------------
# module level extras
# --------------------------------------------------------------------------
def test_module_exposes_regex():
    assert alvo._digits_re.match("123")
    assert alvo._digits_re.match("a") is None
