```python
def test_c28_invalid_checksum_message():
    # [R4/invalida] verifica que InvalidChecksum é subclasse de ValidationError
    # e que a mensagem/tipo levantado é específico do dígito verificador.
    assert issubclass(InvalidChecksum, ValidationError)
    assert issubclass(InvalidLength, InvalidFormat)
    with pytest.raises(InvalidChecksum) as exc_info:
        validate('529.982.247-26')
    assert not isinstance(exc_info.value, InvalidFormat)
```