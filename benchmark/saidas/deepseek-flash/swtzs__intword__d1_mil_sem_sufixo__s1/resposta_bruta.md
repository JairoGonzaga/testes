```python
from alvo import intword


def test_intword_1000_is_humanized():
    assert intword(1000) == "1.0 thousand"


def test_intword_negative_1000_is_humanized():
    assert intword(-1000) == "-1.0 thousand"


def test_intword_999_is_unchanged():
    assert intword(999) == "999"
```