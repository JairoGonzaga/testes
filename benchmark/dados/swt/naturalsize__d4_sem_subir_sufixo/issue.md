# naturalsize(999999) returns '1000.0 kB'

When formatting rounds a value up to the size of the next unit, the unit is not promoted:

```python
>>> from alvo import naturalsize
>>> naturalsize(999999)
'1000.0 kB'
```

Expected `'1.0 MB'`.
