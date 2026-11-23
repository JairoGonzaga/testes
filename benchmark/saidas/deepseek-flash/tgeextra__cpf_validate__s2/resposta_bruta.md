```python
def test_c28_r1_r2():
    # [R1/normal] compact deve remover whitespace nas extremidades via strip
    assert validate('\n\t390.533.447-05\r\n') == '39053344705'

    # [R2/invalida] erro de formato não deve ser confundido com InvalidLength
    with pytest.raises(InvalidFormat) as excinfo:
        validate('12a')
    assert type(excinfo.value) is InvalidFormat

    with pytest.raises(InvalidFormat) as excinfo:
        validate(None)
    assert type(excinfo.value) is InvalidFormat
```