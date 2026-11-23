# intword(1000) is not humanized

Numbers of one thousand or more should be written with a word suffix, but exactly 1000 comes back unchanged:

```python
>>> from alvo import intword
>>> intword(1000)
'1000'
```

Expected `'1.0 thousand'`.
