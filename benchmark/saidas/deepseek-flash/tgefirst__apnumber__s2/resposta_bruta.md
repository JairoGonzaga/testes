```python
def test_c1_r2():
    # [R1/intervalo]
    expected = [
        "zero", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine",
    ]
    for value, word in enumerate(expected):
        assert apnumber(value) == word
```