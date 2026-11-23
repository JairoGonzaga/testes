Below is the source code of a Python module, `alvo.py`, and its complete test file, `test_alvo.py`.

Write ONE additional test function that improves this test suite: it should test behaviour that the
existing tests do not check yet (increasing coverage or the ability to catch bugs).
- It must pass on this code.
- The answer is only the code of the new test function (plus any extra import it needs at the top).
  It will be appended to the end of the test file shown below.

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

## Test file: test_alvo.py (current content)

```python
"""Testes de validate."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidLength, InvalidChecksum


def test_c1_r1():
    # [R1/normal]
    assert validate('390.533.447-05') == '39053344705'


def test_c2_r1():
    # [R1/normal]
    assert validate(' 390 533 447 05 ') == '39053344705'


def test_c3_r1():
    # [R1/normal]
    assert validate('390533447-05') == '39053344705'


def test_c4_r2():
    # [R2/invalida]
    with pytest.raises(InvalidFormat):
        validate('390.533.447=0')


def test_c5_r2():
    # [R2/invalida]
    with pytest.raises(InvalidFormat):
        validate('390.533.447/05')


def test_c6_r2():
    # [R2/invalida]
    with pytest.raises(InvalidFormat):
        validate('')


def test_c7_r2():
    # [R2/fronteira]
    with pytest.raises(InvalidFormat):
        validate('000.000.000-00')


def test_c8_r2():
    # [R2/invalida]
    with pytest.raises(InvalidFormat):
        validate('12a')


def test_c9_r2():
    # [R2/invalida]
    with pytest.raises(InvalidFormat):
        validate(None)


def test_c10_r2():
    # [R2/invalida]
    with pytest.raises(InvalidFormat):
        validate('39053344705X')


def test_c11_r3():
    # [R3/fronteira]
    with pytest.raises(InvalidLength):
        validate('3905334470')


def test_c12_r3():
    # [R3/fronteira]
    with pytest.raises(InvalidLength):
        validate('390533447051')


def test_c13_r3():
    # [R3/invalida]
    with pytest.raises(InvalidLength):
        validate('123')


def test_c14_r4():
    # [R4/invalida]
    with pytest.raises(InvalidChecksum):
        validate('231.002.999-00')


def test_c15_r4():
    # [R4/invalida]
    with pytest.raises(InvalidChecksum):
        validate('529.982.247-26')


def test_c16_r4():
    # [R4/invalida]
    with pytest.raises(InvalidChecksum):
        validate('123.456.789-10')


def test_c17_r5():
    # [R5/invalida]
    with pytest.raises(InvalidFormat):
        validate('12a')


def test_c18_r5():
    # [R5/invalida]
    with pytest.raises(InvalidFormat):
        validate('00000')


def test_c19_r5():
    # [R5/invalida]
    with pytest.raises(InvalidLength):
        validate('1234567890')


def test_c20_r5():
    # [R5/fronteira]
    with pytest.raises(InvalidChecksum):
        validate('00000000001')


def test_c21_r6():
    # [R6/normal]
    assert validate('529.982.247-25') == '52998224725'


def test_c22_r6():
    # [R6/normal]
    assert validate('52998224725') == '52998224725'


def test_c23_r6():
    # [R6/normal]
    assert validate('123.456.789-09') == '12345678909'


def test_c24_r6():
    # [R6/fronteira]
    assert validate('00000000191') == '00000000191'


def test_c25_r6():
    # [R6/normal]
    assert validate('736.625.851-20') == '73662585120'


def test_c26_r7():
    # [R7/normal]
    assert validate('111.111.111-11') == '11111111111'


def test_c27_r7():
    # [R7/normal]
    assert validate('22222222222') == '22222222222'
```
