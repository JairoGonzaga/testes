```python
import pytest

from alvo import ordinal


@pytest.mark.parametrize(
    "value",
    [
        "something else",
        "abc",
        "12x",
        "not-a-number",
    ],
)
def test_ordinal_returns_string_for_non_numeric_input(value):
    assert ordinal(value) == str(value)
```