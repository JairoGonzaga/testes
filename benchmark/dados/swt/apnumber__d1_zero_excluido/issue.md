# apnumber(0) is not spelled out

The docs say numbers from 0 to 9 are returned as words, but zero comes back as a digit string.

```python
>>> from alvo import apnumber
>>> apnumber(0)
'0'
```

Expected `'zero'`. Other single digits (e.g. `apnumber(5)` -> `'five'`) work fine.
