```python
import pytest

from alvo import InvalidChecksum, validate


def test_valid_luhn_number_is_accepted():
    assert validate("79927398713") == "79927398713"


def test_invalid_luhn_number_is_rejected():
    with pytest.raises(InvalidChecksum):
        validate("79927398714")
```