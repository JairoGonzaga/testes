```python
def test_c34_r3_r4_r5():
    # [R3+R4/fronteira] arredondamento para a próxima ordem em valor negativo
    assert intword(-999999) == '-1.0 million'
    # [R3+R5/fronteira] arredondamento aplica o formato customizado após a troca de unidade
    assert intword(999999, format='%.0f') == '1 million'
    assert intword(-999999, format='%.0f') == '-1 million'
```