# Section 2 — Python Study Guide 🔴
> **Required qualification** — Expect at least one coding question on the exam.

---

## Table of Contents
1. [pandas Basics](#1-pandas-basics)
2. [Writing Clean Functions](#2-writing-clean-functions)
3. [REST APIs & File I/O](#3-rest-apis--file-io)
4. [Quick-Reference Cheat Sheet](#4-quick-reference-cheat-sheet)

---

## 1. pandas Basics

### DataFrames

A `DataFrame` is a 2D table with labeled rows and columns. It's the core data structure in pandas.

```python
import pandas as pd

# Create from a list of dicts
df = pd.DataFrame([
    {"name": "Alice", "score": 92},
    {"name": "Bob",   "score": 85},
])

# Read from a CSV
df = pd.read_csv("data.csv")

# Quick inspection
df.head()          # first 5 rows
df.shape           # (rows, columns)
df.dtypes          # column data types
df.info()          # summary + nulls
df.describe()      # stats for numeric cols
```

---

### `groupby`

Use `groupby` to split data into groups and apply an aggregation.

```python
# Total sales per region
df.groupby("region")["sales"].sum()

# Multiple aggregations at once
df.groupby("region").agg(
    total_sales=("sales", "sum"),
    avg_sales=("sales", "mean"),
    num_orders=("order_id", "count"),
)

# Group by multiple columns
df.groupby(["region", "product"])["sales"].sum()
```

> **Key point:** `groupby` returns a `GroupBy` object — chain `.sum()`, `.mean()`, `.count()`, or `.agg()` to get a result.

---

### `merge`

`merge` is pandas' equivalent of a SQL JOIN.

```python
customers = pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]})
orders    = pd.DataFrame({"customer_id": [1, 1, 2], "amount": [50, 30, 90]})

# Inner join (only matching rows)
pd.merge(orders, customers, left_on="customer_id", right_on="id")

# Left join (keep all rows from left)
pd.merge(orders, customers, left_on="customer_id", right_on="id", how="left")
```

| `how=`   | Keeps                          |
|----------|-------------------------------|
| `inner`  | Only matching rows (default)  |
| `left`   | All rows from left DataFrame  |
| `right`  | All rows from right DataFrame |
| `outer`  | All rows from both            |

---

### `apply`

Apply a custom function to every row or column.

```python
# Apply to a single column (element-wise)
df["score_letter"] = df["score"].apply(lambda x: "A" if x >= 90 else "B")

# Apply a function row-wise (axis=1)
def full_label(row):
    return f"{row['name']} — {row['score']}"

df["label"] = df.apply(full_label, axis=1)
```

> **Tip:** Prefer vectorised operations (e.g. `df["col"] * 2`) over `apply` when possible — they're much faster on large datasets.

---

### Handling Nulls

```python
df.isnull().sum()           # count nulls per column
df.dropna()                 # drop rows with ANY null
df.dropna(subset=["email"]) # drop only if "email" is null
df.fillna(0)                # replace nulls with 0
df["age"].fillna(df["age"].mean(), inplace=True)  # fill with column mean
```

---

### Handling Duplicates

```python
df.duplicated().sum()              # count duplicate rows
df.drop_duplicates()               # remove exact duplicates
df.drop_duplicates(subset=["id"])  # deduplicate on a specific column
df.drop_duplicates(subset=["id"], keep="last")  # keep the last occurrence
```

---

## 2. Writing Clean Functions

### List Comprehensions

A concise way to build lists (and dicts/sets) without explicit `for` loops.

```python
# Basic comprehension
squares = [x**2 for x in range(10)]

# With a filter
evens = [x for x in range(20) if x % 2 == 0]

# Nested comprehension
pairs = [(x, y) for x in range(3) for y in range(3)]

# Dict comprehension
word_lengths = {word: len(word) for word in ["apple", "banana", "kiwi"]}
```

> **Rule of thumb:** If a comprehension needs more than one condition or a nested `if/else`, use a regular `for` loop for readability.

---

### Error Handling

```python
def divide(a: float, b: float) -> float:
    """Return a / b, raising ValueError if b is zero."""
    if b == 0:
        raise ValueError("Denominator cannot be zero.")
    return a / b

# Catching specific exceptions
try:
    result = divide(10, 0)
except ValueError as e:
    print(f"Input error: {e}")
except TypeError as e:
    print(f"Type error: {e}")
finally:
    print("Always runs — good for cleanup.")
```

**Best practices:**
- Catch **specific** exceptions, not bare `except:`.
- Raise exceptions with clear, actionable messages.
- Use `finally` for cleanup (closing files, DB connections).
- Create custom exception classes for domain-specific errors.

---

### Type Hints

Type hints make code self-documenting and catch bugs early with tools like `mypy`.

```python
from typing import Optional

def get_user(user_id: int) -> Optional[dict]:
    """Return a user dict, or None if not found."""
    ...

def process_scores(scores: list[float]) -> dict[str, float]:
    return {
        "mean":  sum(scores) / len(scores),
        "min":   min(scores),
        "max":   max(scores),
    }
```

| Hint              | Meaning                                  |
|-------------------|------------------------------------------|
| `int`, `str`, `float` | Primitive types                      |
| `list[int]`       | List of integers                         |
| `dict[str, int]`  | Dict with string keys, int values        |
| `Optional[str]`   | Either `str` or `None`                   |
| `tuple[int, str]` | Tuple with specific types per position   |

---

### Readable Code Checklist

- ✅ Functions do **one thing** — if it needs an "and" in the docstring, split it.
- ✅ Descriptive names: `calculate_monthly_revenue()` not `calc()`.
- ✅ Keep functions short: aim for under ~20 lines.
- ✅ Write a one-line docstring for every public function.
- ✅ Avoid magic numbers — use named constants (`MAX_RETRIES = 3`).
- ✅ Prefer `return early` to deep nesting.

```python
# ❌ Hard to follow
def process(d):
    if d:
        if "id" in d:
            return d["id"] * 2

# ✅ Clear and readable
def double_id(record: dict) -> Optional[int]:
    """Return twice the record's ID, or None if missing."""
    if not record or "id" not in record:
        return None
    return record["id"] * 2
```

---

## 3. REST APIs & File I/O

### `requests` Library

```python
import requests

# GET request
response = requests.get(
    "https://api.example.com/users",
    params={"page": 1, "limit": 50},
    headers={"Authorization": "Bearer MY_TOKEN"},
    timeout=10,  # always set a timeout!
)

response.raise_for_status()  # raises HTTPError for 4xx/5xx

data = response.json()       # parse JSON body
print(response.status_code)  # 200, 404, 500, etc.

# POST request
new_user = {"name": "Alice", "email": "alice@example.com"}
response = requests.post(
    "https://api.example.com/users",
    json=new_user,            # sets Content-Type: application/json automatically
    headers={"Authorization": "Bearer MY_TOKEN"},
)
```

---

### Reading & Writing CSVs

```python
import csv

# --- Read ---
with open("data.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)          # list of dicts, keys from header row

# With pandas (preferred for analysis)
df = pd.read_csv("data.csv")

# --- Write ---
fieldnames = ["name", "score"]
with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows([{"name": "Alice", "score": 92}])

# With pandas
df.to_csv("output.csv", index=False)
```

---

### Parsing JSON Responses

```python
import json

# From a requests response
response = requests.get("https://api.example.com/data", timeout=10)
response.raise_for_status()
payload = response.json()           # dict or list

# Navigating nested JSON
users = payload["results"]
first_name = payload["user"]["profile"]["first_name"]

# Safely access uncertain keys
email = payload.get("user", {}).get("email", "N/A")

# From a JSON file
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Write to a JSON file
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)
```

---

### Putting It Together — End-to-End Example

```python
import requests
import pandas as pd
from typing import Optional

def fetch_user_scores(api_url: str, token: str) -> Optional[pd.DataFrame]:
    """
    Fetch user scores from a REST API and return as a cleaned DataFrame.
    Returns None if the request fails.
    """
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"API error: {e}")
        return None

    records = response.json().get("users", [])
    df = pd.DataFrame(records)

    # Clean up
    df.drop_duplicates(subset=["user_id"], inplace=True)
    df.dropna(subset=["score"], inplace=True)
    df["score"] = df["score"].astype(float)

    return df


def summarise_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Return mean and count of scores grouped by region."""
    return df.groupby("region").agg(
        avg_score=("score", "mean"),
        user_count=("user_id", "count"),
    ).reset_index()
```

---

## 4. Quick-Reference Cheat Sheet

### pandas

| Task                       | Code                                        |
|----------------------------|---------------------------------------------|
| Load CSV                   | `pd.read_csv("file.csv")`                   |
| Inspect shape              | `df.shape`                                  |
| Group & aggregate          | `df.groupby("col").agg(...)`                |
| Join two DataFrames        | `pd.merge(df1, df2, on="key")`              |
| Apply function to column   | `df["col"].apply(func)`                     |
| Count nulls                | `df.isnull().sum()`                         |
| Fill nulls                 | `df.fillna(value)`                          |
| Drop duplicates            | `df.drop_duplicates(subset=["id"])`         |

### Clean Functions

| Principle        | Summary                                           |
|------------------|---------------------------------------------------|
| Type hints       | `def f(x: int) -> str:`                          |
| Error handling   | Catch specific exceptions; raise with messages    |
| Comprehensions   | Use for simple transforms; loops for complexity   |
| Readability      | One function, one job; descriptive names          |

### REST & File I/O

| Task                    | Code                                             |
|-------------------------|--------------------------------------------------|
| GET request             | `requests.get(url, params=..., timeout=10)`      |
| POST request            | `requests.post(url, json=payload)`               |
| Check for HTTP errors   | `response.raise_for_status()`                    |
| Parse JSON response     | `response.json()`                                |
| Read CSV (stdlib)       | `csv.DictReader(f)`                              |
| Read CSV (pandas)       | `pd.read_csv("file.csv")`                        |
| Load JSON file          | `json.load(f)`                                   |
| Safe key access         | `data.get("key", default)`                       |

---

*Good luck — you've got this! 🐍*
