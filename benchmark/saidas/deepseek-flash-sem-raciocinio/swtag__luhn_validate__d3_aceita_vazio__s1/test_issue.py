import pytest

from alvo import InvalidChecksum, InvalidFormat, validate


def test_validate_empty_string_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('')


def test_validate_empty_string_with_custom_alphabet_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('', alphabet='0123456789')


def test_validate_empty_value_in_sequence_raises_invalid_format():
    for value in ('', ''):
        with pytest.raises(InvalidFormat):
            validate(value)


def test_empty_value_is_a_format_error_not_a_checksum_error():
    # The empty value must be a format problem, not a checksum mismatch.
    with pytest.raises(InvalidFormat) as excinfo:
        validate('')
    assert not isinstance(excinfo.value, InvalidChecksum)
