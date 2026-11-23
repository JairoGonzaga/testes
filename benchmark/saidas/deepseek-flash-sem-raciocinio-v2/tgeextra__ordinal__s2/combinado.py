"""Testes de ordinal."""

import math

import pytest

from alvo import ordinal


def test_c1_r1():
    # [R1/normal]
    assert ordinal(1) == '1st'


def test_c2_r1():
    # [R1/normal]
    assert ordinal(2) == '2nd'


def test_c3_r1():
    # [R1/normal]
    assert ordinal(3) == '3rd'


def test_c4_r1():
    # [R1/normal]
    assert ordinal(4) == '4th'


def test_c5_r1():
    # [R1/normal]
    assert ordinal(0) == '0th'


def test_c6_r1():
    # [R1/fronteira]
    assert ordinal(10) == '10th'


def test_c7_r1():
    # [R1/fronteira]
    assert ordinal(14) == '14th'


def test_c8_r1():
    # [R1/normal]
    assert ordinal(21) == '21st'


def test_c9_r1():
    # [R1/normal]
    assert ordinal(22) == '22nd'


def test_c10_r1():
    # [R1/normal]
    assert ordinal(103) == '103rd'


def test_c11_r1():
    # [R1/normal]
    assert ordinal(1002) == '1002nd'


def test_c12_r1():
    # [R1/normal]
    assert ordinal(5) == '5th'


def test_c13_r1():
    # [R1/normal]
    assert ordinal(6) == '6th'


def test_c14_r1():
    # [R1/normal]
    assert ordinal(7) == '7th'


def test_c15_r1():
    # [R1/normal]
    assert ordinal(8) == '8th'


def test_c16_r1():
    # [R1/normal]
    assert ordinal(9) == '9th'


def test_c17_r1():
    # [R1/normal]
    assert ordinal(19) == '19th'


def test_c18_r2():
    # [R2/fronteira]
    assert ordinal(11) == '11th'


def test_c19_r2():
    # [R2/normal]
    assert ordinal(12) == '12th'


def test_c20_r2():
    # [R2/fronteira]
    assert ordinal(13) == '13th'


def test_c21_r2():
    # [R2/fronteira]
    assert ordinal(111) == '111th'


def test_c22_r2():
    # [R2/normal]
    assert ordinal(112) == '112th'


def test_c23_r2():
    # [R2/fronteira]
    assert ordinal(113) == '113th'


def test_c24_r2():
    # [R2/normal]
    assert ordinal(1011) == '1011th'


def test_c25_r3():
    # [R3/normal]
    assert ordinal('5') == '5th'


def test_c26_r3():
    # [R3/normal]
    assert ordinal('22') == '22nd'


def test_c27_r3():
    # [R3/normal]
    assert ordinal(3.9) == '3rd'


def test_c28_r4():
    # [R4/invalida]
    assert ordinal('something else') == 'something else'


def test_c29_r4():
    # [R4/invalida]
    assert ordinal(None) == 'None'


def test_c30_r4():
    # [R4/invalida]
    assert ordinal([1, 2, 3]) == '[1, 2, 3]'


def test_c31_r5():
    # [R5/normal]
    assert ordinal(2, gender='female') == '2nd'


def test_c32_r5():
    # [R5/normal]
    assert ordinal(3, 'female') == '3rd'


def test_c33_r5():
    # [R5/normal]
    assert ordinal(11, gender='male') == '11th'


def test_c34_r6():
    # [R6/invalida]
    assert ordinal(float('inf')) == '+Inf'


def test_c35_r6():
    # [R6/invalida]
    assert ordinal(float('-inf')) == '-Inf'


def test_c36_r6():
    # [R6/invalida]
    assert ordinal(float('nan')) == 'NaN'




def test_c37_r3_r6_varios():
    # [R3/R6/outros]
    assert ordinal('inf') == '+Inf'
    assert ordinal('-inf') == '-Inf'
    assert ordinal('nan') == 'NaN'
    assert ordinal(1.0) == '1st'
    assert ordinal(100) == '100th'
    assert ordinal(-1) == '-1th'
    assert ordinal(-112) == '-112th'
    assert ordinal('  7  ') == '7th'
    assert ordinal('3.9') == '3.9'
    assert ordinal({'a': 1}) == "{'a': 1}"
