# test_issue.py
# This test reproduces the bug reported in the issue:
# intword(1000) incorrectly returns '1000' instead of a human‑readable form.
# The test will fail with the current implementation and pass once the
# boundary condition is corrected.

import pytest
from alvo import intword


def test_intword_boundary_exact_thousand():
    """
    The value 1000 should be expressed as "1.0 thousand".
    The current implementation incorrectly returns the raw integer
    because the boundary check uses <= instead of <.
    """
    assert intword(1000) == "1.0 thousand"


def test_intword_below_thousand():
    """
    Numbers less than 1000 should remain unchanged.
    """
    assert intword(999) == "999"
    assert intword(0) == "0"


def test_intword_above_thousand():
    """
    Numbers just above the threshold should already use the suffix.
    """
    assert intword(1001) == "1.0 thousand"
