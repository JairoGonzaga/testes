```python
import pytest

from alvo import validate


def test_valid_luhn_number_79927398713():
    assert validate("79927398713") == "79927398713"
```