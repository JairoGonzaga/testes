import pytest
from alvo import validate, InvalidFormat


def test_empty_string_raises_invalid_format():
    """An empty string must be rejected with InvalidFormat."""
    with pytest.raises(InvalidFormat):
        validate('')


def test_valid_number_is_returned_unchanged():
    """A known valid number should be accepted and returned."""
    assert validate('0') == '0'
