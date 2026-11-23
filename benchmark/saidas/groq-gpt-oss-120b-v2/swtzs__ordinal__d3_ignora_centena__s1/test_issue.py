import pytest
from alvo import ordinal

def test_ordinal_111_returns_th():
    """Numbers ending with 11 should use the 'th' suffix."""
    assert ordinal(111) == "111th"

def test_ordinal_11_uses_th():
    """The special case 11 should also use the 'th' suffix."""
    assert ordinal(11) == "11th"
