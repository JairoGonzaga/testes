import pytest

from alvo import (
    ValidationError,
    InvalidFormat,
    InvalidChecksum,
    checksum,
    validate,
)


# ---------------- checksum ----------------

def test_checksum_single_zero():
    assert checksum(0) == 0


def test_checksum_single_digit_nonzero():
    assert checksum(1) == 1
    assert checksum(9) == 9


def test_checksum_two_digits():
    # "12": reversed -> 2, 1; values = (2, 1)
    # values[::2] = (2,) sum 2; values[1::2] = (1,); divmod(2,10)=(0,2) sum 2
    # total 4 % 10 == 4
    assert checksum(12) == 4


def test_checksum_three_digits():
    # "121": reversed -> 1, 2, 1 ; values = (1, 2, 1)
    # odd positions sum: values[::2] = (1, 1) -> 2
    # even positions: values[1::2] = (2,) -> divmod(4,10) = (0,4) -> 4
    # total 6 % 10 == 6
    assert checksum(121) == 6


def test_checksum_luhn_valid():
    # A known Luhn-valid number for the default decimal alphabet.
    assert checksum("79927398713") == 0


def test_checksum_luhn_invalid():
    assert checksum("79927398710") != 0


def test_checksum_accepts_string():
    assert checksum("12") == checksum(12) == 4


def test_checksum_custom_alphabet():
    # alphabet "ab": a=0, b=1
    # "ab": reversed -> b, a -> values (1, 0)
    # odd sum: (1,) -> 1 ; even: (0,) -> 0 ; total 1 % 2 == 1
    assert checksum("ab", "ab") == 1
    # "ba": reversed -> a, b -> values (0, 1)
    # odd sum 0 ; even: divmod(2,2) = (1,0) sum 1 ; total 1 % 2 == 1
    assert checksum("ba", "ab") == 1
    assert checksum("aa", "ab") == 0


def test_checksum_alphabet_length_affects_modulus():
    # alphabet of length 3
    # "21": reversed -> 1, 2 ; values (1, 2)
    # odd sum 1 ; even: divmod(4,3) = (1,1) sum 2 ; total 3 % 3 == 0
    assert checksum("21", "012") == 0


def test_checksum_invalid_char_raises():
    with pytest.raises(ValueError):
        checksum("12x")


def test_checksum_empty_string():
    # values is empty -> sum 0 -> 0
    assert checksum("") == 0


# ---------------- exception hierarchy ----------------

def test_exception_hierarchy():
    assert issubclass(ValidationError, ValueError)
    assert issubclass(InvalidFormat, ValidationError)
    assert issubclass(InvalidChecksum, ValidationError)
    assert issubclass(InvalidFormat, ValueError)
    assert issubclass(InvalidChecksum, ValueError)


# ---------------- validate ----------------

def test_validate_valid_returns_number():
    assert validate("79927398713") == "79927398713"


def test_validate_returns_same_object():
    value = "79927398713"
    result = validate(value)
    assert result is value


def test_validate_valid_integer():
    assert validate("0") == "0"


def test_validate_zero_int_is_falsy():
    # 0 is falsy -> InvalidFormat
    with pytest.raises(InvalidFormat):
        validate(0)


def test_validate_empty_string_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("")


def test_validate_none_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate(None)


def test_validate_empty_list_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate([])


def test_validate_bad_checksum_raises_invalid_checksum():
    with pytest.raises(InvalidChecksum):
        validate("79927398710")


def test_validate_single_nonzero_digit_invalid_checksum():
    with pytest.raises(InvalidChecksum):
        validate("1")


def test_validate_non_digit_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("12a")


def test_validate_custom_alphabet_valid():
    assert validate("aa", "ab") == "aa"


def test_validate_custom_alphabet_invalid_checksum():
    # "ab" -> checksum 1, not 0
    with pytest.raises(InvalidChecksum):
        validate("ab", "ab")


def test_validate_custom_alphabet_bad_char():
    with pytest.raises(InvalidFormat):
        validate("az", "ab")


def test_invalid_checksum_is_not_invalid_format():
    with pytest.raises(InvalidChecksum) as exc:
        validate("79927398710")
    assert not isinstance(exc.value, InvalidFormat)
