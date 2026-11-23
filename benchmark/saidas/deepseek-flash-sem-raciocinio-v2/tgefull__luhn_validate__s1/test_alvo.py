import pytest

from alvo import (
    ValidationError,
    InvalidFormat,
    InvalidChecksum,
    checksum,
    validate,
)


# --------------------------------------------------------------------------- #
# Exception hierarchy
# --------------------------------------------------------------------------- #
def test_validation_error_is_value_error():
    assert issubclass(ValidationError, ValueError)


def test_invalid_format_is_validation_error():
    assert issubclass(InvalidFormat, ValidationError)


def test_invalid_checksum_is_validation_error():
    assert issubclass(InvalidChecksum, ValidationError)


def test_raising_instances():
    with pytest.raises(ValueError):
        raise InvalidFormat()
    with pytest.raises(ValueError):
        raise InvalidChecksum()
    with pytest.raises(ValidationError):
        raise InvalidChecksum()


# --------------------------------------------------------------------------- #
# checksum
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "number, expected",
    [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (9, 9),
        (10, 2),
        (11, 3),
        (18, 0),
        (59, 0),
        (12345, 1),
        ("12345", 1),
        (79927398713, 0),
        ("79927398713", 0),
        (79927398710, 7),
    ],
)
def test_checksum_decimal(number, expected):
    assert checksum(number) == expected


def test_checksum_string_and_int_agree():
    assert checksum(12345) == checksum("12345") == 1
    assert checksum(18) == checksum("18") == 0


def test_checksum_explicit_decimal_alphabet():
    assert checksum(79927398713, "0123456789") == 0
    assert checksum(12345, "0123456789") == 1


def test_checksum_hex_alphabet():
    alphabet = "0123456789ABCDEF"
    assert checksum(255, alphabet) == 1
    assert checksum("FF", alphabet) == 14


def test_checksum_single_char_alphabet_zero():
    assert checksum(0, "0") == 0
    assert checksum("00", "0") == 0


def test_checksum_empty_alphabet_raises_value_error():
    with pytest.raises(ValueError):
        checksum(0, "")


def test_checksum_custom_six_alphabet():
    assert checksum(12345, "012345") == 4


def test_checksum_invalid_character_raises_value_error():
    with pytest.raises(ValueError):
        checksum("abc")
    with pytest.raises(ValueError):
        checksum("12a45")


def test_checksum_character_not_in_custom_alphabet():
    with pytest.raises(ValueError):
        checksum("FFFF", "0123456789")


def test_checksum_result_is_modulo_alphabet_length():
    alphabet = "0123456789ABCDEF"
    n = len(alphabet)
    for number in ["0", "A", "FF", "1234", 999]:
        assert 0 <= checksum(number, alphabet) < n


# --------------------------------------------------------------------------- #
# validate - success
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "number",
    [18, "18", 59, "59", 79927398713, "79927398713", 26, 34, 42],
)
def test_validate_returns_number(number):
    assert validate(number) is number


def test_validate_returns_int_unchanged():
    result = validate(18)
    assert result == 18
    assert isinstance(result, int)


def test_validate_returns_string_unchanged():
    result = validate("18")
    assert result == "18"
    assert isinstance(result, str)


def test_validate_explicit_alphabet_success():
    assert validate(18, "0123456789") == 18


def test_validate_hex_alphabet_success():
    alphabet = "0123456789ABCDEF"
    # 30 -> checksum 0 in hex? compute through checksum to stay consistent
    for candidate in ["0", "00", "11", "18", "1F1"]:
        if checksum(candidate, alphabet) == 0:
            assert validate(candidate, alphabet) == candidate


# --------------------------------------------------------------------------- #
# validate - InvalidFormat
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("number", ["", 0, None, [], (), {}, False, ""])
def test_validate_falsy_raises_invalid_format(number):
    with pytest.raises(InvalidFormat):
        validate(number)


def test_validate_zero_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate(0)


@pytest.mark.parametrize("number", ["abc", "12a45", " 18", "18 ", "1.8", "18\n1"])
def test_validate_non_digit_raises_invalid_format(number):
    with pytest.raises(InvalidFormat):
        validate(number)


def test_validate_character_outside_custom_alphabet_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("FFFF", "0123456789")
    with pytest.raises(InvalidFormat):
        validate("G", "0123456789ABCDEF")


# --------------------------------------------------------------------------- #
# validate - InvalidChecksum
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("number", ["12345", 12345, 79927398710, 1, "19", 10])
def test_validate_bad_checksum_raises_invalid_checksum(number):
    with pytest.raises(InvalidChecksum):
        validate(number)


def test_validate_checksum_error_is_also_validation_error():
    with pytest.raises(ValidationError):
        validate("12345")


def test_validate_format_error_is_also_validation_error():
    with pytest.raises(ValidationError):
        validate("abc")


def test_validate_bad_checksum_with_custom_alphabet():
    with pytest.raises(InvalidChecksum):
        validate("12345", "012345")


# --------------------------------------------------------------------------- #
# integration: valid numbers are exactly those with zero checksum
# --------------------------------------------------------------------------- #
def test_validate_matches_checksum_for_small_numbers():
    for n in range(1, 300):
        if checksum(n) == 0:
            assert validate(n) == n
        else:
            with pytest.raises(InvalidChecksum):
                validate(n)
