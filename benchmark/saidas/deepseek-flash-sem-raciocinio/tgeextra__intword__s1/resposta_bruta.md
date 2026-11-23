```python
def test_c34_r2_fronteira_decimal_abaixo():
    # [R2/fronteira] valor não inteiro logo abaixo de mil usa truncamento
    assert intword(999.9) == '999'
```