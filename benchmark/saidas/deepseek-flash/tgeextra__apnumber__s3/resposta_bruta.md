```python
def test_c23_r3_r2_fronteira_conversao_para_int():
    # [R3/R2/fronteira] a conversão para int acontece antes da checagem de faixa
    assert apnumber(9.9) == 'nine'
    assert apnumber(10.9) == '10'
    assert apnumber(-0.5) == 'zero'
    assert apnumber(-1.9) == '-1'
```