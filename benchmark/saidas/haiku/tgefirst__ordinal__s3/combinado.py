"""Testes de ordinal."""

import math

import pytest

from alvo import ordinal


def test_c1_r1():
    # [R1/normal]
    assert ordinal(1) == '1st'


def test_c1_r2():
    # [R2/normal]
    assert ordinal(2) == '2nd'
    assert ordinal(3) == '3rd'
    assert ordinal(21) == '21st'
    assert ordinal(112) == '112th'
