```python
def test_c28_r8():
    # [R8/fronteira] compact remove separadores; strip remove whitespace nas pontas
    assert validate('\t390.533.447-05\n') == '39053344705'
    with pytest.raises(InvalidFormat):
        validate('390\t533.447-05')
```