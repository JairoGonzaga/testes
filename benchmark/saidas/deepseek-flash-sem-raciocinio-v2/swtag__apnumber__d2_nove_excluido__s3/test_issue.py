from alvo import apnumber


def test_apnumber_nine():
    assert apnumber(9) == "nine"


def test_apnumber_single_digits():
    words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    for i, word in enumerate(words):
        assert apnumber(i) == word


def test_apnumber_ten_still_digit():
    assert apnumber(10) == "10"
