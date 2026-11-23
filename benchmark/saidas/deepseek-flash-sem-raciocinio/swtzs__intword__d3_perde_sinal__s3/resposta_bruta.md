```python
import math

import pytest

from alvo import intword


def test_intword_negative_million():
    assert intword(-1000000) == "-1.0 million"


def test_intword_negative_thousand():
    assert intword(-1500) == "-1.5 thousand"


@pytest.mark.parametrize(
    "value,expected",
    [
        (-1000000, "-1.0 million"),
        (-1500, "-1.5 thousand"),
        (-1000, "-1.0 thousand"),
        (-2000000000, "-2.0 billion"),
        (-100, "-100"),
        (-1, "-1"),
        (-1000000000000000000000000000000, "-1.0 decillion"),
    ],
)
def test_intword_negative_values_keep_sign(value, expected):
    assert intword(value) == expected


def test_intword_positive_still_correct():
    assert intword(1000000) == "1.0 million"


def test_intword_negative_inf():
    assert intword(-math.inf) == "-Inf"


def test_intword_negative_nan():
    assert intword(-math.nan) == "NaN"
```