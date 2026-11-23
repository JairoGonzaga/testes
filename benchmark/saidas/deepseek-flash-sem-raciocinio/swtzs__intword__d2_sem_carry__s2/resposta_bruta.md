```python
import pytest

from alvo import intword


def test_intword_999999_rounds_up_to_million():
    assert intword(999999) == "1.0 million"


def test_intword_negative_999999_rounds_up_to_million():
    assert intword(-999999) == "-1.0 million"


def test_intword_boundary_still_direct_million():
    assert intword(1_000_000) == "1.0 million"
```