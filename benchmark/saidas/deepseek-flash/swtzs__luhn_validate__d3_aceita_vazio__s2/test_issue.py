import pytest

from alvo import validate, InvalidFormat


def test_validate_empty_string_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('')


def test_validate_valid_number_still_passes():
    assert validate('0') == '0'
