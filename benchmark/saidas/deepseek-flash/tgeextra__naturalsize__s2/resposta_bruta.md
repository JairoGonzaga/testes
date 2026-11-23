```python
def test_c45_r10():
    # [R10/normal]
    for exp, suffix in enumerate("KMGTPEZYRQ", start=1):
        assert naturalsize(1024**exp, gnu=True) == f"1.0{suffix}"
```