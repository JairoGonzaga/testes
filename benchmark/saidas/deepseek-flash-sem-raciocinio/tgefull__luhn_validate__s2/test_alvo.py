import pytest
from alvo import (
    ValidationError,
    InvalidFormat,
    InvalidChecksum,
    checksum,
    validate,
)


class TestExceptionHierarchy:
    def test_validation_error_is_value_error(self):
        assert issubclass(ValidationError, ValueError)

    def test_invalid_format_is_validation_error(self):
        assert issubclass(InvalidFormat, ValidationError)

    def test_invalid_checksum_is_validation_error(self):
        assert issubclass(InvalidChecksum, ValidationError)


class TestChecksum:
    def test_single_zero(self):
        assert checksum(0) == 0

    def test_luhn_valid_number(self):
        # 79927398713 is a classic Luhn-valid number
        assert checksum("79927398713") == 0

    def test_luhn_invalid_number(self):
        assert checksum("79927398710") != 0

    def test_single_digit(self):
        assert checksum("5") == 5

    def test_two_digits(self):
        # values reversed: [5, 4]; doubled position handles 4*2=8 -> 8
        # sum(values[::1]) -> index 0 is 5; index 1 is 4*2=8; 5+8=13 -> 3
        assert checksum("45") == 3

    def test_custom_alphabet(self):
        # hex alphabet: luhn check with alphabet 0-9a-f
        assert checksum("0") == 0
        assert checksum("f") == 15

    def test_alphabet_length_affects_modulo(self):
        # with binary alphabet, results mod 2
        result = checksum("11", alphabet="01")
        assert result in (0, 1)
        assert result == 0

    def test_result_range(self):
        for s in ["0", "1", "19", "12345", "999"]:
            r = checksum(s)
            assert 0 <= r < 10

    def test_invalid_char_raises(self):
        with pytest.raises(ValueError):
            checksum("12a")


class TestValidate:
    def test_valid_number_returns_number(self):
        assert validate("79927398713") == "79927398713"

    def test_valid_returns_same_object_type(self):
        number = "79927398713"
        assert validate(number) is number

    def test_invalid_checksum_raises(self):
        with pytest.raises(InvalidChecksum):
            validate("79927398710")

    def test_empty_string_raises_invalid_format(self):
        with pytest.raises(InvalidFormat):
            validate("")

    def test_zero_string_is_truthy(self):
        # "0" is truthy -> passes format check
        assert validate("0") == "0"

    def test_none_raises_invalid_format(self):
        with pytest.raises(InvalidFormat):
            validate(None)

    def test_zero_integer_raises_invalid_format(self):
        # 0 is falsy -> InvalidFormat
        with pytest.raises(InvalidFormat):
            validate(0)

    def test_invalid_characters_raise_invalid_format(self):
        with pytest.raises(InvalidFormat):
            validate("abc")

    def test_invalid_format_from_checksum_exception(self):
        # alphabet lacks digit -> index raises inside checksum -> InvalidFormat
        with pytest.raises(InvalidFormat):
            validate("9", alphabet="01")

    def test_custom_alphabet_valid(self):
        assert validate("11", alphabet="01") == "11"

    def test_custom_alphabet_invalid_checksum(self):
        with pytest.raises(InvalidChecksum):
            validate("10", alphabet="01")

    def test_preserves_integer_type_when_valid(self):
        # single digit 0 as integer is falsy, but 5 is truthy
        assert validate(5) == 5

    def test_integer_input_valid(self):
        assert validate(79927398713) == 79927398713

    def test_integer_input_invalid_checksum(self):
        with pytest.raises(InvalidChecksum):
            validate(79927398710)

    def test_invalid_format_is_also_validation_error(self):
        with pytest.raises(ValidationError):
            validate("")

    def test_invalid_checksum_is_also_validation_error(self):
        with pytest.raises(ValidationError):
            validate("79927398710")
