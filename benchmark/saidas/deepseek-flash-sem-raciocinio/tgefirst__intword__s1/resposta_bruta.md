```python
def test_c1_r2_negative_and_invalid_values():
    # [R2/negative + valores inválidos]
    assert intword(-1500) == '-1.5 thousand'
    assert intword(-1000000) == '-1.0 million'
    assert intword("123") == "123"
    assert intword(None) == "None"
    assert intword("abc") == "abc"
```