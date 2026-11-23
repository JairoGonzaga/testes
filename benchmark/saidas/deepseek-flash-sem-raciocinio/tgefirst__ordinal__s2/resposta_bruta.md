```python
def test_c1_r1_negativo():
    # [R1/normal] números negativos usam o dígito absoluto
    assert ordinal(-1) == '-1st'
    assert ordinal(-2) == '-2nd'
    assert ordinal(-3) == '-3rd'
```
```