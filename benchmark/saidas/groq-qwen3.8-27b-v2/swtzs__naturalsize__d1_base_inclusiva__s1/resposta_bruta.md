Analysis
- Promised behaviour (from the issue): `naturalsize(1000)` must return `'1.0 kB'` (decimal, 1000-based), not `'1000 Bytes'`.
- Where the bug is: in `alvo.py`, `if abs_bytes <= base:` returns the raw byte string for any value up to and including the base (1000 decimal / 1024 binary), so exactly one unit is never promoted.
- Expected values come from the issue text: `'1.0 kB'` for 1000. I add the directly analogous binary case (1024 → `'1.0 KiB'`), traced through the same code path.
- I keep the tests to the issue's input plus its binary twin, so they fail now on the `<=` bug and pass once it's promoted to the next unit.

```python
from alvo import naturalsize


def test_naturalsize_decimal_kilobyte():
    # Issue: 1000 (exactly one decimal kilobyte) must be converted to the next unit.
    assert naturalsize(1000) == "1.0 kB"


def test_naturalsize_binary_kibibyte():
    # Binary analogue of the same bug: 1024 is exactly one KiB and must be promoted.
    assert naturalsize(1024, binary=True) == "1.0 KiB"
```

---- revisão ----

Let me verify each assertion by tracing the current code.

Assertion 1: `naturalsize(1000) == "1.0 kB"`
- value=1000, binary=False, gnu=False, format="%.1f" → suffix = ("kB", "MB", ...), base = 1000
- bytes_ = 1000.0, abs_bytes = 1000.0
- abs_bytes == 1? No (1000.0 != 1)
- abs_bytes <= base? 1000.0 <= 1000 → True → returns "%d Bytes" % int(1000.0) = "1000 Bytes"
- So current code returns "1000 Bytes", not "1.0 kB". Test FAILS now. ✓
- After fix: 1000/1000^1 = 1.0, format "%.1f" % 1.0 = "1.0", suffix[0] = "kB", space " " → "1.0 kB". ✓ Expected value comes from the issue text.

Assertion 2: `naturalsize(1024, binary=True) == "1.0 KiB"`
- Traced through code: base=1024, abs_bytes=1024.0 <= 1024 → returns "1024 Bytes" (not "1.0 KiB"). Current FAILS.
- But: is this behaviour stated in the task? NO — the issue only mentions `naturalsize(1000) == '1000 Bytes'` and expects `'1.0 kB'`. It never mentions binary. My expected `'1.0 KiB'` comes from my own convention/assumption, not the task text → violates rule 1. Delete it.

Only the issue-stated assertion survives.

Notes: deleted the binary (1024→"1.0 KiB") assertion — that behaviour is not stated in the issue, so its expected value is an assumption, not a task-specified value.

```python
from alvo import naturalsize


def test_naturalsize_decimal_kilobyte():
    # Issue: 1000 (exactly one decimal kilobyte) must be converted to the next unit.
    assert naturalsize(1000) == "1.0 kB"
```