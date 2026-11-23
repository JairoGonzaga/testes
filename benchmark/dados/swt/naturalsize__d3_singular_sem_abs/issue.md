# naturalsize(-1) uses the plural 'Bytes'

`naturalsize(1)` correctly returns `'1 Byte'`, but the negative counterpart uses the plural:

```python
>>> from alvo import naturalsize
>>> naturalsize(-1)
'-1 Bytes'
```

Expected `'-1 Byte'`.
