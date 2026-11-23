# Luhn validation fails for numbers with digits >= 5 in doubled positions

Valid numbers are rejected when some of the doubled digits are 5 or more:

```python
>>> from alvo import validate
>>> validate('79927398713')
Traceback (most recent call last):
  ...
alvo.InvalidChecksum
```

`79927398713` is the standard valid Luhn example. Expected: returns `'79927398713'`.
