from alvo import validate


def test_valid_luhn_number_with_high_doubled_digits():
    # Standard valid Luhn example from the issue: must not raise.
    assert validate("79927398713") == "79927398713"
