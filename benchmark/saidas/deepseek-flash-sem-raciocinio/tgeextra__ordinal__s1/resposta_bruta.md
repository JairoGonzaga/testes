```python
def test_c37_r3_fronteira_negativa():
    # [R3/fronteira] negativos: -11, -12, -13 não usam sufixo st/nd/rd
    assert ordinal(-11) == '-11th'
    assert ordinal(-21) == '-21st'
    assert ordinal(-103) == '-103rd'
```