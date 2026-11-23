"""Testes de apnumber."""

import math

import pytest

from alvo import apnumber


def test_c1_r1():
    # [R1/fronteira]
    assert apnumber(0) == 'zero'


def test_c1_r2():
    # [R2/fronteira]
    assert apnumber(9) == 'nine'
