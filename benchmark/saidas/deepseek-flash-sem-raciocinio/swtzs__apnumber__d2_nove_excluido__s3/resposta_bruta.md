```python
from alvo import apnumber


def test_apnumber_nine():
    assert apnumber(9) == "nine"


def test_apnumber_single_digits_spelled_out():
    expected = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]
    for value, word in enumerate(expected):
        assert apnumber(value) == word, f"apnumber({value}) != {word}"
```