"""Testes de intword."""

import math

import pytest

from alvo import intword


def test_c1_r1():
    # [R1/normal]
    assert intword(0) == '0'


def test_intword_negativo_em_milhoes():
    # valor negativo: prefixo '-' e unidade pela magnitude do valor absoluto
    assert intword(-1500000) == '-1.5 million'
    assert intword(-999) == '-999'
