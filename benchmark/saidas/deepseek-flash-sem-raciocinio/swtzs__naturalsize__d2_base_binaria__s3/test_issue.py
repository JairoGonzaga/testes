import pytest

from alvo import naturalsize


def test_binary_uses_powers_of_1024():
    assert naturalsize(3000000, binary=True) == "2.9 MiB"


def test_binary_1000():
    # 1000 bytes is less than 1024 -> stays in bytes
    assert naturalsize(1000, binary=True) == "1000 Bytes"


def test_binary_1024():
    assert naturalsize(1024, binary=True) == "1.0 KiB"


def test_binary_exact_mebibyte():
    assert naturalsize(1024 * 1024, binary=True) == "1.0 MiB"


def test_binary_threshold_promotion():
    # just under 1 MiB in binary should be KiB, at/above should be MiB
    assert naturalsize(1024 * 1024 - 1, binary=True) == "1024.0 KiB"
    assert naturalsize(1024 * 1024, binary=True) == "1.0 MiB"
