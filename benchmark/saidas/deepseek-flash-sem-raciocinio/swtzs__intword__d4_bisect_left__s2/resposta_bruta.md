```python
from alvo import intword


def test_intword_googol():
    assert intword(10**100) == "1.0 googol"


def test_intword_googol_float():
    assert intword(1.0e100) == "1.0 googol"


def test_intword_negative_googol():
    assert intword(-(10**100)) == "-1.0 googol"


def test_intword_googol_multiple():
    assert intword(2 * 10**100) == "2.0 googol"
```