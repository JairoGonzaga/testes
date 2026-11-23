"""Test for the apnumber bug where 9 is not spelled out.

The original issue states that apnumber(9) should return 'nine' but currently returns '9'.
This test reproduces that behaviour.
"""

from alvo import apnumber


def test_apnumber_9_spelled_out():
    """apnumber(9) should return 'nine' (single‑digit numbers are spelled)."""
    assert apnumber(9) == 'nine'
