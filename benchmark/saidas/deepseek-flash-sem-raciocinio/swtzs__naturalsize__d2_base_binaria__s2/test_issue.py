import pytest
from alvo import naturalsize


def test_binary_3000000_is_2_9_mib():
    assert naturalsize(3000000, binary=True) == '2.9 MiB'


def test_binary_1024_is_1_kib():
    assert naturalsize(1024, binary=True) == '1.0 KiB'


def test_binary_1048576_is_1_mib():
    assert naturalsize(1048576, binary=True) == '1.0 MiB'


def test_binary_1536_is_1_5_kib():
    assert naturalsize(1536, binary=True) == '1.5 KiB'


def test_binary_uses_powers_of_1024_boundary():
    # 1000 is below 1024, so should still be reported in bytes (or below KiB)
    # while 1100 should be a fraction of a KiB, not a KiB.
    assert naturalsize(1100, binary=True) == '1.1 KiB'
