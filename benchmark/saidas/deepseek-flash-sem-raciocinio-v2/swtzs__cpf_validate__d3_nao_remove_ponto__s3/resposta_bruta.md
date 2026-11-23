Analysis:
- Issue states `validate('111.444.777-35')` must return `'11144477735'`.
- Formatting removed in `compact()`, which does `clean(number, " -")` — only strips space and hyphen, not dots.
- `clean` keeps any char not in its `deletechars` argument, so dots survive, `isdigits` fails → `InvalidFormat`.
- Expected compact value comes directly from the issue text (digits without separators).
- Also a plain unformatted case `'11144477735'` should keep working and return itself (same digits, from issue).
- Test asserts only those two closely related behaviours.

```python
import pytest

from alvo import validate


def test_validate_formatted_cpf_with_dots():
    assert validate("111.444.777-35") == "11144477735"


def test_validate_unformatted_cpf():
    assert validate("11144477735") == "11144477735"
```

---- revisão ----

Notes: Both assertions are justified — `validate("111.444.777-35") == "11144477735"` is the issue's stated expected output (fails now due to the dot bug, passes after fix), and the unformatted case is the same digits from the issue, verifying the fix doesn't break the compact path.

```python
from alvo import validate


def test_validate_formatted_cpf_with_dots():
    assert validate("111.444.777-35") == "11144477735"


def test_validate_unformatted_cpf():
    assert validate("11144477735") == "11144477735"
```