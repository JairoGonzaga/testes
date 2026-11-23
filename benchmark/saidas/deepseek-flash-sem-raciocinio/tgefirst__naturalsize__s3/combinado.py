"""Testes de naturalsize."""

import math

import pytest

from alvo import naturalsize


def test_c1_r1():
    # [R1/invalida]
    with pytest.raises(ValueError):
        naturalsize('abc')


def test_c2_r1():
    # [R1/valida] exatamente 1 byte recebe singular, e -1 também
    assert naturalsize(1) == "1 Byte"
    assert naturalsize(-1) == "1 Byte"
