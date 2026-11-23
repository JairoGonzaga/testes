"""Testes de ordinal."""

import math

import pytest

from alvo import ordinal


def test_c1_r1():
    # [R1/normal]
    assert ordinal(1) == '1st'
