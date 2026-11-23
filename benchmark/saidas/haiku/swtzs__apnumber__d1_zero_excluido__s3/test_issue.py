from alvo import apnumber


def test_apnumber_zero_is_spelled_out():
    assert apnumber(0) == "zero"


def test_apnumber_one_to_nine_are_spelled_out():
    words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    for digit, word in enumerate(words, start=1):
        assert apnumber(digit) == word
