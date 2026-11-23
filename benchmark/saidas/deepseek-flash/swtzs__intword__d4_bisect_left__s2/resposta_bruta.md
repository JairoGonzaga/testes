```python
from alvo import intword


def test_intword_googol():
    assert intword(10**100) == "1.0 googol"
```