# CPF with too many digits raises InvalidChecksum instead of InvalidLength

Any CPF whose compacted form does not have exactly 11 digits should raise `InvalidLength`. With 12 digits we get the wrong exception:

```python
>>> from alvo import validate
>>> validate('111444777350')
Traceback (most recent call last):
  ...
alvo.InvalidChecksum
```

Expected: `InvalidLength`.
