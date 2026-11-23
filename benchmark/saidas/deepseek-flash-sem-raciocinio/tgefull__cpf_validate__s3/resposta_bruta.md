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
    def test_clean_no_delete(self):
        assert clean("abc") == "abc"

    def test_clean_with_delete(self):
        assert clean("a-b-c", "-") == "abc"

    def test_clean_multiple_delete_chars(self):
        assert clean("a-b-c.d e", " -. ") == "abcde"

    def test_clean_all_deleted(self):
        assert clean("---", "-") == ""

    def test_clean_empty(self):
        assert clean("") == ""

    def test_clean_list_input(self):
        assert clean(["a", "b", "c"]) == "abc"

    def test_clean_tuple_input(self):
        assert clean(("a", "b", "-c"), "-") == "abc"

    def test_clean_none_raises(self):
        with pytest.raises(InvalidFormat):
            clean(None)

    def test_clean_int_raises(self):
        with pytest.raises(InvalidFormat):
            clean(42)

    def test_clean_raises_is_validation_error(self):
        with pytest.raises(ValidationError):
            clean(None)


class TestIsdigits:
    def test_digits(self):
        assert isdigits("12345") is True

    def test_zeros(self):
        assert isdigits("0") is True

    def test_empty(self):
        assert isdigits("") is False

    def test_letters(self):
        assert isdigits("12a") is False

    def test_negative(self):
        assert isdigits("-123") is False

    def test_space(self):
        assert isdigits("12 3") is False

    def test_newline(self):
        # regex is anchored so trailing newline should not match
        assert isdigits("123\n") is False

    def test_returns_bool(self):
        assert isinstance(isdigits("123"), bool)
        assert isinstance(isdigits("abc"), bool)


class TestCompact:
    def test_compact_plain(self):
        assert compact("12345678901") == "12345678901"

    def test_compact_spaces(self):
        assert compact("123 456 789 01") == "12345678901"

    def test_compact_dashes(self):
        assert compact("123-456-789-01") == "12345678901"

    def test_compact_dots(self):
        assert compact("123.456.789.01") == "12345678901"

    def test_compact_mixed(self):
        assert compact(" 123.456-789 01 ") == "12345678901"

    def test_compact_other_chars_kept(self):
        assert compact("12a3") == "12a3"

    def test_compact_none_raises(self):
        with pytest.raises(InvalidFormat):
            compact(None)


class TestCalcCheckDigits:
    def test_known_value(self):
        # compute manually to make sure the algorithm is unchanged
        number = "123456789"
        d1 = sum((10 - i) * int(number[i]) for i in range(9))
        d1 = (11 - d1) % 11 % 10
        d2 = sum((11 - i) * int(number[i]) for i in range(9)) + 2 * d1
        d2 = (11 - d2) % 11 % 10
        assert _calc_check_digits(number) == "%d%d" % (d1, d2)

    def test_returns_string_of_two(self):
        result = _calc_check_digits("000000000")
        assert isinstance(result, str)
        assert len(result) == 2
        assert result.isdigit()

    def test_zeros(self):
        # 0*... => d1 = (11-0)%11%10 = 0 ; d2 = (11-0)%11%10 = 0
        assert _calc_check_digits("000000000") == "00"


class TestValidate:
    def test_valid_number(self):
        base = "123456789"
        number = base + _calc_check_digits(base)
        assert validate(number) == number

    def test_valid_number_with_formatting(self):
        base = "123456789"
        number = base + _calc_check_digits(base)
        formatted = "{}.{}.{}-{}".format(number[0:3], number[3:6], number[6:9], number[9:])
        assert validate(formatted) == number

    def test_valid_with_spaces(self):
        base = "987654321"
        number = base + _calc_check_digits(base)
        spaced = " ".join(number)
        assert validate(spaced) == number

    def test_valid_returns_compacted(self):
        base = "111222333"
        number = base + _calc_check_digits(base)
        assert validate(" " + number + " ") == number

    def test_non_digits_raises(self):
        with pytest.raises(InvalidFormat):
            validate("abcdefghijk")

    def test_zero_raises(self):
        with pytest.raises(InvalidFormat):
            validate("00000000000")

    def test_all_zeros_raises_format(self):
        with pytest.raises(InvalidFormat):
            validate("0" * 11)

    def test_short_after_clean_raises_length(self):
        with pytest.raises(InvalidLength):
            validate("123")

    def test_long_raises_length(self):
        with pytest.raises(InvalidLength):
            validate("123456789012")

    def test_empty_raises_format(self):
        with pytest.raises(InvalidFormat):
            validate("")

    def test_bad_checksum_raises(self):
        base = "123456789"
        good = base + _calc_check_digits(base)
        # flip the last digit
        last = str((int(good[-1]) + 1) % 10)
        bad = good[:-1] + last
        with pytest.raises(InvalidChecksum):
            validate(bad)

    def test_bad_first_check_digit_raises(self):
        base = "123456789"
        good = base + _calc_check_digits(base)
        first = str((int(good[-2]) + 1) % 10)
        bad = good[:-2] + first + good[-1]
        with pytest.raises(InvalidChecksum):
            validate(bad)

    def test_invalid_length_is_invalid_format(self):
        with pytest.raises(InvalidFormat):
            validate("123")

    def test_invalid_checksum_is_validation_error(self):
        base = "123456789"
        good = base + _calc_check_digits(base)
        bad = good[:-1] + str((int(good[-1]) + 1) % 10)
        with pytest.raises(ValidationError):
            validate(bad)

    def test_none_raises(self):
        with pytest.raises(InvalidFormat):
            validate(None)
```
```