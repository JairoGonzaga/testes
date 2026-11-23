import pytest

from alvo import validate, InvalidFormat


def test_all_zeros_rejected():
    with pytest.raises(InvalidFormat):
        validate('00000000000')


def test_all_zeros_rejected_formatted():
    with pytest.raises(InvalidFormat):
        validate('000.000.000-00')
