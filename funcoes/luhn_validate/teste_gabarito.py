"""Casos do gabarito (gerado por verificar_gabarito.py)."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidChecksum


def test_g1_r1():
    # [R1/fronteira]
    with pytest.raises(InvalidFormat):
        validate('')


def test_g2_r1():
    # [R1/invalida]
    with pytest.raises(InvalidFormat):
        validate(None)


def test_g3_r1():
    # [R1/fronteira]
    with pytest.raises(InvalidFormat):
        validate(0)


def test_g4_r2():
    # [R2/invalida]
    with pytest.raises(InvalidFormat):
        validate('12a')


def test_g5_r2():
    # [R2/invalida]
    with pytest.raises(InvalidFormat):
        validate('7992 7398 713')


def test_g6_r2():
    # [R2/invalida]
    with pytest.raises(InvalidFormat):
        validate('1A2B', alphabet='0123456789abcdef')


def test_g7_r3():
    # [R3/normal]
    assert validate('79927398713') == '79927398713'


def test_g8_r3():
    # [R3/normal]
    assert validate('4111111111111111') == '4111111111111111'


def test_g9_r3():
    # [R3/normal]
    assert validate('18') == '18'


def test_g10_r3():
    # [R3/normal]
    assert validate('59') == '59'


def test_g11_r3():
    # [R3/normal]
    assert validate('059') == '059'


def test_g12_r3():
    # [R3/fronteira]
    assert validate('0') == '0'


def test_g13_r4():
    # [R4/invalida]
    with pytest.raises(InvalidChecksum):
        validate('79927398710')


def test_g14_r4():
    # [R4/invalida]
    with pytest.raises(InvalidChecksum):
        validate('1')


def test_g15_r4():
    # [R4/invalida]
    with pytest.raises(InvalidChecksum):
        validate('49')


def test_g16_r4():
    # [R4/invalida]
    with pytest.raises(InvalidChecksum):
        validate('4111111111111112')


def test_g17_r5():
    # [R5/normal]
    assert validate(79927398713) == 79927398713


def test_g18_r5():
    # [R5/normal]
    assert validate('00') == '00'


def test_g19_r6():
    # [R6/normal]
    assert validate('1a2b1', alphabet='0123456789abcdef') == '1a2b1'


def test_g20_r6():
    # [R6/invalida]
    with pytest.raises(InvalidChecksum):
        validate('1a2b0', alphabet='0123456789abcdef')
