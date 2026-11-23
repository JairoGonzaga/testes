```python
def test_c23_r5_non_finite_strings():
    # [R5/invalida] strings conversíveis para valores não finitos
    assert apnumber('inf') == '+Inf'
    assert apnumber('-inf') == '-Inf'
    assert apnumber('nan') == 'NaN'
```