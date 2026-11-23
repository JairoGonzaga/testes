## Analysis

The issue: `intword(1000)` returns `'1000'`, expected `'1.0 thousand'`.

Tracing the code: `powers[0] == 1000`. The guard `if value <= powers[0]: return f"{negative_prefix}{value}"` catches 1000 and returns it unchanged. The issue implies the boundary should be `<` not `<=`, so 1000 falls through to the humanization path.

After the fix, `1000` → `ordinal = bisect_right(powers, 1000) = 1`; `ordinal -= 1 = 0`; `power = 1000`; `chopped = 1.0`; `format % 1.0 = "1.0"`; `unit = "thousand"` → `"1.0 thousand"`. Matches expected.

I'll also include `999` (still plain, per the boundary) — the issue only mandates 1000's behavior, but 999 remaining `'999'` is consistent with the trace and the intended guard. To keep the test minimal and safe, I focus on the values the issue states.

```python
from alvo import intword


def test_intword_1000_is_thousand():
    assert intword(1000) == "1.0 thousand"


def test_intword_negative_1000_is_thousand():
    assert intword(-1000) == "-1.0 thousand"
```

---- revisão ----

Notes: The negative case is not stated by the issue; drop it. Keep only the stated `intword(1000) == '1.0 thousand'`.

```python
from alvo import intword


def test_intword_1000_is_thousand():
    assert intword(1000) == "1.0 thousand"
```