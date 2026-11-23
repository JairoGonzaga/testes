from alvo import apnumber


def test_apnumber_zero_is_spelled_out():
    # Issue: apnumber(0) returns '0' instead of 'zero'.
    assert apnumber(0) == "zero"


def test_apnumber_digits_zero_to_nine_are_spelled_out():
    expected = [
        "zero", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine",
    ]
    assert [apnumber(n) for n in range(10)] == expected
