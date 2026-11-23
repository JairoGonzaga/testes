# intword drops the minus sign of negative numbers

Negative values lose their sign:

```python
>>> from alvo import intword
>>> intword(-1000000)
'1.0 million'
```

Expected `'-1.0 million'`.
