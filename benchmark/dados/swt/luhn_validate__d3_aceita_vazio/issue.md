# validate('') accepts an empty string

An empty value should be rejected with `InvalidFormat`, but it is accepted:

```python
>>> from alvo import validate
>>> validate('')
''
```

Expected: `InvalidFormat` is raised.
