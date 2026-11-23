# test_issue.py
"""
Reproduce the issue where negative numbers lose their sign when using
`alvo.intword`.  The current implementation mistakenly sets the
negative prefix to an empty string, so all negative results are
returned without a leading '-'.

These tests confirm that negative numbers are expected to retain
their sign, and that they fail with the buggy code but pass after the
minimal fix.
"""

import pytest

from alvo import intword


def test_negative_small_value():
    # Numbers less than 1 000 should simply return the integer as a
    # string.  The bug drops the minus sign, so the expected output
    # includes the negative sign.
    assert intword(-42) == "-42"


def test_negative_million_value():
    # The example from the issue description.
    assert intword(-1000000) == "-1.0 million"


def test_positive_million_value():
    # Positive numbers are unaffected by the bug and should format
    # normally.
    assert intword(1000000) == "1.0 million"
