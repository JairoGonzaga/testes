```python
def test_c27_r8():
    # [R8/normal]
    assert issubclass(InvalidFormat, ValidationError)
    assert issubclass(InvalidChecksum, ValidationError)
    assert issubclass(InvalidLength, InvalidFormat)

    with pytest.raises(ValidationError):
        validate('123')

    assert validate('999.999.999-99') == '99999999999'

    with pytest.raises(InvalidFormat):
        validate('000.000.000-00')
```