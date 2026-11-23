Analysis:
- The issue promises `intword(999999) == '1.0 million'` (suffix promoted when rounding reaches the next power).
- Current code: `chopped = 999999/1000 = 999.999`, `format %` gives `'1000.0'` → float 1000.0.
- The guard `rounded_value == powers[ordinal + 1]` compares 1000.0 against `powers[1] = 10**6 = 1000000` — wrong comparison, so promotion never happens.
- Expected value '1.0 million' comes directly from the issue text; suffix 'million' is `human_powers[1]`.
- Also `intword(999999999)` should give `'1.0 billion'` by the same stated rule (rounding pushes to next power) — I'll include the directly stated case plus a closely related one derived by the same rule/trace: 999999 → '1.0 million'.

```python
import pytest
from alvo import intword


def test_intword_999999_promotes_to_million():
    assert intword(999999) == "1.0 million"


def test_intword_999999999_promotes_to_billion():
    assert intword(999999999) == "1.0 billion"
```

---- revisão ----

Notes: keep only the exact case stated in the issue (`999999` → `'1.0 million'`); the billion case is my own extrapolation, not stated, so delete it.

```python
from alvo import intword


def test_intword_999999_promotes_to_million():
    assert intword(999999) == "1.0 million"
```