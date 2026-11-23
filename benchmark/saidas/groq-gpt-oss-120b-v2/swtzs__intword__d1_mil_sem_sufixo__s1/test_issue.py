import pytest
from alvo import intword

def test_intword_exact_thousand():
    """Exact thousand should be humanized."""
    assert intword(1000) == "1.0 thousand"

def test_intword_below_thousand():
    """Values below a thousand should remain unchanged."""
    assert intword(999) == "999"

def test_intword_above_thousand():
    """Values above a thousand should be humanized correctly."""
    assert intword(1500) == "1.5 thousand"
