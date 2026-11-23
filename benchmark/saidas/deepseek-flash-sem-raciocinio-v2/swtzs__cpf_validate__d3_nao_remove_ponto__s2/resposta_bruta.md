Analysis:
- The issue promises `validate('111.444.777-35')` returns `'11144477735'` (task text gives this expected value).
- `validate` calls `compact`, which calls `clean(number, " -")` — only spaces and hyphens are deleted, not dots.
- So dots remain, `isdigits` fails, and `InvalidFormat` is raised. Fix: also delete `.` in `compact`.
- We assert the returned compact string from the issue, plus the same CPF with spaces/hyphens already handled (expected value stated by issue: compact form).
- Also check an invalid-checksum dotted CPF doesn't silently pass — but keep minimal; only the stated expected output is asserted. Avoid extra guessed constants.

```python
from alvo import validate, InvalidFormat


def test_validate_formatted_cpf_with_dots():
    assert validate('111.444.777-35') == '11144477735'


def test_validate_formatted_cpf_with_dots_and_spaces():
    assert validate(' 111.444.777-35 ') == '11144477735'
```

---- revisão ----

Notes: The issue explicitly states `validate('111.444.777-35') == '11144477735'`; the second test adds surrounding spaces, which `clean` already strips via `.strip()` — but dots are still present so it also fails on the current bug only, and returns the same compact form. Both assertions trace to the issue's stated contract and expected value.

```python
from alvo import validate


def test_validate_formatted_cpf_with_dots():
    assert validate('111.444.777-35') == '11144477735'
```