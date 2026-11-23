import pytest
from alvo import naturalsize

def test_naturalsize_binary_uses_1024():
    # According to the issue, 3,000,000 bytes with binary=True should be formatted as "2.9 MiB"
    assert naturalsize(3_000_000, binary=True) == "2.9 MiB"
