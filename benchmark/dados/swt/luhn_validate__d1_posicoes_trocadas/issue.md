# Valid Luhn number rejected

The textbook Luhn example number is rejected:

```python
>>> from alvo import validate
>>> validate('79927398713')
Traceback (most recent call last):
  ...
alvo.InvalidChecksum
```

`79927398713` has a valid Luhn check digit. Expected: returns `'79927398713'`.
