"""Testes de intword."""

import math

import pytest

from alvo import intword


def test_c1_r1():
    # [R1/normal]
    assert intword(0) == '0'


def test_c2_r1():
    # [R1/normal] valor negativo na casa dos milhões
    assert intword(-1500000) == '-1.5 million'
