```python
def test_compact_percent_sign_not_removed():
    # '=' is in deletechars but '%' is not; validate should reject wrongly
    # validated numbers that still contain a '%' sign after compaction.
    with pytest.raises(InvalidFormat):
        validate('390.533.447-0%')
```