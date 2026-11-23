```python
import pytest

from alvo import InvalidFormat, validate


def test_validate_rejects_empty_string():
    with pytest.raises(InvalidFormat):
        validate("")
```