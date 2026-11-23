"""Testes de naturalsize."""

import math

import pytest

from alvo import naturalsize


def test_c1_r1():
    # [R1/invalida]
    with pytest.raises(ValueError):
        naturalsize('abc')


def test_naturalsize_basic_units():
    assert naturalsize(1) == "1 Byte"
    assert naturalsize(2) == "2 Bytes"
    assert naturalsize(999) == "999 Bytes"
    assert naturalsize(1000) == "1.0 kB"
    assert naturalsize(1024, binary=True) == "1.0 KiB"
    assert naturalsize(1024, gnu=True) == "1.0K"
    assert naturalsize(1, gnu=True) == "1B"
