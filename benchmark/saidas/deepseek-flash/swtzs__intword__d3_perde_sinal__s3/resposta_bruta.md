```python
import pytest

from alvo import intword


@pytest.mark.parametrize(
    "value, expected",
    [
        (-5, "-5"),
        (-999, "-999"),
        (-1000, "-1.0 thousand"),
        (-1000000, "-1.0 million"),
        (-1500000, "-1.5 million"),
        (-2000000000, "-2.0 billion"),
    ],
)
def test_intword_preserves_minus_sign_for_negative_numbers(value, expected):
    assert intword(value) == expected
```