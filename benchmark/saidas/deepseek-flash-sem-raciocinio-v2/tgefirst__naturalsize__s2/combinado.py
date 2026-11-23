"""Testes de naturalsize."""

import math

import pytest

from alvo import naturalsize


def test_c1_r1():
    # [R1/invalida]
    with pytest.raises(ValueError):
        naturalsize('abc')




def test_c2_r2_decimal_binary_gnu():
    # [R2/valida]
    assert naturalsize(0) == "0 Bytes"
    assert naturalsize(1) == "1 Byte"
    assert naturalsize(-1) == "-1 Byte"
    assert naturalsize(2) == "2 Bytes"
    assert naturalsize(0.5) == "0 Bytes"
    assert naturalsize(999) == "999 Bytes"
    assert naturalsize(1000) == "1.0 kB"
    assert naturalsize(1500) == "1.5 kB"
    assert naturalsize(-1500) == "-1.5 kB"
    assert naturalsize(1000000) == "1.0 MB"
    assert naturalsize(1.5) == "1 Bytes"

    assert naturalsize(1024, binary=True) == "1.0 KiB"
    assert naturalsize(1536, binary=True) == "1.5 KiB"
    assert naturalsize(1000000, binary=True) == "976.6 KiB"

    assert naturalsize(1000, gnu=True) == "1000B"
    assert naturalsize(1500, gnu=True) == "1.5K"
    assert naturalsize(1024, gnu=True) == "1.0K"
    assert naturalsize(1000000, gnu=True) == "976.6K"

    assert naturalsize(1000, format="%.0f") == "1 kB"
