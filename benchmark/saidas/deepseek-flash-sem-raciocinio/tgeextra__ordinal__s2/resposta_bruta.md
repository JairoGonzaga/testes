```python
def test_c37_r3_float_string_truncation():
    # [R3/invalida] a string numérica float é convertida para float antes do int
    assert ordinal('3.9') == '3rd'
```