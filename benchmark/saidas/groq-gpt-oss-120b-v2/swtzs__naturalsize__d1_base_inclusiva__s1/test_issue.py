# test_issue.py
import pytest
from alvo import naturalsize

def test_naturalsize_converts_exact_kilobyte():
    # The bug makes this return "1000 Bytes"; the correct output is "1.0 kB".
    assert naturalsize(1000) == "1.0 kB"
