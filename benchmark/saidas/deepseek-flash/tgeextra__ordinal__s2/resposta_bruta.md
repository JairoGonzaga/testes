```python
@pytest.mark.parametrize(
    "value, expected",
    [
        ("3.9", "3.9"),
        ("1e2", "1e2"),
        ("nan", "NaN"),
        ("inf", "+Inf"),
        ("-inf", "-Inf"),
        ("1e309", "+Inf"),
    ],
)
def test_c37_r3_r6_strings_finitas_nao_inteiras_e_nao_finitas(value, expected):
    # [R3/R6/fronteira] strings que passam por float(), mas não por int(), ou são não finitas
    assert ordinal(value) == expected
```