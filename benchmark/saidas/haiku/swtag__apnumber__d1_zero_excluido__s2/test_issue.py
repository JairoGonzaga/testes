from alvo import apnumber


def test_zero_is_spelled_out():
    # The docs say 0 to 9 are returned as words, so 0 must give 'zero'.
    assert apnumber(0) == "zero"


def test_single_digits_one_to_nine_are_spelled_out():
    expected = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
    }
    for value, word in expected.items():
        assert apnumber(value) == word


def test_ten_is_still_returned_as_digit_string():
    # Boundary check: only 0 to 9 are spelled out.
    assert apnumber(10) == "10"
