```python
import pytest

from alvo import (
    ValidationError,
    InvalidFormat,
    InvalidChecksum,
    checksum,
    validate,
)


class _FalseyWithValidString:
    def __bool__(self):
        return False

    def __str__(self):
        return "18"


class _TruthyWithValidString:
    def __bool__(self):
        return True

    def __str__(self):
        return "18"


def test_exception_hierarchy():
    assert issubclass(ValidationError, ValueError)
    assert issubclass(InvalidFormat, ValidationError)
    assert issubclass(InvalidChecksum, ValidationError)
    assert not issubclass(InvalidFormat, InvalidChecksum)
    assert not issubclass(InvalidChecksum, InvalidFormat)


@pytest.mark.parametrize(
    "number, expected",
    [
        ("0", 0),
        (0, 0),
        ("1", 1),
        ("9", 9),
        ("12", 4),
        ("18", 0),
        ("26", 0),
        ("123", 8),
        ("56", 7),
        ("65", 8),
        ("79", 4),
        ("79927398713", 0),
        ("79927398710", 7),
        ("00018", 0),
        (18, 0),
        (123, 8),
    ],
)
def test_checksum_decimal(number, expected):
    result = checksum(number)
    assert result == expected
    assert isinstance(result, int)


@pytest.mark.parametrize(
    "number, alphabet, expected",
    [
        ("16", "01234567", 0),
        ("17", "01234567", 1),
        ("70", "01234567", 7),
        ("AA", "AB", 0),
        ("AB", "AB", 1),
        ("f", "0123456789abcdef", 15),
        ("0", "0", 0),
        ("00", "0", 0),
    ],
)
def test_checksum_custom_alphabet(number, alphabet, expected):
    result = checksum(number, alphabet)
    assert result == expected
    assert isinstance(result, int)


def test_checksum_empty_number():
    assert checksum("") == 0
    assert checksum("", "01") == 0


def test_checksum_empty_alphabet_raises_zero_division():
    with pytest.raises(ZeroDivisionError):
        checksum("", "")


def test_checksum_invalid_character_raises_value_error():
    with pytest.raises(ValueError):
        checksum("12a")
    with pytest.raises(ValueError):
        checksum("2", "01")


@pytest.mark.parametrize(
    "number, alphabet, expected",
    [
        ("0", "0123456789", "0"),
        ("18", "0123456789", "18"),
        ("26", "0123456789", "26"),
        ("79927398713", "0123456789", "79927398713"),
        ("00018", "0123456789", "00018"),
        ("16", "01234567", "16"),
        ("AA", "AB", "AA"),
        ("000", "0", "000"),
    ],
)
def test_validate_returns_valid_value(number, alphabet, expected):
    assert validate(number, alphabet) == expected


def test_validate_returns_original_integer_for_valid_number():
    result = validate(18)
    assert result == 18
    assert isinstance(result, int)


def test_validate_returns_same_truthy_object():
    value = _TruthyWithValidString()
    assert validate(value) is value


def test_validate_rejects_falsey_object_even_if_string_looks_valid():
    with pytest.raises(InvalidFormat):
        validate(_FalseyWithValidString())


@pytest.mark.parametrize(
    "number",
    [None, "", 0, 0.0, 0j, False, [], (), {}, set(), b""],
)
def test_validate_falsey_inputs_raise_invalid_format(number):
    with pytest.raises(InvalidFormat):
        validate(number)


@pytest.mark.parametrize(
    "number",
    ["12a", "abc", "12 3", "18.0", "💥", "１２", True],
)
def test_validate_invalid_default_format_raises_invalid_format(number):
    with pytest.raises(InvalidFormat):
        validate(number)


@pytest.mark.parametrize(
    "number, alphabet",
    [
        ("2", "01"),
        ("A", "BC"),
        ("0", ""),
        ("0", None),
        ("12", None),
    ],
)
def test_validate_checksum_errors_become_invalid_format(number, alphabet):
    with pytest.raises(InvalidFormat):
        validate(number, alphabet)


@pytest.mark.parametrize(
    "number",
    ["1", "9", "12", "123", "20", "56", "65", "79", "79927398710"],
)
def test_validate_invalid_checksum_raises_invalid_checksum(number):
    with pytest.raises(InvalidChecksum):
        validate(number)


@pytest.mark.parametrize(
    "number, alphabet",
    [
        ("17", "01234567"),
        ("70", "01234567"),
        ("AB", "AB"),
        ("f", "0123456789abcdef"),
    ],
)
def test_validate_invalid_checksum_custom_alphabet(number, alphabet):
    with pytest.raises(InvalidChecksum):
        validate(number, alphabet)
```