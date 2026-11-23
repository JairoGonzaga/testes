Analysis:
- Issue promises `validate('11144477735')` returns `'11144477735'` (well-known valid CPF).
- `_calc_check_digits` trace for 11144477735:
  d1 sum: (10*1+9*1+8*1+7*4+6*4+5*4+4*7+3*7+2*7) = 10+9+8+28+24+20+28+21+14 = 162.
  d1 = (11-162) % 11 % 10 = (-151 % 11) % 10. -151 % 11 = 3 (since -151 = -14*11+3). 3 % 10 = 3. Correct first digit is 3? Actually CPF check: remainder*10%11... The formula used here is wrong; correct d1 should be 3 (matches last two chars '35' first digit 3).
- d2 = (11*1+10*1+9*1+8*4+7*4+6*4+5*7+4*7+3*7) + d1 = 11+10+9+32+28+24+35+28+21 +3 = 201.
  d2 = (11-201) % 11 % 10 = (-190 % 11) % 10. -190 % 11 = 8 (since -190 = -18*11+8). 8 % 10 = 8. So computed "38", expected "35" → InvalidChecksum raised. Confirms bug.
- Bug is the `(11 - d) % 11 % 10` formula (should be `(d * 10) % 11` style). Tests should assert the valid CPF returns itself.
- Do not assert other CPFs' expected values beyond what issue states.

```python
import pytest

from alvo import validate, InvalidChecksum


def test_valid_cpf_11144477735():
    assert validate('11144477735') == '11144477735'


def test_valid_cpf_formatted():
    assert validate('111.444.777-35') == '11144477735'
```

---- revisão ----

Notes: `test_valid_cpf_formatted` is fine — `compact` strips `.`/`-` and the issue's valid CPF is the same number, expected value traced to `'11144477735'`; both tests fail only due to the checksum bug. Keep both.

```python
import pytest

from alvo import validate


def test_valid_cpf_11144477735():
    assert validate('11144477735') == '11144477735'


def test_valid_cpf_formatted():
    assert validate('111.444.777-35') == '11144477735'
```