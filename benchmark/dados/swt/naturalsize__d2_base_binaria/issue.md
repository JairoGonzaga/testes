# naturalsize(binary=True) gives wrong values

With `binary=True` the result should use powers of 1024 (KiB, MiB...), but the numbers look like they are computed with powers of 1000:

```python
>>> from alvo import naturalsize
>>> naturalsize(3000000, binary=True)
'3.0 MiB'
```

3000000 / 1024**2 = 2.86..., so expected `'2.9 MiB'`.
