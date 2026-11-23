```python
def test_c27_r7():
    # [R7/invalida]
    with pytest.raises(ValidationError):
        validate('222.222.222-21')
```