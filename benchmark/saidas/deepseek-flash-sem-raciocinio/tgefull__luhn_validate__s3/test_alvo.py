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
    def test_returns_int(self):
        result = checksum("79927398713")
        assert isinstance(result, int)

    def test_known_valid_luhn(self):
        assert checksum("79927398713") == 0

    def test_known_invalid_luhn(self):
        assert checksum("79927398710") != 0

    def test_checksum_is_zero_for_zero(self):
        assert checksum(0) == 0

    def test_accepts_integer(self):
        assert checksum(79927398713) == checksum("79927398713")

    def test_modulo_range(self):
        for n in ["0", "1", "12", "123", "1234", "12345", "123456"]:
            result = checksum(n)
            assert 0 <= result < 10

    def test_custom_alphabet(self):
        # With a binary-ish alphabet, checksum uses n=2
        result = checksum("1011", alphabet="01")
        assert 0 <= result < 2

    def test_custom_alphabet_known(self):
        # values reversed: 1,1,0,1 -> even idx 1+0=1, odd idx 1,1
        # divmod(1*2,2)=(1,0)->1 ; divmod(1*2,2)=1 -> sum=2 ; total=3 ; %2=1
        assert checksum("1011", alphabet="01") == 1

    def test_custom_alphabet_hex(self):
        result = checksum("ff", alphabet="0123456789abcdef")
        assert 0 <= result < 16

    def test_invalid_character_raises_value_error(self):
        with pytest.raises(ValueError):
            checksum("12x4")

    def test_invalid_alphabet_for_number(self):
        with pytest.raises(ValueError):
            checksum("2", alphabet="01")

    def test_empty_string(self):
        # str("") == "", values empty -> sum empty == 0 -> 0 % n
        assert checksum("") == 0

    def test_single_digit(self):
        assert checksum("5") == 5 % 10

    def test_length_changes_result_predictably(self):
        # even-positioned (from reversed) digits sum plus luhn-doubled odd positions
        assert checksum("0") == 0
        assert checksum("00") == 0


class TestValidate:
    def test_returns_the_number_when_valid(self):
        assert validate("79927398713") == "79927398713"

    def test_returns_same_object_integer(self):
        assert validate(79927398713) == 79927398713

    def test_invalid_checksum_raises(self):
        with pytest.raises(InvalidChecksum):
            validate("79927398710")

    def test_empty_string_raises_invalid_format(self):
        with pytest.raises(InvalidFormat):
            validate("")

    def test_none_raises_invalid_format(self):
        with pytest.raises(InvalidFormat):
            validate(None)

    def test_zero_raises_invalid_format(self):
        with pytest.raises(InvalidFormat):
            validate(0)

    def test_non_numeric_raises_invalid_format(self):
        with pytest.raises(InvalidFormat):
            validate("abcd")

    def test_invalid_chars_converted_to_invalid_format(self):
        with pytest.raises(InvalidFormat):
            validate("12x4")

    def test_invalid_format_also_is_validation_error(self):
        with pytest.raises(ValidationError):
            validate("")

    def test_invalid_checksum_is_validation_error(self):
        with pytest.raises(ValidationError):
            validate("79927398710")

    def test_custom_alphabet_valid(self):
        # From test_checksum: "1011" has checksum 1 with alphabet "01", not valid.
        # Find a valid one: need even sum of digits + doubled odd sum % 2 == 0
        # "0" reversed: [0] even sum 0 -> 0 valid
        assert validate("0", alphabet="01") == "0"

    def test_custom_alphabet_invalid_checksum(self):
        with pytest.raises(InvalidChecksum):
            validate("1011", alphabet="01")

    def test_custom_alphabet_invalid_char(self):
        with pytest.raises(InvalidFormat):
            validate("102", alphabet="01")
