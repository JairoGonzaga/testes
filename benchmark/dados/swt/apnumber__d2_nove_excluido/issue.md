# apnumber(9) returns '9' instead of 'nine'

Single-digit numbers should be spelled out, but 9 is returned as a digit.

```python
>>> from alvo import apnumber
>>> apnumber(9)
'9'
```

Expected `'nine'`.
