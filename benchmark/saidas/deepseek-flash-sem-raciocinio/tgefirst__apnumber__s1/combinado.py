"""Testes de apnumber."""

import math

import pytest

from alvo import apnumber


def test_c1_r1():
    # [R1/fronteira]
    assert apnumber(0) == 'zero'


def test_c1_r1_negative_non_finite():
    # [R1/fronteira] valores não finitos negativos ou NaN
    assert apnumber(-math.inf) == '-Inf'
    assert apnumber(math.nan) == 'NaN'
