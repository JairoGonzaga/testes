Analysis:
- The issue states `intword(-1000000)` must return `'-1.0 million'`.
- In the source, the `value < 0` branch sets `negative_prefix = ""` (a bug); the fix is to make it `"-"`.
- For negative values the magnitude is formatted exactly as the positive case is (`1.0 million`), so the expected string is just `"-" + intword(positive)`.
- I'll test the issue's exact example, plus a couple of closely related negative cases whose expected values follow the same stated rule (prefix `-` on the positive formatting).
- Positive behaviour must stay unchanged: `intword(1000000) == '1.0 million'`.
- Values below powers[0] for negatives return `"-<value>"`; e.g. `intword(-12)` -> `'-12'` (positive path returns `'12'`).

```python
from alvo import intword


def test_intword_negative_million():
    assert intword(-1000000) == "-1.0 million"


def test_intword_positive_million_unchanged():
    assert intword(1000000) == "1.0 million"


def test_intword_negative_below_thousand():
    assert intword(-12) == "-12"


def test_intword_negative_billion():
    assert intword(-2000000000) == "-2.0 billion"
```

---- revisão ----

Notes: The billion case (my own example) is not stated and its rounding isn't verifiable from the text, so I drop it; the other assertions trace directly from the code/issue.

```python
from alvo import intword


def test_intword_negative_million():
    assert intword(-1000000) == "-1.0 million"


def test_intword_positive_million_unchanged():
    assert intword(1000000) == "1.0 million"


def test_intword_negative_below_thousand():
    assert intword(-12) == "-12"
```