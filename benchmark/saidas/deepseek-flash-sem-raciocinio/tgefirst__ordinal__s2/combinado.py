"""Testes de ordinal."""

import math

import pytest

from alvo import ordinal


def test_c1_r1():
    # [R1/normal]
    assert ordinal(1) == '1st'


def test_c1_r1_negativo():
    # [R1/normal] números negativos usam o dígito absoluto
    assert ordinal(-1) == '-1st'
    assert ordinal(-2) == '-2nd'
    assert ordinal(-3) == '-3rd'
