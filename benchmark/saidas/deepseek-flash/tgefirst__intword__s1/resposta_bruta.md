```python
def test_c1_r2():
    # [R2/normal]
    assert intword(1000) == "1.0 thousand"
    assert intword(1500) == "1.5 thousand"
    assert intword(1_000_000) == "1.0 million"
    assert intword(-1500) == "-1.5 thousand"
```