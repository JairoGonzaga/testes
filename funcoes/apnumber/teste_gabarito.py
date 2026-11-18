"""Casos do gabarito (gerado por verificar_gabarito.py)."""

import math

import pytest

from alvo import apnumber


def test_g1_r1():
    # [R1/fronteira]
    assert apnumber(0) == 'zero'


def test_g2_r1():
    # [R1/normal]
    assert apnumber(1) == 'one'


def test_g3_r1():
    # [R1/normal]
    assert apnumber(5) == 'five'


def test_g4_r1():
    # [R1/fronteira]
    assert apnumber(9) == 'nine'


def test_g5_r1():
    # [R1/normal]
    assert apnumber(2) == 'two'


def test_g6_r1():
    # [R1/normal]
    assert apnumber(3) == 'three'


def test_g7_r1():
    # [R1/normal]
    assert apnumber(4) == 'four'


def test_g8_r1():
    # [R1/normal]
    assert apnumber(6) == 'six'


def test_g9_r1():
    # [R1/normal]
    assert apnumber(7) == 'seven'


def test_g10_r1():
    # [R1/normal]
    assert apnumber(8) == 'eight'


def test_g11_r2():
    # [R2/fronteira]
    assert apnumber(10) == '10'


def test_g12_r2():
    # [R2/fronteira]
    assert apnumber(-1) == '-1'


def test_g13_r2():
    # [R2/normal]
    assert apnumber(100) == '100'


def test_g14_r3():
    # [R3/normal]
    assert apnumber('7') == 'seven'


def test_g15_r3():
    # [R3/normal]
    assert apnumber(3.9) == 'three'


def test_g16_r3():
    # [R3/normal]
    assert apnumber('10') == '10'


def test_g17_r4():
    # [R4/invalida]
    assert apnumber('foo') == 'foo'


def test_g18_r4():
    # [R4/invalida]
    assert apnumber(None) == 'None'


def test_g19_r4():
    # [R4/invalida]
    assert apnumber('3.9') == '3.9'


def test_g20_r5():
    # [R5/invalida]
    assert apnumber(float('inf')) == '+Inf'


def test_g21_r5():
    # [R5/invalida]
    assert apnumber(float('-inf')) == '-Inf'


def test_g22_r5():
    # [R5/invalida]
    assert apnumber(float('nan')) == 'NaN'
