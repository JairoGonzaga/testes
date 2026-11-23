import pytest

from alvo import validate, InvalidFormat, InvalidChecksum, checksum


def test_validate_empty_string_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('')


def test_validate_empty_string_with_custom_alphabet_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('', 'abcdefghij')


def test_validate_empty_bytes_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate(b'')


def test_valid_number_still_accepted():
    # '069' style: compute a valid luhn-like number from the module's checksum
    for candidate in ['0', '00', '18', '90', '1230']:
        if checksum(candidate) == 0:
            assert validate(candidate) == candidate
            break
    else:
        raise AssertionError("no valid sample found")


def test_invalid_number_still_raises_invalid_checksum():
    with pytest.raises(InvalidChecksum):
        validate('1234567812345678')
