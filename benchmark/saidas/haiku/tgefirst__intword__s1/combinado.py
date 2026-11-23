"""Testes de intword."""

import math

import pytest

from alvo import intword


def test_c1_r1():
    # [R1/normal]
    assert intword(0) == '0'


def test_c1_r2():
    # [R2/boundary]
    assert intword(999999999) == '1.0 billion'
    assert intword(-999999999) == '-1.0 billion'
