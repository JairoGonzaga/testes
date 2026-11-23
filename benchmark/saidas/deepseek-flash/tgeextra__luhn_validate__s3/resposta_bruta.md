```python
def test_c21_r2_alphabet_invalido():
    # [R2/invalida] um alfabeto de tipo inválido também deve gerar InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('12', alphabet=None)
```