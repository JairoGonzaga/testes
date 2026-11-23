```python
def test_c23_r5_string_not_finite_and_negative_truncation():
    assert apnumber('nan') == 'NaN'
    assert apnumber('inf') == '+Inf'
    assert apnumber('-inf') == '-Inf'
    assert apnumber(-0.1) == 'zero'
    assert apnumber(-1.9) == '-1'
    assert apnumber(True) == 'one'
    assert apnumber(False) == 'zero'
```