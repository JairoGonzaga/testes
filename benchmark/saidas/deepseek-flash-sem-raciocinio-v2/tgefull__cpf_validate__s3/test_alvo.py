import pytest

import alvo
from alvo import (
    clean,
    isdigits,
    compact,
    validate,
    _calc_check_digits,
    ValidationError,
    InvalidFormat,
    InvalidChecksum,
    InvalidLength,
)


class TestHierarchy:
    def test_validation_error_is_value_error(self):
        assert issubclass(ValidationError, ValueError)

    def test_invalid_format_is_validation_error(self):
        assert issubclass(InvalidFormat, ValidationError)

    def test_invalid_checksum_is_validation_error(self):
        assert issubclass(InvalidChecksum, ValidationError)

    def test_invalid_length_is_invalid_format(self):
        assert issubclass(InvalidLength, InvalidFormat)
        assert issubclass(InvalidLength, ValidationError)


class TestClean:
    def test_no_delete_chars(self):
        assert clean("123abc") == "123abc"

    def test_delete_chars(self):
        assert clean("1a2b3c", "abc") == "123"

    def test_delete_chars_none_present(self):
        assert clean("123", "abc") == "123"

    def test_empty_string(self):
        assert clean("") == ""

    def test_empty_deletechars(self):
        assert clean("abc", "") == "abc"

    def test_accepts_list(self):
        assert clean(["1", "2", "3"]) == "123"

    def test_accepts_tuple(self):
        assert clean(("1", "a", "2"), "a") == "12"

    def test_rejects_int(self):
        with pytest.raises(InvalidFormat):
            clean(123)

    def test_rejects_none(self):
        with pytest.raises(InvalidFormat) as excinfo:
            clean(None)
        assert type(excinfo.value) is InvalidFormat


class TestIsdigits:
    def test_digits(self):
        assert isdigits("123") is True

    def test_empty(self):
        assert isdigits("") is False

    def test_with_letter(self):
        assert isdigits("12a") is False

    def test_with_space(self):
        assert isdigits("12 3") is False

    def test_trailing_newline_matches(self):
        # '$' allows a trailing newline, so regex matches
        assert isdigits("123\n") is True

    def test_leading_newline(self):
        assert isdigits("\n123") is False

    def test_returns_bool(self):
        assert isinstance(isdigits("1"), bool)


class TestCompact:
    def test_spaces_dashes_dots(self):
        assert compact("123.456.789-09") == "12345678909"

    def test_with_spaces(self):
        assert compact(" 123 456 789 09 ") == "12345678909"

    def test_plain(self):
        assert compact("12345678909") == "12345678909"

    def test_strips_whitespace(self):
        assert compact("  123  ") == "123"

    def test_keeps_other_chars(self):
        assert compact("12a3") == "12a3"

    def test_invalid_input(self):
        with pytest.raises(InvalidFormat):
            compact(12345)


class TestCalcCheckDigits:
    @pytest.mark.parametrize(
        "base,expected",
        [
            ("123456789", "09"),
            ("987654321", "00"),
            ("000000000", "00"),
            ("111111111", "11"),
            ("123456780", "62"),
        ],
    )
    def test_values(self, base, expected):
        assert _calc_check_digits(base) == expected

    def test_returns_two_chars(self):
        result = _calc_check_digits("123456789")
        assert isinstance(result, str)
        assert len(result) == 2


class TestValidate:
    def test_valid_plain(self):
        assert validate("12345678909") == "12345678909"

    def test_valid_formatted(self):
        assert validate("123.456.789-09") == "12345678909"

    def test_valid_spaced(self):
        assert validate("123 456 789 09") == "12345678909"

    def test_valid_other(self):
        assert validate("98765432100") == "98765432100"

    def test_valid_repeated(self):
        assert validate("11111111111") == "11111111111"

    def test_returns_compact(self):
        assert validate(" 123-456.789-09 ") == "12345678909"

    def test_invalid_checksum(self):
        with pytest.raises(InvalidChecksum):
            validate("12345678900")

    def test_invalid_checksum_second_digit(self):
        with pytest.raises(InvalidChecksum):
            validate("12345678908")

    def test_zero(self):
        with pytest.raises(InvalidFormat):
            validate("00000000000")

    def test_letters(self):
        with pytest.raises(InvalidFormat):
            validate("12345678a09")

    def test_empty(self):
        with pytest.raises(InvalidFormat):
            validate("")

    def test_too_short(self):
        with pytest.raises(InvalidLength):
            validate("1234567890")

    def test_too_long(self):
        with pytest.raises(InvalidLength):
            validate("123456789091")

    def test_too_short_after_compacting(self):
        with pytest.raises(InvalidLength):
            validate("123.456.789")

    def test_invalid_input_type(self):
        with pytest.raises(InvalidFormat):
            validate(None)

    def test_invalid_length_is_invalid_format(self):
        with pytest.raises(InvalidFormat):
            validate("123")

    def test_length_checked_after_format(self):
        # '0' single char -> int value 0 -> InvalidFormat, not InvalidLength
        with pytest.raises(InvalidFormat):
            validate("0")
