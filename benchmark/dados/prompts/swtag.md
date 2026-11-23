You are working in a sandbox folder that contains a small Python module, `alvo.py`, and an issue
report about it, `ISSUE.md`.

Your task: write a pytest test file `test_issue.py` (in the same folder) that REPRODUCES the issue:
- the tests must FAIL on the current code (because of the bug described in the issue), and
- the tests must PASS once the issue is fixed.

Rules:
- Import from the module with `from alvo import ...`.
- You may run Python and `python -m pytest` inside the sandbox to check your work.
- Do not fix the bug in `alvo.py` (any change to it is discarded; only `test_issue.py` is evaluated).
