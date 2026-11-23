```python
import pytest
from alvo import validate, InvalidFormat, InvalidLength


def test_c27_r7():
    # [R7/normal]
    with pytest.raises(InvalidLength):
        validate('111.111.111-1')
```