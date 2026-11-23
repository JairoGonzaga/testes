"""Testes de apnumber."""

import math

import pytest

from alvo import apnumber


def test_c1_r1():
    # [R1/fronteira]
    assert apnumber(0) == 'zero'


def test_c2_r1_intervalo_e_nao_finitos():
    # [R1/intervalo] números de 0 a 9 viram palavras
    esperado = (
        "zero", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine",
    )
    for numero, palavra in enumerate(esperado):
        assert apnumber(numero) == palavra
        assert apnumber(float(numero)) == palavra

    # fora do intervalo 0 <= valor < 10 é convertido para str
    assert apnumber(10) == "10"
    assert apnumber(-1) == "-1"
    assert apnumber(3.9) == "three"  # truncamento via int()
    assert apnumber(-0.5) == "0"

    # valores não finitos têm formatação especial
    assert apnumber(math.nan) == "NaN"
    assert apnumber(math.inf) == "+Inf"
    assert apnumber(-math.inf) == "-Inf"

    # valores não numéricos não quebram
    assert apnumber("7") == "seven"
    assert apnumber(None) == "None"
