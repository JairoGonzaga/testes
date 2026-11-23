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
import re

_digits_re = re.compile(r"^[0-9]+$")


class ValidationError(ValueError):
    """Erro de validação genérico."""


class InvalidFormat(ValidationError):
    """Formato inválido (caracteres não permitidos)."""


class InvalidChecksum(ValidationError):
    """Dígito verificador não confere."""


class InvalidLength(InvalidFormat):
    """Comprimento errado."""


def clean(number, deletechars=""):
    try:
        number = "".join(x for x in number)
    except Exception:
        raise InvalidFormat()
    return "".join(x for x in number if x not in deletechars)


def isdigits(number):
    return bool(_digits_re.match(number))


def compact(number):
    return clean(number, " -.").strip()


def _calc_check_digits(number):
    d1 = sum((10 - i) * int(number[i]) for i in range(9))
    d1 = (11 - d1) % 11 % 10
    d2 = sum((11 - i) * int(number[i]) for i in range(9)) + 2 * d1
    d2 = (11 - d2) % 11 % 10
    return "%d%d" % (d1, d2)


def validate(number):
    number = compact(number)
    if not isdigits(number) or int(number) <= 0:
        raise InvalidFormat()
    if len(number) != 11:
        raise InvalidLength()
    if _calc_check_digits(number) != number[-2:]:
        raise InvalidChecksum()
    return number
```
