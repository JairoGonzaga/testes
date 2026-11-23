```python
import pytest

from alvo import ordinal


@pytest.mark.parametrize("value", [11, 12, 13, 111, 112, 113])
def test_numbers_ending_in_11_12_13_use_th(value):
    assert ordinal(value) == f"{value}th"
```