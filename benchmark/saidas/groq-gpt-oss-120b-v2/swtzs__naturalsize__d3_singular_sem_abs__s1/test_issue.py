# test_issue.py
import pytest
from alvo import naturalsize

def test_negative_one_returns_singular_byte():
    # Bug: currently returns '-1 Bytes', should be '-1 Byte'
    assert naturalsize(-1) == '-1 Byte'

def test_positive_one_returns_singular_byte():
    # Control: the positive case is already correct per the issue description
    assert naturalsize(1) == '1 Byte'
