```python
import pytest

from alvo import validate, InvalidFormat


def test_validate_rejects_all_zero_cpf():
    with pytest.raises(InvalidFormat):
        validate("00000000000")
```