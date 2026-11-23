"""Testes de naturalsize."""

import math

import pytest

from alvo import naturalsize


def test_c1_r1():
    # [R1/invalida]
    with pytest.raises(ValueError):
        naturalsize('abc')


def test_c1_r2():
    # [R2/valida]
    assert naturalsize(1) == "1 Byte"
    assert naturalsize(999) == "999 Bytes"
