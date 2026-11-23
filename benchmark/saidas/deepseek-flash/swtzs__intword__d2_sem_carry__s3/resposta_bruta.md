```python
from alvo import intword


def test_intword_promotes_suffix_when_rounding_reaches_next_power():
    assert intword(999999) == "1.0 million"


def test_intword_promotes_suffix_at_larger_power_boundaries():
    assert intword(999999999) == "1.0 billion"
    assert intword(999999999999) == "1.0 trillion"


def test_intword_promotes_suffix_for_negative_values():
    assert intword(-999999) == "-1.0 million"
```