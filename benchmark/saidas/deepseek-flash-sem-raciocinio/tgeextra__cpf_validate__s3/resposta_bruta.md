```python
def test_c28_import_side_effect():
    # [R2/fronteira] - valida caracteres de limpeza e checagem de dígitos do módulo
    import alvo

    assert alvo.compact(' 390.533.447-05 ') == '39053344705'
    assert alvo.clean('390-533', '-') == '390533'
    assert alvo.isdigits('39053344705') is True
    assert alvo.isdigits('3905334470a') is False
```