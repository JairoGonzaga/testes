"""Casos do gabarito (gerado por verificar_gabarito.py)."""

import math

import pytest

from alvo import intword


def test_g1_r1():
    # [R1/normal]
    assert intword(0) == '0'


def test_g2_r1():
    # [R1/normal]
    assert intword('100') == '100'


def test_g3_r1():
    # [R1/fronteira]
    assert intword(999) == '999'


def test_g4_r2():
    # [R2/fronteira]
    assert intword(1000) == '1.0 thousand'


def test_g5_r2():
    # [R2/normal]
    assert intword('12400') == '12.4 thousand'


def test_g6_r2():
    # [R2/normal]
    assert intword('1000000') == '1.0 million'


def test_g7_r2():
    # [R2/fronteira]
    assert intword(1000000) == '1.0 million'


def test_g8_r2():
    # [R2/normal]
    assert intword(1200000000) == '1.2 billion'


def test_g9_r2():
    # [R2/normal]
    assert intword(8100000000000000000000000000000000) == '8.1 decillion'


def test_g10_r2():
    # [R2/normal]
    assert intword(10**100) == '1.0 googol'


def test_g11_r2():
    # [R2/normal]
    assert intword(10**12) == '1.0 trillion'


def test_g12_r2():
    # [R2/normal]
    assert intword(10**15) == '1.0 quadrillion'


def test_g13_r2():
    # [R2/normal]
    assert intword(10**18) == '1.0 quintillion'


def test_g14_r2():
    # [R2/normal]
    assert intword(10**21) == '1.0 sextillion'


def test_g15_r2():
    # [R2/normal]
    assert intword(10**24) == '1.0 septillion'


def test_g16_r2():
    # [R2/normal]
    assert intword(10**27) == '1.0 octillion'


def test_g17_r2():
    # [R2/normal]
    assert intword(10**30) == '1.0 nonillion'


def test_g18_r2():
    # [R2/normal]
    assert intword(15 * 10**12) == '15.0 trillion'


def test_g19_r3():
    # [R3/fronteira]
    assert intword(999999) == '1.0 million'


def test_g20_r3():
    # [R3/normal]
    assert intword(999999999) == '1.0 billion'


def test_g21_r3():
    # [R3/normal]
    assert intword(10**101) == '10.0 googol'


def test_g22_r4():
    # [R4/normal]
    assert intword(-1200000) == '-1.2 million'


def test_g23_r4():
    # [R4/fronteira]
    assert intword(-999) == '-999'


def test_g24_r4():
    # [R4/fronteira]
    assert intword(-1000) == '-1.0 thousand'


def test_g25_r5():
    # [R5/normal]
    assert intword('1234000', '%0.3f') == '1.234 million'


def test_g26_r5():
    # [R5/normal]
    assert intword(1234000, format='%.0f') == '1 million'


def test_g27_r6():
    # [R6/invalida]
    assert intword(None) == 'None'


def test_g28_r6():
    # [R6/invalida]
    assert intword('abc') == 'abc'


def test_g29_r6():
    # [R6/normal]
    assert intword(12700000.0) == '12.7 million'


def test_g30_r6():
    # [R6/invalida]
    assert intword('12.7') == '12.7'


def test_g31_r7():
    # [R7/invalida]
    assert intword(float('inf')) == '+Inf'


def test_g32_r7():
    # [R7/invalida]
    assert intword(float('-inf')) == '-Inf'


def test_g33_r7():
    # [R7/invalida]
    assert intword(float('nan')) == 'NaN'
