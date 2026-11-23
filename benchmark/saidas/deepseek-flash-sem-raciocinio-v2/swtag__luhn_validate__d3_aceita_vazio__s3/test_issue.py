import pytest

from alvo import validate, InvalidFormat


def test_validate_empty_string_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("")


def test_validate_empty_string_with_alphabet_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("", alphabet="0123456789")
