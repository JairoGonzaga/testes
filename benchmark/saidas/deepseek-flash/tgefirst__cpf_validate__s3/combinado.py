"""Testes de validate."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidLength, InvalidChecksum


def test_c1_r1():
    # [R1/normal]
    assert validate('390.533.447-05') == '39053344705'


def test_c1_r2():
    # [R1/erros] Formato, comprimento e dígito verificador inválidos.
    with pytest.raises(InvalidFormat):
        validate('390.533.447-0a')
    with pytest.raises(InvalidLength):
        validate('390.533.447-0')
    with pytest.raises(InvalidChecksum):
        validate('390.533.447-04')
