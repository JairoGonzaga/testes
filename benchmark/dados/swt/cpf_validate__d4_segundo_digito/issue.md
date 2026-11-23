# Valid CPF rejected with InvalidChecksum

Some perfectly valid CPF numbers are rejected as having a wrong check digit:

```python
>>> from alvo import validate
>>> validate('11144477735')
Traceback (most recent call last):
  ...
alvo.InvalidChecksum
```

`111.444.777-35` is a well-known valid CPF (both check digits are correct). Expected: returns `'11144477735'`.
