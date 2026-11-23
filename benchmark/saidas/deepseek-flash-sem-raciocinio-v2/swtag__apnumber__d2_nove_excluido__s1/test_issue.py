from alvo import apnumber


def test_nine_is_spelled_out():
    assert apnumber(9) == "nine"


def test_all_single_digits_are_spelled_out():
    expected = [
        "zero", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine",
    ]
    assert [apnumber(i) for i in range(10)] == expected


def test_ten_is_not_spelled_out():
    assert apnumber(10) == "10"
