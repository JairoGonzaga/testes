"""Testes de intword."""

import math

import pytest

from alvo import intword


def test_c1_r1():
    # [R1/normal]
    assert intword(0) == '0'


def test_c2_r1():
    # [R1/normal]
    assert intword('100') == '100'


def test_c3_r1():
    # [R1/fronteira]
    assert intword(999) == '999'


def test_c4_r2():
    # [R2/fronteira]
    assert intword(1000) == '1.0 thousand'


def test_c5_r2():
    # [R2/normal]
    assert intword('12400') == '12.4 thousand'


def test_c6_r2():
    # [R2/normal]
    assert intword('1000000') == '1.0 million'


def test_c7_r2():
    # [R2/fronteira]
    assert intword(1000000) == '1.0 million'


def test_c8_r2():
    # [R2/normal]
    assert intword(1200000000) == '1.2 billion'


def test_c9_r2():
    # [R2/normal]
    assert intword(8100000000000000000000000000000000) == '8.1 decillion'


def test_c10_r2():
    # [R2/normal]
    assert intword(10**100) == '1.0 googol'


def test_c11_r2():
    # [R2/normal]
    assert intword(10**12) == '1.0 trillion'


def test_c12_r2():
    # [R2/normal]
    assert intword(10**15) == '1.0 quadrillion'


def test_c13_r2():
    # [R2/normal]
    assert intword(10**18) == '1.0 quintillion'


def test_c14_r2():
    # [R2/normal]
    assert intword(10**21) == '1.0 sextillion'


def test_c15_r2():
    # [R2/normal]
    assert intword(10**24) == '1.0 septillion'


def test_c16_r2():
    # [R2/normal]
    assert intword(10**27) == '1.0 octillion'


def test_c17_r2():
    # [R2/normal]
    assert intword(10**30) == '1.0 nonillion'


def test_c18_r2():
    # [R2/normal]
    assert intword(15 * 10**12) == '15.0 trillion'


def test_c19_r3():
    # [R3/fronteira]
    assert intword(999999) == '1.0 million'


def test_c20_r3():
    # [R3/normal]
    assert intword(999999999) == '1.0 billion'


def test_c21_r3():
    # [R3/normal]
    assert intword(10**101) == '10.0 googol'


def test_c22_r4():
    # [R4/normal]
    assert intword(-1200000) == '-1.2 million'


def test_c23_r4():
    # [R4/fronteira]
    assert intword(-999) == '-999'


def test_c24_r4():
    # [R4/fronteira]
    assert intword(-1000) == '-1.0 thousand'


def test_c25_r5():
    # [R5/normal]
    assert intword('1234000', '%0.3f') == '1.234 million'


def test_c26_r5():
    # [R5/normal]
    assert intword(1234000, format='%.0f') == '1 million'


def test_c27_r6():
    # [R6/invalida]
    assert intword(None) == 'None'


def test_c28_r6():
    # [R6/invalida]
    assert intword('abc') == 'abc'


def test_c29_r6():
    # [R6/normal]
    assert intword(12700000.0) == '12.7 million'


def test_c30_r6():
    # [R6/invalida]
    assert intword('12.7') == '12.7'


def test_c31_r7():
    # [R7/invalida]
    assert intword(float('inf')) == '+Inf'


def test_c32_r7():
    # [R7/invalida]
    assert intword(float('-inf')) == '-Inf'


def test_c33_r7():
    # [R7/invalida]
    assert intword(float('nan')) == 'NaN'


def test_c34_r3_r5_negative_and_format_rollover():
    # Rollover to the next unit combined with negative values and custom formatting.
    assert intword(-999999) == '-1.0 million'
    assert intword(999999, '%.0f') == '1 million'
    assert intword(-999999, '%.0f') == '-1 million'
