"""Casos do gabarito (gerado por verificar_gabarito.py)."""

import math

import pytest

from alvo import naturalsize


def test_g1_r1():
    # [R1/invalida]
    with pytest.raises(ValueError):
        naturalsize('abc')


def test_g2_r1():
    # [R1/invalida]
    with pytest.raises(TypeError):
        naturalsize(None)


def test_g3_r1():
    # [R1/normal]
    assert naturalsize('1000') == '1.0 kB'


def test_g4_r2():
    # [R2/fronteira]
    assert naturalsize(1) == '1 Byte'


def test_g5_r2():
    # [R2/normal]
    assert naturalsize(-1) == '-1 Byte'


def test_g6_r2():
    # [R2/normal]
    assert naturalsize(1, binary=True) == '1 Byte'


def test_g7_r3():
    # [R3/normal]
    assert naturalsize(0) == '0 Bytes'


def test_g8_r3():
    # [R3/normal]
    assert naturalsize(2) == '2 Bytes'


def test_g9_r3():
    # [R3/fronteira]
    assert naturalsize(999) == '999 Bytes'


def test_g10_r3():
    # [R3/normal]
    assert naturalsize(-999) == '-999 Bytes'


def test_g11_r3():
    # [R3/fronteira]
    assert naturalsize(1023, binary=True) == '1023 Bytes'


def test_g12_r3():
    # [R3/normal]
    assert naturalsize(300, gnu=True) == '300B'


def test_g13_r3():
    # [R3/normal]
    assert naturalsize(1, gnu=True) == '1B'


def test_g14_r3():
    # [R3/fronteira]
    assert naturalsize(1023, gnu=True) == '1023B'


def test_g15_r4():
    # [R4/fronteira]
    assert naturalsize(1000) == '1.0 kB'


def test_g16_r4():
    # [R4/normal]
    assert naturalsize(1500) == '1.5 kB'


def test_g17_r4():
    # [R4/normal]
    assert naturalsize(3000000) == '3.0 MB'


def test_g18_r4():
    # [R4/normal]
    assert naturalsize(1000000000) == '1.0 GB'


def test_g19_r4():
    # [R4/normal]
    assert naturalsize(10**28) == '10.0 RB'


def test_g20_r4():
    # [R4/normal]
    assert naturalsize(-1000) == '-1.0 kB'


def test_g21_r4():
    # [R4/normal]
    assert naturalsize(10**12) == '1.0 TB'


def test_g22_r4():
    # [R4/normal]
    assert naturalsize(10**15) == '1.0 PB'


def test_g23_r4():
    # [R4/normal]
    assert naturalsize(10**18) == '1.0 EB'


def test_g24_r4():
    # [R4/normal]
    assert naturalsize(10**21) == '1.0 ZB'


def test_g25_r4():
    # [R4/normal]
    assert naturalsize(10**24) == '1.0 YB'


def test_g26_r5():
    # [R5/fronteira]
    assert naturalsize(1024, binary=True) == '1.0 KiB'


def test_g27_r5():
    # [R5/normal]
    assert naturalsize(3000, True) == '2.9 KiB'


def test_g28_r5():
    # [R5/normal]
    assert naturalsize(-4096, True) == '-4.0 KiB'


def test_g29_r5():
    # [R5/normal]
    assert naturalsize(1048576, binary=True) == '1.0 MiB'


def test_g30_r5():
    # [R5/normal]
    assert naturalsize(2**30, binary=True) == '1.0 GiB'


def test_g31_r5():
    # [R5/normal]
    assert naturalsize(2**40, binary=True) == '1.0 TiB'


def test_g32_r5():
    # [R5/normal]
    assert naturalsize(2**50, binary=True) == '1.0 PiB'


def test_g33_r5():
    # [R5/normal]
    assert naturalsize(2**60, binary=True) == '1.0 EiB'


def test_g34_r5():
    # [R5/normal]
    assert naturalsize(2**70, binary=True) == '1.0 ZiB'


def test_g35_r5():
    # [R5/normal]
    assert naturalsize(2**80, binary=True) == '1.0 YiB'


def test_g36_r5():
    # [R5/normal]
    assert naturalsize(2**90, binary=True) == '1.0 RiB'


def test_g37_r5():
    # [R5/normal]
    assert naturalsize(2**100, binary=True) == '1.0 QiB'


def test_g38_r6():
    # [R6/normal]
    assert naturalsize(3000, False, True) == '2.9K'


def test_g39_r6():
    # [R6/fronteira]
    assert naturalsize(1024, gnu=True) == '1.0K'


def test_g40_r6():
    # [R6/normal]
    assert naturalsize(1024, True, True) == '1.0K'


def test_g41_r7():
    # [R7/normal]
    assert naturalsize(3000, False, True, '%.3f') == '2.930K'


def test_g42_r7():
    # [R7/normal]
    assert naturalsize(1000, format='%.3f') == '1.000 kB'


def test_g43_r8():
    # [R8/fronteira]
    assert naturalsize(999999) == '1.0 MB'


def test_g44_r9():
    # [R9/normal]
    assert naturalsize(10**34 * 3) == '30000.0 QB'
