```python
def test_bug_rounding_boundary_binary():
    # [R8/fronteira] O arredondamento de 1024**2 - 1 para "1.0 KiB" via format deve
    # promover para MiB em binário também (mesma lógica do teste c43 para decimal).
    # Com format="%.0f", 1023.999... arredonda para 1024, exigindo exp += 1.
    assert naturalsize(1024**2 - 1, binary=True, format="%.0f") == "1 MiB"
```