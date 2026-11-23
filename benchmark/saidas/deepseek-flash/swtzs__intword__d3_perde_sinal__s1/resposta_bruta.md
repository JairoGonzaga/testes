```python
import pytest

from alvo import intword


@pytest.mark.parametrize(
    "value, expected",
    [
        (-1000000, "-1.0 million"),
        (-1000, "-1.0 thousand"),
        (-1500, "-1.5 thousand"),
        (-999, "-999"),
        (-999999, "-1.0 million"),
    ],
)
def test_intword_negative_values_preserve_minus_sign(value, expected):
    assert intword(value) == expected
```