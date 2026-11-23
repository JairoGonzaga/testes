"""Testes de validate."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidLength, InvalidChecksum


def test_c1_r1():
    # [R1/normal]
    assert validate('390.533.447-05') == '39053344705'


def test_c1_r2():
    # [R2/limite] números com 11 dígitos e DV válido calculado dinamicamente
    from alvo import _calc_check_digits
    base = '123456789'
    dv = _calc_check_digits(base + '00'[:0] or base)
    number = base + dv
    assert validate(number) == number
