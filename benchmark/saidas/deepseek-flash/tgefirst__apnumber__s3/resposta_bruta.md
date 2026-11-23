```python
def test_apnumber_next_behaviour():
    assert apnumber(1) == "one"
    assert apnumber(9) == "nine"
    assert apnumber(10) == "10"
    assert apnumber(-1) == "-1"
    assert apnumber(3.7) == "three"
    assert apnumber(float("nan")) == "NaN"
    assert apnumber(float("inf")) == "+Inf"
    assert apnumber(float("-inf")) == "-Inf"
    assert apnumber("abc") == "abc"
    assert apnumber(None) == "None"
```