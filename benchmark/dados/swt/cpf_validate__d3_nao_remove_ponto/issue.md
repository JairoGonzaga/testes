# Formatted CPF with dots is rejected

`validate()` is documented to accept CPFs in the usual `XXX.XXX.XXX-XX` format (spaces, dots and hyphens are removed before validating), but a correctly formatted valid CPF fails:

```python
>>> from alvo import validate
>>> validate('111.444.777-35')
Traceback (most recent call last):
  ...
alvo.InvalidFormat
```

Expected: returns the compact form `'11144477735'`.
