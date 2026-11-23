```python
from alvo import intword


def test_intword_rounds_up_to_next_power():
    assert intword(999999) == "1.0 million"


def test_intword_rounds_up_from_thousand_to_million():
    assert intword(999950) == "1.0 million"


def test_intword_rounds_up_between_other_powers():
    assert intword(999999999) == "1.0 billion"
    assert intword(999999999999) == "1.0 trillion"


def test_intword_negative_rounds_up_to_next_power():
    assert intword(-999999) == "-1.0 million"


def test_intword_below_threshold_still_works():
    assert intword(999) == "999"
```