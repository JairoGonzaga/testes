```python
# test_issue.py
import pytest
from alvo import ordinal

def test_ordinal_111_should_be_th():
    # The bug causes 111 to incorrectly return the 'st' suffix.
    # After the fix this assertion will pass.
    assert ordinal(111) == '111th'


@pytest.mark.parametrize(
    "value,expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (14, "14th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (111, "111th"),   # same as above; will fail until bug is fixed
    ],
)
def test_ordinal_suffixes(value, expected):
    assert ordinal(value) == expected
```
```

---- revisão ----

**Notes**: The test only checks behaviour explicitly described by the issue and the code: the correct suffix for 111 and the already‑working suffixes for 11, 12, and 13. No additional assumptions are made.

```python
# test_issue.py
import pytest
from alvo import ordinal


def test_ordinal_111_should_be_th():
    # Bug causes 111 to incorrectly return '111st'.
    # After the fix this assertion will pass.
    assert ordinal(111) == '111th'


@pytest.mark.parametrize(
    "value,expected",
    [
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
    ],
)
def test_ordinal_small_numbers(value, expected):
    assert ordinal(value) == expected
```
