# Section 4 Study Guide — Snowflake & dbt 🟡

> **Interview tip:** These are listed as *preferred qualifications* — mention your familiarity early, even if it's surface-level. It signals awareness of modern data stack tooling.

---

## ❄️ Snowflake

### 1. Virtual Warehouses — Compute vs. Storage Separation

Snowflake's architecture separates **storage** (S3/GCS/Azure Blob) from **compute** (virtual warehouses). This means:

- You can scale compute up/down independently without moving data.
- Multiple warehouses can query the **same data** simultaneously without contention.
- Warehouses auto-suspend when idle and auto-resume on demand — you only pay for compute while it's running.

**Key concepts:**
- **Warehouse size** (XS → 4XL+) controls parallelism and credits/hour.
- **Multi-cluster warehouses** handle concurrency by spinning up additional clusters.
- **Credits** are the billing unit for compute (not time directly).

**Interview signal:** Be ready to explain *why* this separation matters (cost efficiency, independent scaling, no resource contention).

---

### 2. Stages and Data Loading

A **stage** is a named location for raw files before loading into tables.

| Stage Type | Description |
|---|---|
| **Internal stage** | Snowflake-managed storage (user stage `@~`, table stage, named stage) |
| **External stage** | Points to S3, GCS, or Azure Blob |

**`COPY INTO` — Bulk loading:**
```sql
COPY INTO my_table
FROM @my_stage/data/
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"')
ON_ERROR = 'SKIP_FILE';
```
- Best for large, scheduled batch loads.
- Tracks loaded files to avoid duplicates (load history).

**Snowpipe — Continuous / event-driven loading:**
- Micro-batch loading triggered by cloud event notifications (e.g., S3 `ObjectCreated`).
- Lower latency than scheduled `COPY INTO`, but higher per-file overhead.
- Uses a serverless compute model (billed per file processed).

**Interview signal:** Know when to use each — Snowpipe for near-real-time ingestion, `COPY INTO` for bulk/batch.

---

### 3. Time Travel and Zero-Copy Cloning

**Time Travel** lets you query, restore, or clone data *as it existed at a past point in time*.

```sql
-- Query data as of 1 hour ago
SELECT * FROM orders AT (OFFSET => -3600);

-- Restore a dropped table
UNDROP TABLE orders;

-- Clone from a point in time
CREATE TABLE orders_backup CLONE orders
  AT (TIMESTAMP => '2024-01-15 09:00:00');
```

- Retention period: **0–90 days** (default 1 day on Standard, up to 90 on Enterprise).
- Applies to tables, schemas, and databases.

**Zero-Copy Cloning** creates an instant copy of any object *without duplicating the underlying data*. New writes diverge; existing micro-partitions are shared.

```sql
CREATE DATABASE prod_clone CLONE production;
```

- **Use cases:** Dev/test environments, safe experimentation, pre-deployment snapshots.
- **Cost:** No storage cost for shared partitions; you only pay for new/changed data.

---

### 4. Clustering Keys and Micro-Partitions

**Micro-partitions** are Snowflake's fundamental storage unit (~50–500 MB of uncompressed data). Each stores min/max metadata per column, enabling **partition pruning** — skipping irrelevant partitions at query time.

**Natural clustering** happens automatically as data is inserted (sorted by insertion order).

**Clustering keys** explicitly define the column(s) Snowflake should sort/co-locate data by:

```sql
ALTER TABLE events CLUSTER BY (event_date, region);
```

- Improves query performance on large tables with frequent filters on those columns.
- Snowflake runs **automatic clustering** in the background (incurs credit cost).

**When to use:**
- Tables > ~1TB frequently filtered on date, region, or similar high-cardinality columns.
- Not needed for small tables — natural clustering is usually sufficient.

**Interview signal:** Understand that clustering is a *maintenance feature*, not a primary key. Know the tradeoff: faster queries vs. ongoing credit cost.

---

## 🔧 dbt (data build tool)

### 1. Models, Sources, and Refs

**Models** are `.sql` files containing a `SELECT` statement. dbt compiles them and materializes the result as a table or view.

```sql
-- models/marts/fct_orders.sql
SELECT
    o.order_id,
    o.customer_id,
    s.status_label
FROM {{ ref('stg_orders') }} o
LEFT JOIN {{ ref('dim_status') }} s ON o.status_id = s.id
```

**`ref()`** — Reference another dbt model. dbt resolves the correct schema/database and builds the DAG dependency.

**Sources** — Declare raw/external tables (not built by dbt) so you can reference and test them:

```yaml
# models/staging/_sources.yml
sources:
  - name: raw
    database: raw_db
    schema: public
    tables:
      - name: orders
        loaded_at_field: _loaded_at
        freshness:
          warn_after: {count: 6, period: hour}
```

```sql
-- Reference a source in a model
SELECT * FROM {{ source('raw', 'orders') }}
```

**Interview signal:** Know the difference between `ref()` (dbt-managed models) and `source()` (external/raw tables).

---

### 2. Tests — Schema Tests and Custom Tests

**Schema tests** are defined in `.yml` files alongside models:

```yaml
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: status
        tests:
          - accepted_values:
              values: ['placed', 'shipped', 'delivered', 'cancelled']
      - name: customer_id
        tests:
          - relationships:
              to: ref('dim_customers')
              field: customer_id
```

Built-in generic tests: `unique`, `not_null`, `accepted_values`, `relationships`.

**Custom (singular) tests** — plain `.sql` files in `tests/`. The test *passes* if the query returns **zero rows**:

```sql
-- tests/assert_positive_order_amounts.sql
SELECT order_id
FROM {{ ref('fct_orders') }}
WHERE amount <= 0
```

**Run tests:**
```bash
dbt test                        # all tests
dbt test --select fct_orders    # tests for one model
dbt test --select source:raw    # tests for sources
```

---

### 3. Macros and Jinja Templating

dbt uses **Jinja2** to make SQL dynamic. Macros are reusable functions defined in `.sql` files under `macros/`.

**Built-in Jinja examples:**
```sql
-- Conditional logic
{% if target.name == 'prod' %}
  WHERE created_at >= CURRENT_DATE - 7
{% endif %}

-- Loop
SELECT
  {% for col in ['a', 'b', 'c'] %}
    SUM({{ col }}) AS sum_{{ col }}{% if not loop.last %},{% endif %}
  {% endfor %}
```

**Custom macro:**
```sql
-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name) %}
    ({{ column_name }} / 100.0)::DECIMAL(10,2)
{% endmacro %}

-- Usage in a model
SELECT {{ cents_to_dollars('amount_cents') }} AS amount_usd
```

**Interview signal:** Macros enable DRY SQL — great for date spine generation, data type casting, or environment-specific logic.

---

### 4. Incremental Models

Incremental models process **only new or changed rows** rather than rebuilding from scratch — critical for large tables.

```sql
-- models/fct_events.sql
{{ config(materialized='incremental', unique_key='event_id') }}

SELECT
    event_id,
    user_id,
    event_type,
    created_at
FROM {{ source('raw', 'events') }}

{% if is_incremental() %}
  WHERE created_at > (SELECT MAX(created_at) FROM {{ this }})
{% endif %}
```

**How it works:**
1. On first run: builds the full table.
2. On subsequent runs: `is_incremental()` is `true`, so only new rows are fetched and merged/appended.

**`unique_key`** — If set, dbt will `MERGE` (upsert) on that key. Without it, rows are appended.

**`incremental_strategy`** options (warehouse-dependent):
| Strategy | Description |
|---|---|
| `append` | Insert new rows only (no deduplication) |
| `merge` | Upsert based on `unique_key` |
| `delete+insert` | Delete matching rows, re-insert |
| `insert_overwrite` | Overwrite partitions (BigQuery/Spark) |

**When to use incremental models:**
- Tables with millions+ rows where a full refresh would be slow/expensive.
- Event tables, logs, clickstream data.
- When source data is append-only or has a reliable `updated_at` timestamp.

**Gotcha:** Full refreshes are still needed periodically or after schema changes:
```bash
dbt run --select fct_events --full-refresh
```

---

### 5. Lineage / DAG in dbt

dbt automatically builds a **Directed Acyclic Graph (DAG)** from your `ref()` and `source()` calls. Each node is a model, source, test, or snapshot; edges represent dependencies.

**Why it matters:**
- dbt runs models in dependency order — no manual orchestration needed.
- Enables selective execution: run a model and all its upstream/downstream dependencies.

**CLI selectors:**
```bash
dbt run --select fct_orders+          # fct_orders and all downstream
dbt run --select +fct_orders          # fct_orders and all upstream
dbt run --select +fct_orders+         # full lineage
dbt run --select tag:daily            # models tagged 'daily'
```

**Viewing the DAG:**
- `dbt docs generate` + `dbt docs serve` launches an interactive lineage graph in the browser.
- The DAG helps identify bottlenecks, long dependency chains, and blast radius of changes.

**Interview signal:** Understand that the DAG is derived implicitly from code — there's no separate config file. dbt is a *transformation* tool, not an orchestrator (use Airflow/Prefect/Dagster for scheduling).

---

## 📚 Resources

| Resource | What to do |
|---|---|
| [Snowflake Quickstarts](https://quickstarts.snowflake.com/) | Free hands-on labs — try the "Getting Started with Snowflake" and data loading labs |
| [dbt Docs — Introduction](https://docs.getdbt.com/docs/introduction) | Read the first 3 sections: What is dbt?, How dbt Works, and dbt Projects |
| [dbt Learn (free courses)](https://courses.getdbt.com/) | "dbt Fundamentals" course is ~4 hours and covers everything above |
| [Snowflake Docs — Virtual Warehouses](https://docs.snowflake.com/en/user-guide/warehouses-overview) | Reference for warehouse sizing and billing |

---

## ✅ Quick Self-Check

Before your interview, make sure you can answer these without notes:

1. What's the advantage of Snowflake's separation of compute and storage?
2. When would you use Snowpipe vs. `COPY INTO`?
3. What does zero-copy cloning actually mean — is any data duplicated?
4. What's the difference between `ref()` and `source()` in dbt?
5. How does an incremental model know which rows to process?
6. What does `dbt test` actually check, and what does a "passing" custom test look like?
7. How is the dbt DAG built — where is it configured?
