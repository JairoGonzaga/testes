

@pytest.mark.parametrize(
    "value,expected",
    [
        (1, "one"),
        (5, "five"),
        (9, "nine"),
        (10, "10"),
        (11, "11"),
        (-1, "-1"),
        (9.7, "nine"),
        (3.0, "three"),
        ("7", "seven"),
        ("abc", "abc"),
        (None, "None"),
        (True, "one"),
        (float("nan"), "NaN"),
        (float("inf"), "+Inf"),
        (float("-inf"), "-Inf"),
        ("nan", "NaN"),
    ],
)
def test_c1_r2_conversoes(value, expected):
    # [R2/conversão de tipos e não finitos]
    assert apnumber(value) == expected
