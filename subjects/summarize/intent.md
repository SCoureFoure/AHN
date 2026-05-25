# Subject: summarize

Write a function `summarize(items: list[dict]) -> dict` in a Python file named `solution.py` that summarizes a list of order items. Each item has at least a `price` field. An item may also have a `qty` field; if `qty` is missing, treat it as 1.

The returned dict must include `count` (the number of items) and `total` (sum of `price * qty` for each item).

Place the file at the root of your working directory. Do not add a `__main__` block. Do not print anything.
