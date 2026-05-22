# SQL Study Guide

## 1. Window Functions

Window functions perform calculations across a set of rows related to the current row — without collapsing them into a single output row like `GROUP BY` does.

**Syntax pattern:**
```sql
function_name() OVER (
  PARTITION BY column
  ORDER BY column
  ROWS/RANGE BETWEEN ...
)
```

---

### `ROW_NUMBER()`

Assigns a unique sequential integer to each row within a partition. No ties — every row gets a distinct number.

```sql
SELECT
  employee_id,
  department,
  salary,
  ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_num
FROM employees;
```

**Use case:** Return only the top-paid employee per department:
```sql
SELECT * FROM (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn
  FROM employees
) t
WHERE rn = 1;
```

---

### `RANK()`

Assigns a rank with gaps for ties. If two rows tie for rank 2, the next rank is 4.

```sql
SELECT
  name,
  score,
  RANK() OVER (ORDER BY score DESC) AS rank
FROM leaderboard;
-- Result: 1, 2, 2, 4, 5 ...
```

---

### `DENSE_RANK()`

Like `RANK()` but without gaps. Ties share a rank, and the next rank is always consecutive.

```sql
SELECT
  name,
  score,
  DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank
FROM leaderboard;
-- Result: 1, 2, 2, 3, 4 ...
```

**Comparison table:**

| Score | `RANK()` | `DENSE_RANK()` | `ROW_NUMBER()` |
|-------|----------|----------------|----------------|
| 100   | 1        | 1              | 1              |
| 95    | 2        | 2              | 2              |
| 95    | 2        | 2              | 3              |
| 90    | 4        | 3              | 4              |

---

### `LAG()`

Accesses a value from a **previous** row in the partition without a self-join.

```sql
SELECT
  order_date,
  revenue,
  LAG(revenue, 1) OVER (ORDER BY order_date) AS prev_revenue,
  revenue - LAG(revenue, 1) OVER (ORDER BY order_date) AS delta
FROM daily_sales;
```

`LAG(col, n, default)` — `n` is how many rows back (default 1), `default` is the fallback when no prior row exists.

---

### `LEAD()`

Accesses a value from a **following** row. Same signature as `LAG()`.

```sql
SELECT
  user_id,
  event_time,
  LEAD(event_time, 1) OVER (PARTITION BY user_id ORDER BY event_time) AS next_event
FROM events;
```

**Use case:** Calculate time between a user's consecutive events.

---

### `PARTITION BY`

Divides rows into groups for the window function to operate on independently. Think of it as `GROUP BY` for window functions — but rows aren't collapsed.

```sql
-- Salary as % of department total
SELECT
  name,
  department,
  salary,
  salary * 1.0 / SUM(salary) OVER (PARTITION BY department) AS pct_of_dept
FROM employees;
```

Omitting `PARTITION BY` treats the entire result set as one partition.

---

### Other useful window functions

| Function | What it does |
|----------|-------------|
| `SUM() OVER (...)` | Running or partitioned total |
| `AVG() OVER (...)` | Running or partitioned average |
| `FIRST_VALUE()` / `LAST_VALUE()` | First or last value in a window frame |
| `NTILE(n)` | Divides rows into `n` equal buckets |
| `PERCENT_RANK()` | Relative rank as a value between 0 and 1 |

---

## 2. Joins & Aggregations

### Join types

#### `INNER JOIN`
Returns only rows with a match in **both** tables.

```sql
SELECT o.order_id, c.name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id;
```

#### `LEFT JOIN`
Returns all rows from the left table, with `NULL` for non-matching right table columns.

```sql
SELECT c.name, o.order_id
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id;
-- Customers with no orders appear with NULL order_id
```

#### `RIGHT JOIN`
Mirror of `LEFT JOIN` — all rows from the right table, `NULL` for unmatched left rows. (Rarely needed; usually rewritten as a `LEFT JOIN` for readability.)

#### `FULL OUTER JOIN`
All rows from both tables. `NULL` fills in wherever there's no match.

#### Anti-join (find unmatched rows)
Two common patterns to find rows in table A with no match in B:

```sql
-- Using LEFT JOIN + IS NULL
SELECT c.name
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.customer_id IS NULL;

-- Using NOT EXISTS (often faster)
SELECT name
FROM customers c
WHERE NOT EXISTS (
  SELECT 1 FROM orders o WHERE o.customer_id = c.id
);
```

---

### `GROUP BY` and `HAVING`

`GROUP BY` collapses rows with the same value(s) into a single row, allowing aggregate functions.

```sql
SELECT department, COUNT(*) AS headcount, AVG(salary) AS avg_salary
FROM employees
GROUP BY department;
```

**`HAVING`** filters on aggregate results (use `WHERE` to filter *before* aggregation, `HAVING` to filter *after*):

```sql
SELECT department, COUNT(*) AS headcount
FROM employees
GROUP BY department
HAVING COUNT(*) > 10;   -- Only departments with more than 10 employees
```

**Common mistake:** Using `WHERE` with an aggregate:
```sql
-- WRONG
WHERE COUNT(*) > 10

-- RIGHT
HAVING COUNT(*) > 10
```

---

### CTEs (`WITH` clauses)

A Common Table Expression defines a named temporary result set, readable once per query. Improves readability and avoids deeply nested subqueries.

```sql
WITH dept_avg AS (
  SELECT department, AVG(salary) AS avg_sal
  FROM employees
  GROUP BY department
),
high_earners AS (
  SELECT e.name, e.department, e.salary
  FROM employees e
  JOIN dept_avg d ON e.department = d.department
  WHERE e.salary > d.avg_sal
)
SELECT * FROM high_earners ORDER BY salary DESC;
```

**Recursive CTEs** (for hierarchical data like org charts or trees):

```sql
WITH RECURSIVE org AS (
  SELECT id, name, manager_id, 1 AS level
  FROM employees
  WHERE manager_id IS NULL          -- anchor: start at the top

  UNION ALL

  SELECT e.id, e.name, e.manager_id, org.level + 1
  FROM employees e
  JOIN org ON e.manager_id = org.id -- recursive step
)
SELECT * FROM org ORDER BY level;
```

---

## 3. Query Optimization

### Reading `EXPLAIN` / `EXPLAIN ANALYZE`

Run `EXPLAIN` before a query to see the execution plan without running it. Use `EXPLAIN ANALYZE` to actually execute and see real timing.

```sql
EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 42;
```

**Key things to look for:**

| Term | What it means |
|------|--------------|
| `Seq Scan` | Full table scan — no index used. Investigate if the table is large. |
| `Index Scan` | An index is being used. Generally good. |
| `Index Only Scan` | Best case — query answered from index alone. |
| `Hash Join` / `Merge Join` | Join strategies. Hash joins are common for large unsorted sets. |
| `Nested Loop` | Fine for small row counts; can be slow if the inner side is large. |
| `rows=` | Estimated row count. Large gaps between estimate and actual rows → stale statistics. |
| `cost=X..Y` | Estimated startup cost .. total cost in arbitrary units. |
| `actual time=` | Real elapsed time (with `ANALYZE`). |

**Red flags:** `Seq Scan` on millions of rows, very wrong row estimates, high cost nodes near the top.

---

### Avoiding `SELECT *`

```sql
-- Bad: fetches every column, defeats index-only scans, breaks if schema changes
SELECT * FROM orders WHERE customer_id = 42;

-- Good: only what you need
SELECT order_id, order_date, total FROM orders WHERE customer_id = 42;
```

Problems with `SELECT *`:
- Transfers unnecessary data over the network
- Prevents index-only scans (need all columns in the index)
- Breaks downstream code when columns are added or reordered
- Harder to understand query intent

---

### Indexing concepts

An index is a data structure (usually a B-tree) that allows the database to find rows quickly without scanning every row.

```sql
-- Single column index
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- Composite (multi-column) index — column order matters
CREATE INDEX idx_orders_cust_date ON orders(customer_id, order_date);

-- Partial index — only index rows matching a condition
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- Covering index — includes all columns a query needs
CREATE INDEX idx_covering ON orders(customer_id) INCLUDE (order_date, total);
```

**Composite index column order:** put the most selective or equality-filtered column first. For `WHERE customer_id = 42 AND order_date > '2024-01-01'`, `(customer_id, order_date)` is better than `(order_date, customer_id)`.

**Indexes slow down writes** (INSERT/UPDATE/DELETE must update the index too). Don't index every column — focus on columns used in `WHERE`, `JOIN ON`, and `ORDER BY`.

---

### Partitioning

Partitioning splits a large table into smaller physical pieces (partitions) while appearing as one logical table. Queries that filter on the partition key only scan relevant partitions ("partition pruning").

```sql
-- Range partitioning by date (PostgreSQL syntax)
CREATE TABLE orders (
  order_id INT,
  order_date DATE,
  total NUMERIC
) PARTITION BY RANGE (order_date);

CREATE TABLE orders_2023 PARTITION OF orders
  FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

CREATE TABLE orders_2024 PARTITION OF orders
  FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

**Types of partitioning:**

| Type | Best for |
|------|----------|
| Range | Dates, IDs with natural ordering |
| List | Known discrete values (country, status) |
| Hash | Even distribution when no natural range |

**Other optimization tips:**
- Use `EXISTS` instead of `IN` with subqueries for large sets
- Avoid functions on indexed columns in `WHERE` clauses: `WHERE YEAR(created_at) = 2024` prevents index use; use `WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'` instead
- Rewrite correlated subqueries as joins when possible
- `LIMIT` early — filter and limit before joining to large tables

---

## 4. Root Cause Analysis on Data

### Diagnosing NULLs

```sql
-- Count NULLs per column
SELECT
  COUNT(*) AS total_rows,
  COUNT(email) AS non_null_email,
  COUNT(*) - COUNT(email) AS null_email_count,
  ROUND(100.0 * (COUNT(*) - COUNT(email)) / COUNT(*), 2) AS null_pct
FROM users;

-- Find rows where any key field is NULL
SELECT *
FROM orders
WHERE customer_id IS NULL
   OR order_date IS NULL
   OR total IS NULL;
```

**Common causes:** upstream ETL not setting defaults, outer joins introducing NULLs, optional fields in source systems, failed lookups leaving foreign keys unresolved.

**Gotcha:** `NULL != NULL` — always use `IS NULL` / `IS NOT NULL`. Aggregates like `COUNT(col)` ignore NULLs; `COUNT(*)` does not.

---

### Diagnosing duplicates

```sql
-- Find duplicate rows on a key
SELECT customer_id, order_id, COUNT(*) AS cnt
FROM orders
GROUP BY customer_id, order_id
HAVING COUNT(*) > 1;

-- See the actual duplicate rows
SELECT *
FROM orders
WHERE (customer_id, order_id) IN (
  SELECT customer_id, order_id
  FROM orders
  GROUP BY customer_id, order_id
  HAVING COUNT(*) > 1
)
ORDER BY customer_id, order_id;

-- Quick check: are row count and distinct count the same?
SELECT
  COUNT(*) AS total,
  COUNT(DISTINCT order_id) AS distinct_orders
FROM orders;
```

**Common causes:** multiple JOIN paths (fanout), repeated ETL loads without deduplication, missing unique constraints at the source, snapshot tables loaded more than once.

**Fix options:** `DISTINCT`, `ROW_NUMBER()` deduplication (keep rn = 1), or adding a unique constraint to prevent future duplicates.

---

### Diagnosing unexpected row counts

```sql
-- Compare expected vs actual after a JOIN
SELECT COUNT(*) FROM orders;               -- baseline

SELECT COUNT(*) FROM orders o
JOIN customers c ON o.customer_id = c.id;  -- does count change?

-- If count increased → many-to-many join causing row multiplication
-- If count decreased → inner join filtering out rows (use LEFT JOIN to diagnose)

-- Check for fanout: does customer have multiple matching rows?
SELECT customer_id, COUNT(*) FROM customers GROUP BY customer_id HAVING COUNT(*) > 1;
```

**Systematic checklist for unexpected counts:**

1. **Check table grain** — what does one row represent? Is that consistent?
2. **Check JOINs** — each join can multiply or filter rows. Test joins one at a time.
3. **Check filters** — are `WHERE` conditions excluding expected rows?
4. **Check date ranges** — off-by-one or timezone issues dropping rows at boundaries?
5. **Check NULLs in JOIN keys** — `NULL = NULL` is false, so NULLs in join columns silently drop rows.
6. **Check partitioning or sharding** — are you querying all partitions?

```sql
-- Useful: row count by date to spot missing days
SELECT DATE(order_date) AS day, COUNT(*) AS cnt
FROM orders
GROUP BY 1
ORDER BY 1;
-- Gaps in dates, sudden spikes, or unexpected zeros are signal
```

---

### General RCA workflow

1. **Establish a baseline** — what is the expected count, sum, or distribution?
2. **Isolate the problem** — narrow by time range, segment, or table until you find where it breaks.
3. **Trace the data lineage** — which upstream tables feed the metric? Check each one.
4. **Form and test hypotheses** — is it NULLs? Duplicates? A bad join? A filter removing rows?
5. **Validate the fix** — after fixing, rerun the baseline check to confirm numbers align.

```sql
-- Template: audit a metric end-to-end
WITH raw AS (SELECT COUNT(*) AS raw_cnt FROM source_table),
after_filter AS (SELECT COUNT(*) AS filtered_cnt FROM source_table WHERE status = 'complete'),
after_join AS (
  SELECT COUNT(*) AS joined_cnt
  FROM source_table s
  JOIN dim_table d ON s.key = d.key
  WHERE s.status = 'complete'
)
SELECT * FROM raw, after_filter, after_join;
-- Each step should tell you where rows are being lost or gained
```
