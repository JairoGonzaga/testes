```python
import pytest

from alvo import (
    ValidationError,
    InvalidFormat,
    InvalidChecksum,
    checksum,
    validate,
)


class TestExceptions:
    def test_validation_error_is_value_error(self):
        assert issubclass(ValidationError, ValueError)

    def test_invalid_format_is_validation_error(self):
        assert issubclass(InvalidFormat, ValidationError)

    def test_invalid_checksum_is_validation_error(self):
        assert issubclass(InvalidChecksum, ValidationError)

    def test_instances(self):
        assert isinstance(InvalidFormat(), ValidationError)
        assert isinstance(InvalidChecksum(), ValidationError)
        assert isinstance(InvalidFormat(), ValueError)
        assert isinstance(InvalidChecksum(), ValueError)


class TestChecksum:
    def test_simple_luhn(self):
        # Well-known Luhn for "79927398713" is valid (checksum 0)
        assert checksum("79927398713") == 0

    def test_simple_invalid_luhn(self):
        assert checksum("79927398710") != 0

    def test_single_zero(self):
        assert checksum("0") == 0

    def test_single_nonzero(self):
        assert checksum("1") == 1
        assert checksum("9") == 9

    def test_zero_int(self):
        assert checksum(0) == 0

    def test_int_input(self):
        assert checksum(79927398713) == 0
        assert checksum(79927398710) != 0

    def test_known_valid_numbers(self):
        for n in ["0", "00", "0000000000", "18", "79927398713"]:
            assert checksum(n) == 0

    def test_known_invalid_numbers(self):
        for n in ["1", "12", "123", "79927398712"]:
            assert checksum(n) != 0

    def test_alphabet_hex(self):
        alphabet = "0123456789abcdef"
        # just ensure it computes and stays within range
        result = checksum("0", alphabet)
        assert result == 0
        for s in ["12345", "abcdef", "f", "deadbeef"]:
            r = checksum(s, alphabet)
            assert 0 <= r < len(alphabet)

    def test_alphabet_hex_known(self):
        # Compute manually: single char 'f' -> index 15, one value
        # values = (15,), values[::2]=[15], values[1::2]=[]
        # sum=15 mod 16 = 15
        assert checksum("f", "0123456789abcdef") == 15

    def test_alphabet_hex_two_chars(self):
        # '1f': values in reversed order are (15, 1)
        # values[::2] = 15, values[1::2] = 1 -> divmod(2,16)=(0,2) -> sum=15+2=17 %16=1
        assert checksum("1f", "0123456789abcdef") == 1

    def test_alphabet_hex_double_digit_carry(self):
        # '8': index 8, values=(8,), sum=8
        # '88': reversed (8, 8); values[::2]=8; values[1::2]=8 -> 2*8=16 divmod(16,16)=(1,0) sum=1; total 9
        assert checksum("88", "0123456789abcdef") == 9

    def test_luhn_reference_doubling_wraps(self):
        # For '79': reversed (9, 7); values[::2]=9; values[1::2]=7 -> 14 -> 1+4=5; total 14 %10=4
        assert checksum("79") == 4

    def test_raises_on_invalid_char(self):
        with pytest.raises(ValueError):
            checksum("12a")

    def test_raises_on_empty_string(self):
        with pytest.raises(ValueError):
            checksum("")


class TestValidate:
    def test_valid_returns_number(self):
        assert validate("79927398713") == "79927398713"

    def test_valid_int_returned(self):
        assert validate(79927398713) == 79927398713

    def test_valid_zero_string(self):
        assert validate("0") == "0"

    def test_valid_zero_int_raises(self):
        # 0 is falsy -> InvalidFormat
        with pytest.raises(InvalidFormat):
            validate(0)

    def test_empty_string_raises_invalid_format(self):
        with pytest.raises(InvalidFormat):
            validate("")

    def test_none_raises_invalid_format(self):
        with pytest.raises(InvalidFormat):
            validate(None)

    def test_invalid_checksum_raises(self):
        with pytest.raises(InvalidChecksum):
            validate("79927398712")

    def test_invalid_checksum_single(self):
        with pytest.raises(InvalidChecksum):
            validate("1")

    def test_invalid_char_raises_invalid_format(self):
        with pytest.raises(InvalidFormat):
            validate("12a")

    def test_validate_preserves_type(self):
        result = validate("18")
        assert result == "18"
        assert isinstance(result, str)

    def test_invalid_checksum_exception_is_not_format(self):
        with pytest.raises(InvalidChecksum) as exc_info:
            validate("79927398712")
        assert not isinstance(exc_info.value, InvalidFormat)

    def test_format_exception_is_not_checksum(self):
        with pytest.raises(InvalidFormat) as exc_info:
            validate("")
        assert not isinstance(exc_info.value, InvalidChecksum)

    def test_custom_alphabet_valid(self):
        alphabet = "0123456789abcdef"
        # Find a value with checksum 0 for '1f'+? compute: we know checksum('1f')==1
        # Let's just verify with computed valid number.
        # pick '10': reversed (0,1); values[::2]=0; values[1::2]=1 -> 2 -> sum=2 %16=2
        # We'll construct one: checksum(s) == 0 means valid
        for s in ["00", "1", "06"]:
            # test only ones we can verify
            pass
        # explicit: for hex, try '8' computed 8 not 0
        # use '0' which is 0
        assert validate("0", alphabet) == "0"

    def test_custom_alphabet_invalid_checksum(self):
        alphabet = "0123456789abcdef"
        with pytest.raises(InvalidChecksum):
            validate("8", alphabet)

    def test_custom_alphabet_bad_char(self):
        alphabet = "0123456789abcdef"
        with pytest.raises(InvalidFormat):
            validate("xyz", alphabet)
```