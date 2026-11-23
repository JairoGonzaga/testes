```python
def test_c21_checksum_exact_remainders():
    from alvo import checksum

    assert checksum("79927398713") == 0
    assert checksum("79927398710") == 7
    assert checksum("1a2b1", alphabet="0123456789abcdef") == 0
    assert checksum("1a2b0", alphabet="0123456789abcdef") == 15
```