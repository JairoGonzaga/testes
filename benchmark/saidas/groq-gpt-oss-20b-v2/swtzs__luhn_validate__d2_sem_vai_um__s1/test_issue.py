# test_issue.py
# This test reproduces the reported Luhn validation bug in alvo.validate().
# It should fail with the current implementation (raising InvalidChecksum)
# and pass after the bug is fixed.

from alvo import validate

def test_valid_luhn_number_should_pass():
    """
    The example Luhn number '79927398713' should be accepted and returned.
    With the buggy checksum implementation it raises InvalidChecksum.
    """
    assert validate('79927398713') == '79927398713'
