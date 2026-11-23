```python
import pytest

from alvo import (
    ValidationError,
    InvalidFormat,
    InvalidChecksum,
    checksum,
    validate,
)


class TruthyEmptyString:
    def __bool__(self):
        return True

    def __str__(self):
        return ""


class ValidStringable:
    def __init__(self, text):
        self.text = text

    def __bool__(self):
        return True

    def __str__(self):
        return self.text


def test_validation_error_class_hierarchy():
    assert issubclass(ValidationError, ValueError)
    assert issubclass(InvalidFormat, ValidationError)
    assert issubclass(InvalidChecksum, ValidationError)

    assert InvalidFormat is not InvalidChecksum
    assert isinstance(InvalidFormat(), ValidationError)
    assert isinstance(InvalidChecksum(), ValidationError)
    assert not isinstance(InvalidFormat(), InvalidChecksum)
    assert not isinstance(InvalidChecksum(), InvalidFormat)


@pytest.mark.parametrize(
    "number, expected",
    [
        ("", 0),
        ("0", 0),
        ("00", 0),
        ("7", 7),
        ("99", 8),
        ("12", 4),
        ("13", 5),
        ("12345678", 4),
        ("79927398713", 0),
        ("79927398710", 7),
        (12345678, 4),
        (79927398713, 0),
        (0, 0),
    ],
)
def test_checksum_default_alphabet(number, expected):
    assert checksum(number) == expected


@pytest.mark.parametrize(
    "number, alphabet, expected",
    [
        ("12", "0123", 0),
        ("13", "0123", 1),
        ("123", "0123", 1),
        ("F", "0123456789ABCDEF", 15),
        ("1E", "0123456789ABCDEF", 0),
        ("E1", "0123456789ABCDEF", 14),
    ],
)
def test_checksum_custom_alphabet(number, alphabet, expected):
    assert checksum(number, alphabet) == expected


@pytest.mark.parametrize(
    "number, alphabet",
    [
        ("12x", "0123456789"),
        ("A", "0123456789"),
        ("2", "01"),
    ],
)
def test_checksum_invalid_symbol_raises_value_error(number, alphabet):
    with pytest.raises(ValueError) as exc_info:
        checksum(number, alphabet)

    assert exc_info.type is ValueError


def test_checksum_empty_number_with_empty_alphabet_raises_zero_division_error():
    with pytest.raises(ZeroDivisionError) as exc_info:
        checksum("", alphabet="")

    assert exc_info.type is ZeroDivisionError


def test_checksum_nonempty_number_with_empty_alphabet_raises_value_error():
    with pytest.raises(ValueError) as exc_info:
        checksum("0", alphabet="")

    assert exc_info.type is ValueError


@pytest.mark.parametrize("number", ["79927398713", "0", "00"])
def test_validate_returns_valid_string_unchanged(number):
    result = validate(number)

    assert result == number
    assert result is number


def test_validate_returns_valid_integer_unchanged():
    number = 79927398713
    result = validate(number)

    assert result == number
    assert result is number
    assert isinstance(result, int)


def test_validate_returns_original_truthy_object_when_checksum_valid():
    number = ValidStringable("79927398713")
    result = validate(number)

    assert result is number


@pytest.mark.parametrize(
    "number, alphabet",
    [
        ("12", "0123"),
        ("00", "0123"),
        ("1E", "0123456789ABCDEF"),
    ],
)
def test_validate_returns_valid_custom_alphabet_unchanged(number, alphabet):
    result = validate(number, alphabet)

    assert result == number
    assert result is number


@pytest.mark.parametrize("number", [0, "", None, [], False])
def test_validate_rejects_falsy_values_as_invalid_format(number):
    with pytest.raises(InvalidFormat) as exc_info:
        validate(number)

    assert exc_info.type is InvalidFormat


@pytest.mark.parametrize(
    "number, alphabet",
    [
        ("79927398710", "0123456789"),
        ("13", "0123"),
        ("1F", "0123456789ABCDEF"),
    ],
)
def test_validate_rejects_nonzero_checksum(number, alphabet):
    with pytest.raises(InvalidChecksum) as exc_info:
        validate(number, alphabet)

    assert exc_info.type is InvalidChecksum
    assert not isinstance(exc_info.value, InvalidFormat)


@pytest.mark.parametrize(
    "number, alphabet",
    [
        ("x", "0123456789"),
        ("12x", "0123456789"),
        ("12", "01"),
        ("A", "0123456789"),
        (-1, "0123456789"),
    ],
)
def test_validate_wraps_checksum_value_errors_as_invalid_format(number, alphabet):
    with pytest.raises(InvalidFormat) as exc_info:
        validate(number, alphabet)

    assert exc_info.type is InvalidFormat
    assert not isinstance(exc_info.value, InvalidChecksum)


def test_validate_wraps_non_value_error_from_checksum_as_invalid_format():
    with pytest.raises(InvalidFormat) as exc_info:
        validate(TruthyEmptyString(), alphabet="")

    assert exc_info.type is InvalidFormat
    assert not isinstance(exc_info.value, InvalidChecksum)
```