# naturalsize(1000) returns '1000 Bytes'

Exactly one kilobyte is not converted to the next unit:

```python
>>> from alvo import naturalsize
>>> naturalsize(1000)
'1000 Bytes'
```

Expected `'1.0 kB'`.
