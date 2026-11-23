You are given an issue report for a small Python project and the full source of the module it
concerns, `alvo.py`.

Write a pytest test file that REPRODUCES the issue:
- the tests must FAIL on the current code (because of the bug described in the issue), and
- the tests must PASS once the issue is fixed.

Rules:
- Import from the module with `from alvo import ...`. The test file will be saved as
  `test_issue.py` in the same folder as `alvo.py`.
- Do not modify, copy or re-implement the module. Do not fix the bug.
- The answer is a single complete, runnable pytest file.

## Issue: validate('') accepts an empty string

An empty value should be rejected with `InvalidFormat`, but it is accepted:

```python
>>> from alvo import validate
>>> validate('')
''
```

Expected: `InvalidFormat` is raised.

## Source: alvo.py

```python
class ValidationError(ValueError):
    """Erro de validação genérico."""


class InvalidFormat(ValidationError):
    """Formato inválido."""


class InvalidChecksum(ValidationError):
    """Soma de verificação não confere."""


def checksum(number, alphabet="0123456789"):
    n = len(alphabet)
    values = tuple(alphabet.index(i) for i in reversed(str(number)))
    return (sum(values[::2]) + sum(sum(divmod(i * 2, n)) for i in values[1::2])) % n


def validate(number, alphabet="0123456789"):
    try:
        valid = checksum(number, alphabet) == 0
    except Exception:
        raise InvalidFormat()
    if not valid:
        raise InvalidChecksum()
    return number
```
