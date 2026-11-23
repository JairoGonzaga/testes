```python
import pytest

from alvo import validate, InvalidFormat


def test_validate_all_zeros_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("00000000000")


def test_validate_all_zeros_with_formatting_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("000.000.000-00")
```