```python
def test_validate_valid_and_invalid_checksum():
    assert validate("18") == "18"

    with pytest.raises(InvalidChecksum):
        validate("19")
```