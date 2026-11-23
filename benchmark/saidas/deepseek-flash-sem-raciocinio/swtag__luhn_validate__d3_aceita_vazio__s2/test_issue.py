import pytest

from alvo import InvalidFormat, ValidationError, validate


def test_validate_empty_string_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("")


def test_validate_empty_string_is_not_accepted():
    # An empty value must never be returned as valid.
    try:
        result = validate("")
    except ValidationError:
        return
    pytest.fail(f"validate('') returned {result!r} instead of raising InvalidFormat")


def test_validate_empty_string_with_custom_alphabet_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("", "abcdefghij")


def test_validate_empty_string_raises_subclass_of_validation_error():
    with pytest.raises(ValidationError) as excinfo:
        validate("")
    assert isinstance(excinfo.value, InvalidFormat)


def test_valid_number_still_passes():
    # Sanity check: the fix must not break valid input.
    assert validate("0") == "0"
    assert validate("00") == "00"
    assert validate("18") == "18"
