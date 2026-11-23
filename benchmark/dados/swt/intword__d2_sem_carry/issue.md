# intword(999999) returns '1000.0 thousand'

When rounding pushes a value up to the next power, the suffix is not promoted:

```python
>>> from alvo import intword
>>> intword(999999)
'1000.0 thousand'
```

Expected `'1.0 million'`.
