```python
import math

import pytest

from alvo import intword


def test_intword_negative_million():
    assert intword(-1000000) == "-1.0 million"


def test_intword_negative_small_number():
    assert intword(-123) == "-123"


def test_intword_negative_thousand():
    assert intword(-23000) == "-23.0 thousand"


def test_intword_positive_unchanged():
    assert intword(1000000) == "1.0 million"


def test_intword_negative_inf():
    assert intword(float("-inf")) == "-Inf"


def test_intword_negative_nan_sign_not_required():
    assert intword(float("-nan")) == "NaN"
```