import pytest

from alvo import (
    ValidationError,
    InvalidFormat,
    InvalidChecksum,
    checksum,
    validate,
)


ALNUM = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class TestHierarchy:
    def test_validation_error_is_value_error(self):
        assert issubclass(ValidationError, ValueError)

    def test_invalid_format_subclass(self):
        assert issubclass(InvalidFormat, ValidationError)
        assert issubclass(InvalidFormat, ValueError)

    def test_invalid_checksum_subclass(self):
        assert issubclass(InvalidChecksum, ValidationError)
        assert issubclass(InvalidChecksum, ValueError)

    def test_siblings(self):
        assert not issubclass(InvalidFormat, InvalidChecksum)
        assert not issubclass(InvalidChecksum, InvalidFormat)


class TestChecksumDecimal:
    def test_zero_string(self):
        assert checksum("0") == 0

    def test_zero_int(self):
        assert checksum(0) == 0

    def test_double_zero(self):
        assert checksum("00") == 0

    def test_single_digit(self):
        assert checksum("1") == 1
        assert checksum("5") == 5
        assert checksum("9") == 9

    def test_int_input_converted_to_str(self):
        assert checksum(1) == 1
        assert checksum(1234) == checksum("1234")

    def test_two_digits(self):
        # reversed "12" -> 2,1 ; doubling 1 -> 2 ; (2 + 2) % 10
        assert checksum("12") == 4

    def test_two_digits_second(self):
        # reversed "13" -> 3,1 ; doubling 1 -> 2 ; (3 + 2) % 10
        assert checksum("13") == 5

    def test_doubling_splits_digits_above_nine(self):
        # "91": values (reversed) 1, 9 ; 9*2=18 -> 1+8=9 ; (1+9)%10 = 0
        assert checksum("91") == 0

    def test_doubling_exactly_ten(self):
        # "55": values reversed 5, 5 ; 5*2=10 -> 1+0=1 ; (5+1)%10 = 6
        assert checksum("55") == 6

    def test_three_digits(self):
        # "123": reversed 3,2,1 ; 3 + (2*2=4) + 1 = 8
        assert checksum("123") == 8

    def test_four_digits(self):
        # "1234": reversed 4,3,2,1 ; (4+2) + (3*2=6) + (1*2=2) = 14 -> 4
        assert checksum("1234") == 4

    def test_leading_zeros_span(self):
        assert checksum("000000000018") == 0

    def test_result_in_range(self):
        for i in range(100):
            r = checksum(str(i))
            assert 0 <= r < 10

    def test_deterministic(self):
        assert checksum("036000291453") == 9
        assert checksum("036000291453") == checksum("036000291453")


class TestChecksumAlphabet:
    def test_custom_alnum(self):
        assert checksum("A", ALNUM) == 10

    def test_custom_alnum_last(self):
        assert checksum("Z", ALNUM) == 35

    def test_custom_alnum_zero(self):
        assert checksum("0", ALNUM) == 0
        assert checksum("00", ALNUM) == 0

    def test_custom_two_chars(self):
        # "10": reversed 0,1 ; 1*2=2 -> 2 ; (0+2) % 36 = 2
        assert checksum("10", ALNUM) == 2

    def test_custom_valid(self):
        assert checksum("999", ALNUM) == 0

    def test_alnum_leading_zero_span(self):
        assert checksum("00A", ALNUM) == checksum("0A", ALNUM)

    def test_binary_alphabet(self):
        # mod 2 alphabet
        assert checksum("1", "01") == 1
        assert checksum("11", "01") == 0
        # reversed "110" -> 0,1,1 ; (0+1) + (1*2=2 -> 1+0=1) = 2 % 2 = 0
        assert checksum("110", "01") == 0

    def test_alphabet_characters_outside(self):
        with pytest.raises(ValueError):
            checksum("x")

    def test_alphabet_characters_outside_custom(self):
        with pytest.raises(ValueError):
            checksum("a", ALNUM)

    def test_none_raises(self):
        with pytest.raises(ValueError):
            checksum(None)


class TestValidate:
    def test_empty_string(self):
        with pytest.raises(InvalidFormat):
            validate("")

    def test_zero_int(self):
        with pytest.raises(InvalidFormat):
            validate(0)

    def test_none(self):
        with pytest.raises(InvalidFormat):
            validate(None)

    def test_empty_list(self):
        with pytest.raises(InvalidFormat):
            validate([])

    def test_invalid_characters(self):
        with pytest.raises(InvalidFormat):
            validate("x")

    def test_invalid_characters_custom(self):
        with pytest.raises(InvalidFormat):
            validate("a", ALNUM)

    def test_bad_checksum(self):
        with pytest.raises(InvalidChecksum):
            validate("1")

    def test_bad_checksum_two(self):
        with pytest.raises(InvalidChecksum):
            validate("1234")

    def test_bad_checksum_long(self):
        with pytest.raises(InvalidChecksum):
            validate("036000291453")

    def test_valid_zero(self):
        assert validate("0") == "0"

    def test_valid_double_zero(self):
        assert validate("00") == "00"

    def test_valid_returns_input(self):
        assert validate("000000000018") == "000000000018"
        assert validate("0018") == "0018"

    def test_valid_alnum_returns_input(self):
        assert validate("999", ALNUM) == "999"
        assert validate("0", ALNUM) == "0"

    def test_invalid_checksum_alnum(self):
        with pytest.raises(InvalidChecksum):
            validate("A", ALNUM)

    def test_invalid_checksum_alnum_two(self):
        with pytest.raises(InvalidChecksum):
            validate("1A", ALNUM)

    def test_exceptions_are_validation_errors(self):
        with pytest.raises(ValidationError):
            validate("")
        with pytest.raises(ValidationError):
            validate("x")
        with pytest.raises(ValidationError):
            validate("1")
