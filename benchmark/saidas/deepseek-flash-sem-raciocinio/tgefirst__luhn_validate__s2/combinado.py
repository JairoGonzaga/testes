"""Testes de validate."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidChecksum


def test_c1_r1():
    # [R1/fronteira]
    with pytest.raises(InvalidFormat):
        validate('')


def test_c2_r2():
    # [R2/estrutura] um valor com dígito verificador válido pelo algoritmo de Luhn
    # passa na validação e é retornado inalterado
    number = '79927398713'
    assert validate(number) == number
