```python
def test_c23_r5_nan_string():
    # [R5/invalida] strings especiais são convertidas para float antes da checagem
    assert apnumber('nan') == 'NaN'
```