```python
from alvo import validate


def test_validate_returns_int_unchanged():
    number = 79927398713

    result = validate(number)

    assert result == number
    assert isinstance(result, int)


def test_validate_returns_valid_string_unchanged():
    number = "79927398713"

    result = validate(number)

    assert result == number
    assert isinstance(result, str)
```