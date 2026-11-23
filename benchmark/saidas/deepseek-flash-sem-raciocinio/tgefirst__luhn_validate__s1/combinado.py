"""Testes de validate."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidChecksum


def test_c1_r1():
    # [R1/fronteira]
    with pytest.raises(InvalidFormat):
        validate('')


def test_c2_r1():
    # [R1/fronteira] caracteres fora do alfabeto
    with pytest.raises(InvalidFormat):
        validate('abc')
