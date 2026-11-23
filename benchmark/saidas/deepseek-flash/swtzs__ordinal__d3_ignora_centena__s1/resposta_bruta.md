```python
import pytest

from alvo import ordinal


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (1011, "1011th"),
        (1012, "1012th"),
        (1013, "1013th"),
    ],
)
def test_ordinal_suffix_for_numbers_ending_in_11_12_13(value, expected):
    assert ordinal(value) == expected
```