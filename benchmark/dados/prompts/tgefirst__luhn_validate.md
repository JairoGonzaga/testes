Below is the source code of a Python module, `alvo.py`, and the beginning of its test file,
`test_alvo.py` (imports and the first test function).

Write the NEXT test function of this test file.
- It must pass on this code and test behaviour of the module.
- The answer is only the code of the new test function (plus any extra import it needs at the top).
  It will be appended to the end of the test file shown below.

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

## Test file: test_alvo.py (current content)

```python
"""Testes de validate."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidChecksum


def test_c1_r1():
    # [R1/fronteira]
    with pytest.raises(InvalidFormat):
        validate('')
```
