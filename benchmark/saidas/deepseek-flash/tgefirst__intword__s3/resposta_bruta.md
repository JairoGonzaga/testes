```python
def test_intword_formats_units_and_rounding():
    assert intword(999) == "999"
    assert intword(1000) == "1.0 thousand"
    assert intword(999_999) == "1.0 million"
    assert intword(1_500_000) == "1.5 million"
    assert intword(-2_000_000) == "-2.0 million"
```