"""
Test for the bug described in the issue:
- `naturalsize(999999)` currently returns '1000.0 kB' but should return '1.0 MB'.

The test checks this specific case and ensures the bug is reproduced
by asserting the expected string.  When the bug is fixed, the test
will pass.
"""

import pytest
from alvo import naturalsize


def test_naturalsize_rounds_up_produces_next_unit():
    """
    For a value just below the next unit boundary (999 999 bytes),
    the function should round to 1.0 MB, promoting the suffix.
    """
    expected = "1.0 MB"
    # This assertion will fail with the current implementation, which
    # incorrectly produces '1000.0 kB'.
    assert naturalsize(999999) == expected


# The following additional checks are harmless; they do not influence
# the outcome of the bug but illustrate that the function behaves as
# expected for other values.  They also guard against regressions that
# might affect the rounding logic in unrelated circumstances.

def test_naturalsize_exact_boundary():
    """
    Exactly one million bytes should already be 1.0 MB.
    """
    assert naturalsize(1_000_000) == "1.0 MB"


def test_naturalsize_small_value():
    """
    Values less than the base should return the byte count with 'B'.
    """
    assert naturalsize(999) == "999 Bytes"


def test_naturalsize_binary_mode():
    """
    Binary mode uses 1024 as the base; the same rounding issue does not
    occur here because 999 999 / 1024 ≈ 976.6, which does not round to 1000.
    """
    assert naturalsize(999_999, binary=True) == "976.6 KiB"
