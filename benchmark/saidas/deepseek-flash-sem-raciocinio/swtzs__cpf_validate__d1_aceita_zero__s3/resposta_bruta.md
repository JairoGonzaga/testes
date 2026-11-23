```python
import pytest

from alvo import validate, InvalidFormat


def test_all_zeros_cpf_is_rejected():
    with pytest.raises(InvalidFormat):
        validate('00000000000')
```