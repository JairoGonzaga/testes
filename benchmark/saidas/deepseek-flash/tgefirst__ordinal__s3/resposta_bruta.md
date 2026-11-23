```python
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (101, "101st"),
        (111, "111th"),
    ],
)
def test_ordinal_sufixos_especiais(value, expected):
    assert ordinal(value) == expected
```