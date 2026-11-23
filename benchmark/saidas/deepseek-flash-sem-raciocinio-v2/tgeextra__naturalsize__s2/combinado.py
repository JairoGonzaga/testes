"""Testes de naturalsize."""

import math

import pytest

from alvo import naturalsize


def test_c1_r1():
    # [R1/invalida]
    with pytest.raises(ValueError):
        naturalsize('abc')


def test_c2_r1():
    # [R1/invalida]
    with pytest.raises(TypeError):
        naturalsize(None)


def test_c3_r1():
    # [R1/normal]
    assert naturalsize('1000') == '1.0 kB'


def test_c4_r2():
    # [R2/fronteira]
    assert naturalsize(1) == '1 Byte'


def test_c5_r2():
    # [R2/normal]
    assert naturalsize(-1) == '-1 Byte'


def test_c6_r2():
    # [R2/normal]
    assert naturalsize(1, binary=True) == '1 Byte'


def test_c7_r3():
    # [R3/normal]
    assert naturalsize(0) == '0 Bytes'


def test_c8_r3():
    # [R3/normal]
    assert naturalsize(2) == '2 Bytes'


def test_c9_r3():
    # [R3/fronteira]
    assert naturalsize(999) == '999 Bytes'


def test_c10_r3():
    # [R3/normal]
    assert naturalsize(-999) == '-999 Bytes'


def test_c11_r3():
    # [R3/fronteira]
    assert naturalsize(1023, binary=True) == '1023 Bytes'


def test_c12_r3():
    # [R3/normal]
    assert naturalsize(300, gnu=True) == '300B'


def test_c13_r3():
    # [R3/normal]
    assert naturalsize(1, gnu=True) == '1B'


def test_c14_r3():
    # [R3/fronteira]
    assert naturalsize(1023, gnu=True) == '1023B'


def test_c15_r4():
    # [R4/fronteira]
    assert naturalsize(1000) == '1.0 kB'


def test_c16_r4():
    # [R4/normal]
    assert naturalsize(1500) == '1.5 kB'


def test_c17_r4():
    # [R4/normal]
    assert naturalsize(3000000) == '3.0 MB'


def test_c18_r4():
    # [R4/normal]
    assert naturalsize(1000000000) == '1.0 GB'


def test_c19_r4():
    # [R4/normal]
    assert naturalsize(10**28) == '10.0 RB'


def test_c20_r4():
    # [R4/normal]
    assert naturalsize(-1000) == '-1.0 kB'


def test_c21_r4():
    # [R4/normal]
    assert naturalsize(10**12) == '1.0 TB'


def test_c22_r4():
    # [R4/normal]
    assert naturalsize(10**15) == '1.0 PB'


def test_c23_r4():
    # [R4/normal]
    assert naturalsize(10**18) == '1.0 EB'


def test_c24_r4():
    # [R4/normal]
    assert naturalsize(10**21) == '1.0 ZB'


def test_c25_r4():
    # [R4/normal]
    assert naturalsize(10**24) == '1.0 YB'


def test_c26_r5():
    # [R5/fronteira]
    assert naturalsize(1024, binary=True) == '1.0 KiB'


def test_c27_r5():
    # [R5/normal]
    assert naturalsize(3000, True) == '2.9 KiB'


def test_c28_r5():
    # [R5/normal]
    assert naturalsize(-4096, True) == '-4.0 KiB'


def test_c29_r5():
    # [R5/normal]
    assert naturalsize(1048576, binary=True) == '1.0 MiB'


def test_c30_r5():
    # [R5/normal]
    assert naturalsize(2**30, binary=True) == '1.0 GiB'


def test_c31_r5():
    # [R5/normal]
    assert naturalsize(2**40, binary=True) == '1.0 TiB'


def test_c32_r5():
    # [R5/normal]
    assert naturalsize(2**50, binary=True) == '1.0 PiB'


def test_c33_r5():
    # [R5/normal]
    assert naturalsize(2**60, binary=True) == '1.0 EiB'


def test_c34_r5():
    # [R5/normal]
    assert naturalsize(2**70, binary=True) == '1.0 ZiB'


def test_c35_r5():
    # [R5/normal]
    assert naturalsize(2**80, binary=True) == '1.0 YiB'


def test_c36_r5():
    # [R5/normal]
    assert naturalsize(2**90, binary=True) == '1.0 RiB'


def test_c37_r5():
    # [R5/normal]
    assert naturalsize(2**100, binary=True) == '1.0 QiB'


def test_c38_r6():
    # [R6/normal]
    assert naturalsize(3000, False, True) == '2.9K'


def test_c39_r6():
    # [R6/fronteira]
    assert naturalsize(1024, gnu=True) == '1.0K'


def test_c40_r6():
    # [R6/normal]
    assert naturalsize(1024, True, True) == '1.0K'


def test_c41_r7():
    # [R7/normal]
    assert naturalsize(3000, False, True, '%.3f') == '2.930K'


def test_c42_r7():
    # [R7/normal]
    assert naturalsize(1000, format='%.3f') == '1.000 kB'


def test_c43_r8():
    # [R8/fronteira]
    assert naturalsize(999999) == '1.0 MB'


def test_c44_r9():
    # [R9/normal]
    assert naturalsize(10**34 * 3) == '30000.0 QB'




def test_c45_r9_expoente_limitado():
    # [R9/fronteira] exp e' limitado a len(suffix); o sufixo maximo se repete
    assert naturalsize(2**110, binary=True) == '1024.0 QiB'
    assert naturalsize(-10**40) == '-10000000000.0 QB'
    assert naturalsize(10**40, format='%.0f') == '10000000000 QB'
