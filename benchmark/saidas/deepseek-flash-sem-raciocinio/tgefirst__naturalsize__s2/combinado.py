"""Testes de naturalsize."""

import math

import pytest

from alvo import naturalsize


def test_c1_r1():
    # [R1/invalida]
    with pytest.raises(ValueError):
        naturalsize('abc')


def test_decimal_basics():
    # [R1/R2/R4/R5/valida] comportamento padrão em base decimal
    assert naturalsize(0) == "0 Bytes"
    assert naturalsize(1) == "1 Byte"
    assert naturalsize(2) == "2 Bytes"
    assert naturalsize(999) == "999 Bytes"
    assert naturalsize(1000) == "1.0 kB"
    assert naturalsize(1500) == "1.5 kB"
    assert naturalsize(-1500) == "-1.5 kB"
    assert naturalsize(10**6) == "1.0 MB"
    assert naturalsize(10**9) == "1.0 GB"


def test_binary_and_gnu():
    # [R3/R4/R5/valida] variantes binária e GNU (base 1024)
    assert naturalsize(1, binary=True) == "1 Byte"
    assert naturalsize(1000, binary=True) == "1000 Bytes"
    assert naturalsize(1024, binary=True) == "1.0 KiB"
    assert naturalsize(1536, binary=True) == "1.5 KiB"
    assert naturalsize(1024**2, binary=True) == "1.0 MiB"

    assert naturalsize(0, gnu=True) == "0B"
    assert naturalsize(1, gnu=True) == "1B"
    assert naturalsize(999, gnu=True) == "999B"
    assert naturalsize(1024, gnu=True) == "1.0K"
    assert naturalsize(1536, gnu=True) == "1.5K"
    assert naturalsize(1024**2, gnu=True) == "1.0M"


def test_rounding_exp_increment():
    # [R6/valida] incremento da expoente quando arredondamento atinge a base
    assert naturalsize(999_950) == "999.95 kB"
    assert naturalsize(999_999) == "1.0 MB"
