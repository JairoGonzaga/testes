```python
import pytest

from alvo import ordinal


@pytest.mark.parametrize(
    "value, expected",
    [
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (1011, "1011th"),
        (1012, "1012th"),
        (1013, "1013th"),
    ],
)
def test_numbers_ending_in_11_12_13_use_th(value, expected):
    assert ordinal(value) == expected
```