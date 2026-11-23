import pytest
import alvo
from alvo import (
    checksum,
    validate,
    ValidationError,
    InvalidFormat,
    InvalidChecksum,
)


def test_exception_hierarchy():
    assert issubclass(ValidationError, ValueError)
    assert issubclass(InvalidFormat, ValidationError)
    assert issubclass(InvalidChecksum, ValidationError)
    assert isinstance(InvalidFormat(), ValidationError)
    assert isinstance(InvalidChecksum(), ValidationError)
    assert isinstance(InvalidFormat(), ValueError)
    assert isinstance(InvalidChecksum(), ValueError)


@pytest.mark.parametrize(
    ("number", "alphabet", "expected"),
    [
        ("", "0123456789", 0),
        ("", "abc", 0),
        ("0", "0123456789", 0),
        ("00", "0123456789", 0),
        ("1", "0123456789", 1),
        ("9", "0123456789", 9),
        ("18", "0123456789", 0),
        ("81", "0123456789", 8),
        ("79927398713", "0123456789", 0),
        (79927398713, "0123456789", 0),
        ("1234567812345670", "0123456789", 0),
        ("1234567812345671", "0123456789", 1),
        ("a", "abc", 0),
        ("b", "abc", 1),
        ("c", "abc", 2),
        ("aa", "abc", 0),
        ("ab", "abc", 1),
        ("ba", "abc", 2),
        ("cc", "abc", 1),
        ("0", "01", 0),
        ("1", "01", 1),
        ("11", "01", 0),
    ],
)
def test_checksum_exact_values(number, alphabet, expected):
    assert checksum(number, alphabet) == expected


@pytest.mark.parametrize(
    ("number", "alphabet"),
    [
        ("12a", "0123456789"),
        ("A", "0123456789"),
        ("2", "01"),
        ("z", "abc"),
        ("A", "abc"),
    ],
)
def test_checksum_raises_for_character_not_in_alphabet(number, alphabet):
    with pytest.raises(ValueError):
        checksum(number, alphabet)


def test_checksum_empty_string_with_empty_alphabet_raises_zero_division():
    with pytest.raises(ZeroDivisionError):
        checksum("", "")


@pytest.mark.parametrize(
    ("value", "alphabet"),
    [
        ("0", "0123456789"),
        ("00", "0123456789"),
        ("18", "0123456789"),
        ("79927398713", "0123456789"),
        ("1234567812345670", "0123456789"),
        (18, "0123456789"),
        ("a", "abc"),
        ("aa", "abc"),
        ("0", "01"),
        ("11", "01"),
    ],
)
def test_validate_returns_the_original_valid_input(value, alphabet):
    assert validate(value, alphabet) is value


@pytest.mark.parametrize(
    "value",
    [
        0,
        0.0,
        False,
        "",
        None,
        [],
        (),
        {},
    ],
)
def test_validate_rejects_falsy_values_with_invalid_format(value):
    with pytest.raises(InvalidFormat):
        validate(value)


def test_validate_checks_falsy_value_before_calling_checksum(monkeypatch):
    called = False

    def should_not_be_called(*args, **kwargs):
        nonlocal called
        called = True
        raise AssertionError("checksum should not be called for a falsy value")

    monkeypatch.setattr(alvo, "checksum", should_not_be_called)

    with pytest.raises(InvalidFormat):
        validate(0)

    assert called is False


@pytest.mark.parametrize(
    ("value", "alphabet"),
    [
        ("1", "0123456789"),
        ("81", "0123456789"),
        ("79927398710", "0123456789"),
        ("1234567812345671", "0123456789"),
        ("b", "abc"),
        ("ba", "abc"),
        ("cc", "abc"),
        ("1", "01"),
    ],
)
def test_validate_rejects_bad_checksum_with_invalid_checksum(value, alphabet):
    with pytest.raises(InvalidChecksum):
        validate(value, alphabet)


@pytest.mark.parametrize(
    ("value", "alphabet"),
    [
        ("12a", "0123456789"),
        ("-1", "0123456789"),
        ("1.0", "0123456789"),
        ("2", "01"),
        ("z", "abc"),
    ],
)
def test_validate_rejects_unencodable_numbers_with_invalid_format(value, alphabet):
    with pytest.raises(InvalidFormat):
        validate(value, alphabet)


def test_validate_wraps_unexpected_checksum_exception_as_invalid_format(monkeypatch):
    def boom(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(alvo, "checksum", boom)

    with pytest.raises(InvalidFormat):
        validate("123")


def test_validate_uses_the_checksum_result(monkeypatch):
    monkeypatch.setattr(alvo, "checksum", lambda number, alphabet: 0)
    assert validate("anything", "0123456789") == "anything"

    monkeypatch.setattr(alvo, "checksum", lambda number, alphabet: 1)
    with pytest.raises(InvalidChecksum):
        validate("anything", "0123456789")


def test_validate_passes_value_and_alphabet_to_checksum(monkeypatch):
    calls = []

    def fake_checksum(number, alphabet):
        calls.append((number, alphabet))
        return 0

    monkeypatch.setattr(alvo, "checksum", fake_checksum)

    result = validate("42", "abc")

    assert result == "42"
    assert calls == [("42", "abc")]
