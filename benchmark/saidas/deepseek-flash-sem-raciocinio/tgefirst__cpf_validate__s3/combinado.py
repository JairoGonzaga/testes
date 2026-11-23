"""Testes de validate."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidLength, InvalidChecksum


def test_c1_r1():
    # [R1/normal]
    assert validate('390.533.447-05') == '39053344705'


def test_c1_r2():
    # [R2/inválido] formato: letras, zeros, vazio e não-iterável
    for bad in ('abcdefghijk', '000.000.000-00', '', '           ', None, 12345678901):
        with pytest.raises(InvalidFormat):
            validate(bad)
