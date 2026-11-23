"""Testes de ordinal."""

import math

import pytest

from alvo import ordinal


def test_c1_r1():
    # [R1/normal]
    assert ordinal(1) == '1st'


def test_c1_r2():
    # [R2/special]
    assert ordinal(11) == '11th'
    assert ordinal(12) == '12th'
    assert ordinal(13) == '13th'
    assert ordinal(111) == '111th'
