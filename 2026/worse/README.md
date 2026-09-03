# 7 Python features that can make your code worse

Run each example independently with Python 3.14 or newer:

```bash
uv run 01_property_hides_expensive_work.py
```

Only the caching example has an external dependency:

```bash
uv sync
```

Each file contrasts a tempting implementation with a more explicit design. The
features are useful; the examples show the cost of using them where they hide
important behaviour or constrain future changes.
