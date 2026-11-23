"""Testes de validate."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidChecksum


def test_c1_r1():
    # [R1/fronteira]
    with pytest.raises(InvalidFormat):
        validate('')


def test_c1_r2():
    # [R2/caminho feliz]
    assert validate('79927398713') == '79927398713'
