# intword(10**100) does not return '1.0 googol'

A googol should be humanized as `'1.0 googol'`, but we get a huge number with the previous suffix:

```python
>>> from alvo import intword
>>> intword(10**100)
'9999999999999999827367757839185598317239782875580932278577147150336.0 decillion'
```

Expected `'1.0 googol'`.
