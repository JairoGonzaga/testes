Below is the source code of a Python module, `alvo.py`.

Write a complete pytest unit-test suite for this module.
- Import with `from alvo import ...`. The test file will be saved as `test_alvo.py` next to `alvo.py`.
- The tests must pass on this code.
- Exercise all of its behaviour (aim for full line and branch coverage), including edge cases and
  error handling, and make the assertions strong enough to catch bugs: the suite will be evaluated
  by coverage and by mutation testing.
- The answer is a single complete, runnable pytest file.

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
    if not bool(number):
        raise InvalidFormat()
    try:
        valid = checksum(number, alphabet) == 0
    except Exception:
        raise InvalidFormat()
    if not valid:
        raise InvalidChecksum()
    return number
```
