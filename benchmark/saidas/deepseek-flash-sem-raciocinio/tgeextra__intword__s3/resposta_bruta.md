```python
def test_c34_r2_fronteira_arredondamento_limite():
    # [R2/fronteira] valor abaixo do limiar que, ao arredondar, sobe de unidade
    assert intword(999949) == '999.9 thousand'
    assert intword(999950) == '1.0 million'
```