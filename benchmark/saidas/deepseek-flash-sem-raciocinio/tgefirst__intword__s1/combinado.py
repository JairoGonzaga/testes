"""Testes de intword."""

import math

import pytest

from alvo import intword


def test_c1_r1():
    # [R1/normal]
    assert intword(0) == '0'


def test_c1_r2_negative_and_invalid_values():
    # [R2/negative + valores inválidos]
    assert intword(-1500) == '-1.5 thousand'
    assert intword(-1000000) == '-1.0 million'
    assert intword("123") == "123"
    assert intword(None) == "None"
    assert intword("abc") == "abc"
