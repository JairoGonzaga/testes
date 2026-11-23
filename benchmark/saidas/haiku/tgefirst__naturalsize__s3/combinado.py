"""Testes de naturalsize."""

import math

import pytest

from alvo import naturalsize


def test_c1_r1():
    # [R1/invalida]
    with pytest.raises(ValueError):
        naturalsize('abc')


def test_c2_r1():
    # [R1/valida]
    assert naturalsize(1500) == "1.5 kB"
