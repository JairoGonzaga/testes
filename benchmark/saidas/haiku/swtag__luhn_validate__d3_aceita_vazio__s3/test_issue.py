import pytest

from alvo import InvalidFormat, validate


def test_validate_empty_string_raises_invalid_format():
    # Issue: validate('') currently returns '' instead of raising InvalidFormat.
    with pytest.raises(InvalidFormat):
        validate('')


def test_validate_empty_string_custom_alphabet_raises_invalid_format():
    # Same bug with a non-default alphabet: an empty value must be rejected.
    with pytest.raises(InvalidFormat):
        validate('', alphabet='0123456789ABCDEF')
