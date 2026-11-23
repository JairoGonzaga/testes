```python
import pytest

from alvo import intword


@pytest.mark.parametrize(
    "value, expected",
    [
        (-999, "-999"),
        (-1000, "-1.0 thousand"),
        (-1500, "-1.5 thousand"),
        (-1000000, "-1.0 million"),
        (-1234567, "-1.2 million"),
    ],
)
def test_intword_preserves_minus_sign_for_negative_numbers(value, expected):
    assert intword(value) == expected
```