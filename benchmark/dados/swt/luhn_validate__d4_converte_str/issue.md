# validate() returns a string when given an int

`validate()` should return the value it received, unchanged, when it is valid. When an int is passed, a str comes back:

```python
>>> from alvo import validate
>>> validate(79927398713)
'79927398713'
```

Expected the int `79927398713`.
