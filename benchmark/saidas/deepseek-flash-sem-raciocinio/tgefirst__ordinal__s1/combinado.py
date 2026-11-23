"""Testes de ordinal."""

import math

import pytest

from alvo import ordinal


def test_c1_r1():
    # [R1/normal]
    assert ordinal(1) == '1st'


def test_c1_r2():
    # [R2/limite]
    assert ordinal(1.9) == '1st'
    assert ordinal('2') == '2nd'
    assert ordinal(3.0) == '3rd'
    assert ordinal(0) == '0th'
    assert ordinal(-1) == '-1th'
    assert ordinal(-2) == '-2th'
    assert ordinal(-3) == '-3th'
    assert ordinal(-4) == '-4th'
    assert ordinal(11) == '11th'
    assert ordinal(12) == '12th'
    assert ordinal(13) == '13th'
    assert ordinal(21) == '21st'
    assert ordinal(22) == '22nd'
    assert ordinal(23) == '23rd'
    assert ordinal(101) == '101st'
    assert ordinal(111) == '111th'
    assert ordinal(112) == '112th'
    assert ordinal(113) == '113th'
