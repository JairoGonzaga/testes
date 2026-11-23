```python
import pytest
from alvo import validate


def test_validate_returns_int_unchanged():
    result = validate(79927398713)
    assert result == 79927398713
    assert isinstance(result, int)


def test_validate_returns_str_unchanged():
    result = validate("79927398713")
    assert result == "79927398713"
    assert isinstance(result, str)
```