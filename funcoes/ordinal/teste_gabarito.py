"""Casos do gabarito (gerado por verificar_gabarito.py)."""

import math

import pytest

from alvo import ordinal


def test_g1_r1():
    # [R1/normal]
    assert ordinal(1) == '1st'


def test_g2_r1():
    # [R1/normal]
    assert ordinal(2) == '2nd'


def test_g3_r1():
    # [R1/normal]
    assert ordinal(3) == '3rd'


def test_g4_r1():
    # [R1/normal]
    assert ordinal(4) == '4th'


def test_g5_r1():
    # [R1/normal]
    assert ordinal(0) == '0th'


def test_g6_r1():
    # [R1/fronteira]
    assert ordinal(10) == '10th'


def test_g7_r1():
    # [R1/fronteira]
    assert ordinal(14) == '14th'


def test_g8_r1():
    # [R1/normal]
    assert ordinal(21) == '21st'


def test_g9_r1():
    # [R1/normal]
    assert ordinal(22) == '22nd'


def test_g10_r1():
    # [R1/normal]
    assert ordinal(103) == '103rd'


def test_g11_r1():
    # [R1/normal]
    assert ordinal(1002) == '1002nd'


def test_g12_r1():
    # [R1/normal]
    assert ordinal(5) == '5th'


def test_g13_r1():
    # [R1/normal]
    assert ordinal(6) == '6th'


def test_g14_r1():
    # [R1/normal]
    assert ordinal(7) == '7th'


def test_g15_r1():
    # [R1/normal]
    assert ordinal(8) == '8th'


def test_g16_r1():
    # [R1/normal]
    assert ordinal(9) == '9th'


def test_g17_r1():
    # [R1/normal]
    assert ordinal(19) == '19th'


def test_g18_r2():
    # [R2/fronteira]
    assert ordinal(11) == '11th'


def test_g19_r2():
    # [R2/normal]
    assert ordinal(12) == '12th'


def test_g20_r2():
    # [R2/fronteira]
    assert ordinal(13) == '13th'


def test_g21_r2():
    # [R2/fronteira]
    assert ordinal(111) == '111th'


def test_g22_r2():
    # [R2/normal]
    assert ordinal(112) == '112th'


def test_g23_r2():
    # [R2/fronteira]
    assert ordinal(113) == '113th'


def test_g24_r2():
    # [R2/normal]
    assert ordinal(1011) == '1011th'


def test_g25_r3():
    # [R3/normal]
    assert ordinal('5') == '5th'


def test_g26_r3():
    # [R3/normal]
    assert ordinal('22') == '22nd'


def test_g27_r3():
    # [R3/normal]
    assert ordinal(3.9) == '3rd'


def test_g28_r4():
    # [R4/invalida]
    assert ordinal('something else') == 'something else'


def test_g29_r4():
    # [R4/invalida]
    assert ordinal(None) == 'None'


def test_g30_r4():
    # [R4/invalida]
    assert ordinal([1, 2, 3]) == '[1, 2, 3]'


def test_g31_r5():
    # [R5/normal]
    assert ordinal(2, gender='female') == '2nd'


def test_g32_r5():
    # [R5/normal]
    assert ordinal(3, 'female') == '3rd'


def test_g33_r5():
    # [R5/normal]
    assert ordinal(11, gender='male') == '11th'


def test_g34_r6():
    # [R6/invalida]
    assert ordinal(float('inf')) == '+Inf'


def test_g35_r6():
    # [R6/invalida]
    assert ordinal(float('-inf')) == '-Inf'


def test_g36_r6():
    # [R6/invalida]
    assert ordinal(float('nan')) == 'NaN'
