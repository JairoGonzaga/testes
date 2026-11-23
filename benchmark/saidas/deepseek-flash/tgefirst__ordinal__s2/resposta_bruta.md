```python
def test_c1_r2():
    assert ordinal(2) == "2nd"
    assert ordinal(3) == "3rd"
    assert ordinal(4) == "4th"
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"
    assert ordinal(21) == "21st"
    assert ordinal(22) == "22nd"
    assert ordinal(23) == "23rd"
    assert ordinal(100) == "100th"
    assert ordinal(101) == "101st"
    assert ordinal(111) == "111th"
    assert ordinal(112) == "112th"
    assert ordinal(113) == "113th"
```