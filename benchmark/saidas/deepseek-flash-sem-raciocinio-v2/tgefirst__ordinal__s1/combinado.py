"""Testes de ordinal."""

import math

import pytest

from alvo import ordinal


def test_c1_r1():
    # [R1/normal]
    assert ordinal(1) == '1st'




def test_r1_sufixos_e_nao_finitos():
    # [R1/normal] sufixos e valores não finitos / inválidos
    assert ordinal(2) == '2nd'
    assert ordinal(3) == '3rd'
    assert ordinal(4) == '4th'
    assert ordinal(11) == '11th'
    assert ordinal(12) == '12th'
    assert ordinal(13) == '13th'
    assert ordinal(21) == '21st'
    assert ordinal(111) == '111th'
    assert ordinal(113) == '113th'
    assert ordinal(float('nan')) == 'NaN'
    assert ordinal(float('inf')) == '+Inf'
    assert ordinal(float('-inf')) == '-Inf'
    assert ordinal('abc') == 'abc'
    assert ordinal(True) == '1st'
