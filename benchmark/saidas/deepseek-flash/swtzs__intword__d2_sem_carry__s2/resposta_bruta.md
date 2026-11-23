```python
from alvo import intword


def test_intword_promotes_suffix_after_rounding_to_next_power():
    assert intword(999999) == "1.0 million"


def test_intword_promotes_suffix_after_rounding_to_next_power_negative():
    assert intword(-999999) == "-1.0 million"


def test_intword_promotes_suffix_after_rounding_from_million_to_billion():
    assert intword(999999999) == "1.0 billion"
```