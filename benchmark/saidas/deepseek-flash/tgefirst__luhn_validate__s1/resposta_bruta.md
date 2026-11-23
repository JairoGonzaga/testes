```python
def test_checksum_invalido():
    # [R1/erro]
    with pytest.raises(InvalidChecksum):
        validate('1')
```