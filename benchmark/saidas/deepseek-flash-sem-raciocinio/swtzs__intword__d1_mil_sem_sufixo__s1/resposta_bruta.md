```python
import pytest
from alvo import intword


def test_intword_1000():
    assert intword(1000) == "1.0 thousand"


def test_intword_1000_negative():
    assert intword(-1000) == "-1.0 thousand"


def test_intword_1500():
    assert intword(1500) == "1.5 thousand"


def test_intword_below_thousand_unchanged():
    assert intword(999) == "999"


def test_intword_million():
    assert intword(1000000) == "1.0 million"
```