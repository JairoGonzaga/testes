```python
from alvo import validate


def test_textbook_luhn_number_is_accepted():
    number = "79927398713"
    assert validate(number) == number
```