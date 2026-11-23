```python
# test_issue.py
import pytest
from alvo import intword


def test_intword_rounding_promotion_positive():
    """
    The function should promote to the next unit when rounding pushes a value
    exactly to the power threshold. For 999_999, the rounded value is 1000.0,
    which equals the power 1_000. The expected result is '1.0 million'.
    """
    assert intword(999999) == "1.0 million"


def test_intword_rounding_promotion_negative():
    """
    Negative values should keep the sign but still promote correctly.
    """
    assert intword(-999999) == "-1.0 million"


def test_intword_no_promotion_just_below_threshold():
    """
    Values that round to less than the next power should not be promoted.
    999_500 rounds to 999.5 thousand, not 1000.0 thousand.
    """
    assert intword(999500) == "999.5 thousand"


def test_intword_exact_threshold_no_promotion_needed():
    """
    An exact power should already be in the correct unit, e.g. 1_000_000
    should return '1.0 million'.
    """
    assert intword(1000000) == "1.0 million"
```

---- revisão ----

```python
import pytest
from alvo import intword


def test_intword_rounding_promotion_positive():
    """
    The function should promote to the next unit when rounding pushes a value
    exactly to the power threshold. For 999_999, the rounded value is 1000.0,
    which equals the power 1_000. The expected result is '1.0 million'.
    """
    assert intword(999999) == "1.0 million"
```