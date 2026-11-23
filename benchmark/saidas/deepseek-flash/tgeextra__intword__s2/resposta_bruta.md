```python
def test_c34_r3_r5_negative_and_format_rollover():
    # Rollover to the next unit combined with negative values and custom formatting.
    assert intword(-999999) == '-1.0 million'
    assert intword(999999, '%.0f') == '1 million'
    assert intword(-999999, '%.0f') == '-1 million'
```