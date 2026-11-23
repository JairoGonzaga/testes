"""Testes de apnumber."""

import math

import pytest

from alvo import apnumber


def test_c1_r1():
    # [R1/fronteira]
    assert apnumber(0) == 'zero'


def test_c1_r1_integers_and_string_numbers():
    # [R1] números inteiros de 0 a 9 e valores fora do intervalo
    assert apnumber(1) == 'one'
    assert apnumber(9) == 'nine'
    assert apnumber(10) == '10'
    assert apnumber(-1) == '-1'
    assert apnumber(100) == '100'
