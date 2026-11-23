"""Testes de validate."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidChecksum


def test_c1_r1():
    # [R1/fronteira]
    with pytest.raises(InvalidFormat):
        validate('')


def test_c2_r1():
    # [R1/invalida]
    with pytest.raises(InvalidFormat):
        validate(None)


def test_c3_r1():
    # [R1/fronteira]
    with pytest.raises(InvalidFormat):
        validate(0)


def test_c4_r2():
    # [R2/invalida]
    with pytest.raises(InvalidFormat):
        validate('12a')


def test_c5_r2():
    # [R2/invalida]
    with pytest.raises(InvalidFormat):
        validate('7992 7398 713')


def test_c6_r2():
    # [R2/invalida]
    with pytest.raises(InvalidFormat):
        validate('1A2B', alphabet='0123456789abcdef')


def test_c7_r3():
    # [R3/normal]
    assert validate('79927398713') == '79927398713'


def test_c8_r3():
    # [R3/normal]
    assert validate('4111111111111111') == '4111111111111111'


def test_c9_r3():
    # [R3/normal]
    assert validate('18') == '18'


def test_c10_r3():
    # [R3/normal]
    assert validate('59') == '59'


def test_c11_r3():
    # [R3/normal]
    assert validate('059') == '059'


def test_c12_r3():
    # [R3/fronteira]
    assert validate('0') == '0'


def test_c13_r4():
    # [R4/invalida]
    with pytest.raises(InvalidChecksum):
        validate('79927398710')


def test_c14_r4():
    # [R4/invalida]
    with pytest.raises(InvalidChecksum):
        validate('1')


def test_c15_r4():
    # [R4/invalida]
    with pytest.raises(InvalidChecksum):
        validate('49')


def test_c16_r4():
    # [R4/invalida]
    with pytest.raises(InvalidChecksum):
        validate('4111111111111112')


def test_c17_r5():
    # [R5/normal]
    assert validate(79927398713) == 79927398713


def test_c18_r5():
    # [R5/normal]
    assert validate('00') == '00'


def test_c19_r6():
    # [R6/normal]
    assert validate('1a2b1', alphabet='0123456789abcdef') == '1a2b1'




def test_c20_r6_invalida():
    # [R6/invalida]
    with pytest.raises(ValidationError):
        validate('1a2b', alphabet='0123456789abcdef')
