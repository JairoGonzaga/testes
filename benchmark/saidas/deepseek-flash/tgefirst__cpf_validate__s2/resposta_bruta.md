```python
def test_c1_r2():
    # [R1/exceções]
    with pytest.raises(InvalidFormat):
        validate('abc')

    with pytest.raises(InvalidLength):
        validate('1234567890')

    with pytest.raises(InvalidChecksum):
        validate('39053344706')

    with pytest.raises(InvalidFormat):
        validate('00000000000')
```