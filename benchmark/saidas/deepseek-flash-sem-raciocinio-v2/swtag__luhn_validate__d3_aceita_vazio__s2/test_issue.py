import pytest

from alvo import validate, InvalidFormat


def test_empty_string_rejected():
    with pytest.raises(InvalidFormat):
        validate('')


def test_empty_string_rejected_with_alphabet():
    with pytest.raises(InvalidFormat):
        validate('', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
