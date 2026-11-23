"""Testes de apnumber."""

import math

import pytest

from alvo import apnumber


def test_c1_r1():
    # [R1/fronteira]
    assert apnumber(0) == 'zero'


def test_c2_r1():
    # [R1/normal]
    assert apnumber(1) == 'one'


def test_c3_r1():
    # [R1/normal]
    assert apnumber(5) == 'five'


def test_c4_r1():
    # [R1/fronteira]
    assert apnumber(9) == 'nine'


def test_c5_r1():
    # [R1/normal]
    assert apnumber(2) == 'two'


def test_c6_r1():
    # [R1/normal]
    assert apnumber(3) == 'three'


def test_c7_r1():
    # [R1/normal]
    assert apnumber(4) == 'four'


def test_c8_r1():
    # [R1/normal]
    assert apnumber(6) == 'six'


def test_c9_r1():
    # [R1/normal]
    assert apnumber(7) == 'seven'


def test_c10_r1():
    # [R1/normal]
    assert apnumber(8) == 'eight'


def test_c11_r2():
    # [R2/fronteira]
    assert apnumber(10) == '10'


def test_c12_r2():
    # [R2/fronteira]
    assert apnumber(-1) == '-1'


def test_c13_r2():
    # [R2/normal]
    assert apnumber(100) == '100'


def test_c14_r3():
    # [R3/normal]
    assert apnumber('7') == 'seven'


def test_c15_r3():
    # [R3/normal]
    assert apnumber(3.9) == 'three'


def test_c16_r3():
    # [R3/normal]
    assert apnumber('10') == '10'


def test_c17_r4():
    # [R4/invalida]
    assert apnumber('foo') == 'foo'


def test_c18_r4():
    # [R4/invalida]
    assert apnumber(None) == 'None'


def test_c19_r4():
    # [R4/invalida]
    assert apnumber('3.9') == '3.9'


def test_c20_r5():
    # [R5/invalida]
    assert apnumber(float('inf')) == '+Inf'


def test_c21_r5():
    # [R5/invalida]
    assert apnumber(float('-inf')) == '-Inf'


def test_c22_r5():
    # [R5/invalida]
    assert apnumber(float('nan')) == 'NaN'




def test_c23_r3_float_int_negative():
    # [R3/invalida] -4.9 vira -4, que esta fora do intervalo 0..9
    assert apnumber(-4.9) == '-4'
