# ordinal() returns an empty string for non-numeric input

Values that cannot be converted to int should be returned as `str(value)`, but an empty string comes back:

```python
>>> from alvo import ordinal
>>> ordinal('something else')
''
```

Expected `'something else'`.
