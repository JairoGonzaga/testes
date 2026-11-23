# apnumber(None) crashes with TypeError

Values that cannot be converted to int are supposed to be returned unchanged as a string (`str(value)`), but passing `None` raises:

```python
>>> from alvo import apnumber
>>> apnumber(None)
Traceback (most recent call last):
  ...
TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
```

Expected `'None'`, the same way `apnumber('abc')` returns `'abc'`.
