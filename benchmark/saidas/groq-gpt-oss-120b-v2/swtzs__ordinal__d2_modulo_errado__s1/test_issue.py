import pytest
from alvo import ordinal


def test_ordinal_11_returns_th():
    """The issue states that ordinal(11) must return '11th'."""
    assert ordinal(11) == "11th"
