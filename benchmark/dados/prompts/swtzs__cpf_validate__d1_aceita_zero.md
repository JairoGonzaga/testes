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

## Issue: validate() accepts the all-zeros CPF

A CPF made only of zeros is not a valid number and should be rejected with `InvalidFormat`, but it is accepted:

```python
>>> from alvo import validate
>>> validate('00000000000')
'00000000000'
```

Expected: `InvalidFormat` is raised.

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
    if not isdigits(number):
        raise InvalidFormat()
    if len(number) != 11:
        raise InvalidLength()
    if _calc_check_digits(number) != number[-2:]:
        raise InvalidChecksum()
    return number
```
