# validate() accepts the all-zeros CPF

A CPF made only of zeros is not a valid number and should be rejected with `InvalidFormat`, but it is accepted:

```python
>>> from alvo import validate
>>> validate('00000000000')
'00000000000'
```

Expected: `InvalidFormat` is raised.
