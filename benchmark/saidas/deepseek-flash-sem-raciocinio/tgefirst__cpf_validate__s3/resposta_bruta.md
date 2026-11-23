```python
def test_c1_r2():
    # [R2/inválido] formato: letras, zeros, vazio e não-iterável
    for bad in ('abcdefghijk', '000.000.000-00', '', '           ', None, 12345678901):
        with pytest.raises(InvalidFormat):
            validate(bad)
```