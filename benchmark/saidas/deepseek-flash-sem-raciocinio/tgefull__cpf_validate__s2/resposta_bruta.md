```python
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


class TestExceptions:
    def test_hierarchy(self):
        assert issubclass(ValidationError, ValueError)
        assert issubclass(InvalidFormat, ValidationError)
        assert issubclass(InvalidChecksum, ValidationError)
        assert issubclass(InvalidLength, InvalidFormat)


class TestClean:
    def test_no_deletechars(self):
        assert clean("12345") == "12345"

    def test_delete_some(self):
        assert clean("12-34 56.78", " -.") == "12345678"

    def test_delete_all(self):
        assert clean("abc", "abc") == ""

    def test_empty(self):
        assert clean("") == ""

    def test_deletechars_subset(self):
        assert clean("a-b-c", "-") == "abc"

    def test_list_input(self):
        assert clean(["1", "2", "3"]) == "123"

    def test_list_input_with_delete(self):
        assert clean(["1", "-", "2"], "-") == "12"

    def test_invalid_input_raises(self):
        with pytest.raises(InvalidFormat):
            clean(12345)

    def test_invalid_input_none(self):
        with pytest.raises(InvalidFormat):
            clean(None)

    def test_invalid_raises_validation_error(self):
        with pytest.raises(ValidationError):
            clean(1.5)


class TestIsdigits:
    def test_digits(self):
        assert isdigits("123") is True

    def test_empty(self):
        assert isdigits("") is False

    def test_letters(self):
        assert isdigits("12a") is False

    def test_sign(self):
        assert isdigits("-12") is False

    def test_space(self):
        assert isdigits("1 2") is False

    def test_decimal(self):
        assert isdigits("1.2") is False


class TestCompact:
    def test_spaces(self):
        assert compact(" 123 ") == "123"

    def test_separators(self):
        assert compact("1-2.3 4") == "1234"

    def test_all_separators(self):
        assert compact(" - . ") == ""

    def test_no_separators(self):
        assert compact("12345678901") == "12345678901"


class TestCalcCheckDigits:
    def test_known_valid(self):
        # BR CPF valid example
        assert _calc_check_digits("12345678909") == "09"

    def test_calc_does_not_use_check_positions(self):
        # The last two digits should not affect computation
        assert _calc_check_digits("12345678900") == _calc_check_digits(
            "12345678999"
        )

    def test_calc_specific_value(self):
        assert _calc_check_digits("00000000000") == "00"

    def test_calc_ones(self):
        # 111111111 -> d1, d2
        assert _calc_check_digits("11111111111") == "11"


class TestValidate:
    def test_valid_cpf(self):
        assert validate("12345678909") == "12345678909"

    def test_valid_cpf_with_formatting(self):
        assert validate("123.456.789-09") == "12345678909"

    def test_valid_cpf_spaces(self):
        assert validate(" 123 456 789 09 ") == "12345678909"

    def test_all_zeros_invalid_format(self):
        with pytest.raises(InvalidFormat):
            validate("00000000000")

    def test_empty_invalid(self):
        with pytest.raises(InvalidFormat):
            validate("")

    def test_letters_invalid(self):
        with pytest.raises(InvalidFormat):
            validate("abcdefghijk")

    def test_too_short(self):
        with pytest.raises(InvalidLength):
            validate("1234567890")

    def test_too_long(self):
        with pytest.raises(InvalidLength):
            validate("123456789012")

    def test_invalid_checksum(self):
        with pytest.raises(InvalidChecksum):
            validate("12345678900")

    def test_invalid_checksum_formatted(self):
        with pytest.raises(InvalidChecksum):
            validate("123.456.789-00")

    def test_length_checked_after_format(self):
        # formatted valid length but non-digit after stripping
        with pytest.raises(InvalidFormat):
            validate("123.456.789-0a")

    def test_invalid_checksum_subclass_validation(self):
        with pytest.raises(ValidationError):
            validate("12345678900")

    def test_all_ones_is_checksum_or_length(self):
        # 11111111111 -> check digits "11" -> valid
        assert validate("11111111111") == "11111111111"

    def test_another_valid_cpf(self):
        # CPF 11144477735 is valid
        assert validate("111.444.777-35") == "11144477735"
```