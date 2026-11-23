```python
from alvo import validate


def test_validate_accepts_standard_luhn_number_with_high_doubled_digits():
    number = "79927398713"
    assert validate(number) == number
```