Analysis:
- The issue states `intword(-1000000)` must return `'-1.0 million'`; the source shows `negative_prefix` is set to `""` in both the negative and non-negative branch, so the sign is dropped.
- Expected value comes directly from the issue text: `'-1.0 million'`.
- Also stated: example `intword(-1000000)` currently returns `'1.0 million'`. I assert the promised negative behaviour.
- I add only closely related negative case consistent with the same promise: `intword(-2000)` → `'-2.0 thousand'` (format defaults to `"%.1f"`, power thousand, value 2.0).
- Keep small: two negative cases, checking the minus sign is preserved.

```python
from alvo import intword


def test_intword_negative_million_keeps_sign():
    assert intword(-1000000) == "-1.0 million"


def test_intword_negative_thousand_keeps_sign():
    assert intword(-2000) == "-2.0 thousand"
```

---- revisão ----

The first assertion is stated verbatim in the issue (`'-1.0 million'`); the second was not given in the issue, so per the rules I delete it to keep the test minimal.

```python
from alvo import intword


def test_intword_negative_million_keeps_sign():
    assert intword(-1000000) == "-1.0 million"
```