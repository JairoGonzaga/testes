Analysis:
- The docstring/issue states `validate()` accepts the `XXX.XXX.XXX-XX` format; dots are to be removed before validating.
- `compact()` only removes spaces and hyphens (`clean(number, " -")`), so dots remain and `isdigits` fails → `InvalidFormat`.
- Issue's expected value: `validate('111.444.777-35')` returns `'11144477735'`.
- Check digit computation for `11144477735`: per `_calc_check_digits`, digits `111444777` give `d1=3`, `d2=5` (as the issue calls it valid), matching the last two chars.
- Also a related dotted case: `validate('111.444.777/35')`? No — only dots/hyphens/spaces stated; keep to dots case and a plain case returning compact form.

```python
import pytest

from alvo import validate, InvalidFormat


def test_validate_formatted_cpf_with_dots():
    assert validate("111.444.777-35") == "11144477735"


def test_validate_plain_cpf_unaffected():
    assert validate("11144477735") == "11144477735"
```

---- revisão ----

Notes: Both assertions are fine — `'11144477735'` comes from the issue text, and the plain-CPF case is traced from the code (checksum matches per `_calc_check_digits`); it guards against a fix breaking the compact path.

```python
import pytest

from alvo import validate


def test_validate_formatted_cpf_with_dots():
    assert validate("111.444.777-35") == "11144477735"


def test_validate_plain_cpf_unaffected():
    assert validate("11144477735") == "11144477735"
```