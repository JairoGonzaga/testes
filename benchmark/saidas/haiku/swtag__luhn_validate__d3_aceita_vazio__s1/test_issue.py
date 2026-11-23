import pytest

from alvo import InvalidFormat, validate


def test_validate_empty_string_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('')


def test_validate_empty_string_with_custom_alphabet_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('', alphabet='0123456789X')


def test_validate_valid_non_empty_number_still_returns_it():
    assert validate('79927398713') == '79927398713'
