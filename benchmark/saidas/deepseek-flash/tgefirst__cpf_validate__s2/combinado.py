"""Testes de validate."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidLength, InvalidChecksum


def test_c1_r1():
    # [R1/normal]
    assert validate('390.533.447-05') == '39053344705'


def test_c1_r2():
    # [R1/exceções]
    with pytest.raises(InvalidFormat):
        validate('abc')

    with pytest.raises(InvalidLength):
        validate('1234567890')

    with pytest.raises(InvalidChecksum):
        validate('39053344706')

    with pytest.raises(InvalidFormat):
        validate('00000000000')
