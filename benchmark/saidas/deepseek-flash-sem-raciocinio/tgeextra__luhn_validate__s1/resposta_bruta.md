```python
def test_c21_r6_checksum():
    # [R6/normal] verifica comportamento de checksum com alfabeto não decimal
    from alvo import checksum
    assert checksum('1a2b1', alphabet='0123456789abcdef') == 0
```
```