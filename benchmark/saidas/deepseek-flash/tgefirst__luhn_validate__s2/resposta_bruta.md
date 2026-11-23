```python
def test_validate_invalid_character_raises_invalid_format():
    # [R2/formato]
    with pytest.raises(InvalidFormat):
        validate("7992739871x")
```