# test_issue.py
import pytest
from alvo import naturalsize


def test_naturalsize_binary_scaling():
    """
    When binary=True, the function should use powers of 1024.
    3_000_000 bytes ≈ 2.86 MiB → rounded to 2.9 MiB.
    """
    assert naturalsize(3_000_000, binary=True) == "2.9 MiB"
