# Section 3 — Pipelines & Data Architecture 🔴

> **Priority:** High — explicitly called out in the JD (data pipelines, ELT/ETL, data lakes, data warehouses)

---

## 1. ELT vs ETL

### Definitions

| | ETL | ELT |
|---|---|---|
| **Stands for** | Extract → Transform → Load | Extract → Load → Transform |
| **Where transform happens** | Outside the warehouse (staging server, custom code) | Inside the warehouse (SQL, dbt, etc.) |
| **Best for** | Legacy systems, strict data governance, small/medium data | Cloud-native warehouses (Snowflake, BigQuery, Redshift), large data volumes |
| **Tools** | Informatica, Talend, SSIS | dbt, Snowflake, BigQuery, Spark |

### When to Use Each

**Use ETL when:**
- Data must be cleaned/masked *before* it touches the warehouse (PII, compliance)
- The destination system has limited compute or storage
- Transformations are complex and compute-heavy outside SQL
- Working with legacy or on-prem systems

**Use ELT when:**
- Using a cloud data warehouse with abundant compute (Snowflake, BigQuery)
- You want raw data preserved for re-transformation later
- Teams want SQL-based transformations (accessible to analysts, not just engineers)
- Schema changes are frequent — raw data is preserved as a fallback

### Trade-offs Summary

| Concern | ETL | ELT |
|---|---|---|
| Data quality at load | ✅ Clean data in warehouse | ⚠️ Raw/messy data lands first |
| Storage cost | ✅ Only transformed data stored | ⚠️ Raw + transformed both stored |
| Flexibility | ⚠️ Re-runs require full re-extract | ✅ Can re-transform from raw anytime |
| Compute cost | ⚠️ External compute needed | ✅ Warehouse compute used |
| Auditability | ⚠️ Raw data may be lost | ✅ Full lineage from raw → final |

---

## 2. Apache Airflow Concepts

### Core Architecture

```
Scheduler → triggers DAGs based on schedule
Workers   → execute individual tasks
Metadata DB → stores DAG state, task history
Web UI    → monitor, trigger, debug DAGs
```

### DAGs (Directed Acyclic Graphs)

A **DAG** is a collection of tasks with defined dependencies and a schedule.

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_team',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
}

with DAG(
    dag_id='daily_claims_ingestion',
    default_args=default_args,
    schedule_interval='@daily',       # or '0 6 * * *' (cron)
    start_date=datetime(2024, 1, 1),
    catchup=False,                    # don't backfill missed runs
) as dag:
    ...
```

**Key DAG properties:**
- `schedule_interval` — cron expression or preset (`@daily`, `@hourly`, `@weekly`)
- `catchup=False` — prevents Airflow from running all past missed intervals on startup
- `start_date` — when the DAG becomes active
- `max_active_runs` — limits concurrent DAG runs

### Tasks & Operators

A **task** is a unit of work. An **operator** is the *type* of task.

| Operator | Use Case |
|---|---|
| `PythonOperator` | Run a Python function |
| `BashOperator` | Run a shell command |
| `PostgresOperator` / `SnowflakeOperator` | Execute SQL |
| `S3ToSnowflakeOperator` | Load data between cloud services |
| `BranchPythonOperator` | Conditional branching logic |
| `DummyOperator` | Placeholder for grouping |
| `SensorOperator` | Wait for a condition (file arrives, API ready) |

```python
extract = PythonOperator(
    task_id='extract_claims',
    python_callable=extract_from_sftp,
)

load = SnowflakeOperator(
    task_id='load_to_snowflake',
    sql='COPY INTO claims_raw FROM @claims_stage',
    snowflake_conn_id='snowflake_prod',
)

transform = PythonOperator(
    task_id='transform_claims',
    python_callable=run_dbt_models,
)

# Define dependencies
extract >> load >> transform
```

### Scheduling & Retries

- **Retries:** `retries=3` + `retry_delay=timedelta(minutes=10)` — Airflow retries failed tasks automatically
- **SLAs:** Define max acceptable task duration; breach triggers an alert callback
  ```python
  sla=timedelta(hours=2)  # Alert if task takes > 2 hours
  ```
- **Execution date:** The *logical* date of the run, not the actual run time (important for backfills)

### XComs (Cross-Communication)

XComs allow tasks to pass small pieces of data to each other.

```python
# Task 1: push a value
def extract_fn(**context):
    record_count = fetch_data()
    context['ti'].xcom_push(key='record_count', value=record_count)

# Task 2: pull the value
def validate_fn(**context):
    count = context['ti'].xcom_pull(task_ids='extract_claims', key='record_count')
    if count == 0:
        raise ValueError("No records extracted!")
```

> ⚠️ **XComs are for small metadata, not large datasets.** Never XCom a DataFrame — use S3/GCS as intermediate storage instead.

---

## 3. Data Modeling Basics

### Star Schema

The **star schema** organizes data into a central **fact table** surrounded by **dimension tables**.

```
         dim_patient
              |
dim_provider—fact_claims—dim_date
              |
         dim_diagnosis
```

**Why "star"?** The ERD looks like a star when drawn out.

### Fact vs Dimension Tables

| | Fact Table | Dimension Table |
|---|---|---|
| **Contains** | Measurable events/transactions | Descriptive attributes |
| **Rows** | One per event (claim, visit, transaction) | One per entity (patient, provider, date) |
| **Columns** | Foreign keys + numeric measures | Descriptive text, IDs, categorizations |
| **Size** | Very large (billions of rows) | Smaller (thousands–millions of rows) |
| **Changes** | Append-only (new events) | Slowly changing |
| **Example** | `fact_claims` | `dim_patient`, `dim_provider` |

**Healthcare example:**

```sql
-- fact_claims: one row per insurance claim
CREATE TABLE fact_claims (
    claim_id        BIGINT PRIMARY KEY,
    patient_key     INT REFERENCES dim_patient(patient_key),
    provider_key    INT REFERENCES dim_provider(provider_key),
    date_key        INT REFERENCES dim_date(date_key),
    diagnosis_key   INT REFERENCES dim_diagnosis(diagnosis_key),
    billed_amount   DECIMAL(10,2),
    paid_amount     DECIMAL(10,2),
    claim_status    VARCHAR(20)
);

-- dim_patient: one row per patient
CREATE TABLE dim_patient (
    patient_key     INT PRIMARY KEY,      -- surrogate key
    patient_id      VARCHAR(20),          -- natural/business key
    full_name       VARCHAR(100),
    date_of_birth   DATE,
    gender          VARCHAR(10),
    insurance_plan  VARCHAR(50)
);
```

### Slowly Changing Dimensions (SCDs)

Dimensions change over time (patient moves, provider changes network). SCDs define *how* to handle history.

| Type | Strategy | Use When |
|---|---|---|
| **SCD Type 1** | Overwrite the old value | History doesn't matter (typo fix) |
| **SCD Type 2** | Add a new row with date ranges | Need full history (address changes) |
| **SCD Type 3** | Add a "previous value" column | Only need current + one prior value |

**SCD Type 2 example (most common):**

```sql
-- dim_patient with SCD Type 2
patient_key   | patient_id | insurance_plan | effective_date | expiry_date  | is_current
101           | P001       | BlueCross PPO  | 2022-01-01     | 2023-06-30   | FALSE
208           | P001       | Aetna HMO      | 2023-07-01     | 9999-12-31   | TRUE
```

When patient P001 changes insurance, a new row is inserted rather than updating the old one. Fact rows preserve the `patient_key` at the time of the claim.

---

## 4. Idempotency

### Definition

A pipeline is **idempotent** if running it multiple times produces the same result as running it once.

> "If this pipeline runs twice, is the data any different than if it ran once?"

### Why It Matters

- Pipelines fail and must be retried
- Airflow reruns, backfills, and manual triggers happen
- Without idempotency: duplicate rows, inflated metrics, corrupted data

### Idempotency Patterns

**1. DELETE + INSERT (Partition Replace)**
```sql
-- Delete the partition for today, then re-insert
DELETE FROM claims_daily WHERE claim_date = '{{ ds }}';
INSERT INTO claims_daily
SELECT * FROM claims_raw WHERE claim_date = '{{ ds }}';
```

**2. MERGE / UPSERT**
```sql
-- Snowflake MERGE
MERGE INTO claims_final AS target
USING claims_staging AS source
  ON target.claim_id = source.claim_id
WHEN MATCHED THEN UPDATE SET
    paid_amount = source.paid_amount,
    updated_at = source.updated_at
WHEN NOT MATCHED THEN INSERT (claim_id, paid_amount, ...)
    VALUES (source.claim_id, source.paid_amount, ...);
```

**3. Deduplication with ROW_NUMBER**
```sql
-- Keep only the latest version of each claim
WITH deduped AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY claim_id
            ORDER BY updated_at DESC
        ) AS rn
    FROM claims_raw
)
SELECT * FROM deduped WHERE rn = 1;
```

**4. Stage → Swap Pattern**
```
1. Load fresh data into `claims_temp`
2. Validate row counts, nulls, etc.
3. SWAP `claims_temp` → `claims_final` (atomic, zero-downtime)
```

### Checklist for Idempotent Pipelines

- [ ] Use surrogate keys or natural keys for deduplication
- [ ] Partition deletes/replaces by date or batch ID
- [ ] Use MERGE instead of blind INSERT
- [ ] Store `pipeline_run_id` on records to trace provenance
- [ ] Validate before committing (row counts, null checks)

---

## 5. Big Data Concepts

### Apache Spark Basics

Spark is a distributed compute engine for processing large datasets across a cluster.

```
Driver Program
    ↓ submits jobs
Cluster Manager (YARN / Kubernetes / Standalone)
    ↓ allocates resources
Executors (worker nodes)
    ↓ execute tasks in parallel
```

**Key concepts:**

| Concept | Description |
|---|---|
| **RDD** | Resilient Distributed Dataset — low-level, fault-tolerant collection |
| **DataFrame** | High-level API, like a distributed SQL table (use this) |
| **Transformation** | Lazy operation (`filter`, `join`, `groupBy`) — builds a plan |
| **Action** | Triggers execution (`count`, `show`, `write`) |
| **Lazy evaluation** | Spark builds an execution plan and optimizes before running |
| **DAG** | Spark's internal execution plan (different from Airflow DAGs) |

**Simple PySpark example:**
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum

spark = SparkSession.builder.appName("ClaimsAgg").getOrCreate()

claims = spark.read.parquet("s3://bucket/claims/")

result = (
    claims
    .filter(col("claim_status") == "PAID")
    .groupBy("provider_id", "claim_date")
    .agg(sum("paid_amount").alias("total_paid"))
)

result.write.mode("overwrite").partitionBy("claim_date").parquet("s3://bucket/claims_agg/")
```

### Partitioning Strategies

Partitioning divides data into chunks that can be processed independently.

**Storage partitioning (file layout):**
```
s3://bucket/claims/
    claim_date=2024-01-01/
        part-00000.parquet
        part-00001.parquet
    claim_date=2024-01-02/
        ...
```
Benefits: Queries that filter by `claim_date` only scan relevant partitions ("partition pruning").

**Spark partitioning (in-memory):**
```python
# Repartition for even distribution before a join
claims.repartition(200, "provider_id")

# Coalesce to reduce partitions (e.g., before writing)
result.coalesce(10).write.parquet(...)
```

**Partition key selection:**
- Prefer low-to-medium cardinality columns (`claim_date`, `state`, `status`)
- Avoid high-cardinality keys (`claim_id`) — creates too many small files
- Avoid very low-cardinality keys (`is_paid: Y/N`) — skewed partitions

### Distributed Processing Trade-offs

| Concern | Detail |
|---|---|
| **Shuffles** | Expensive — moving data across nodes (triggered by `join`, `groupBy`). Minimize by broadcasting small tables. |
| **Skew** | One partition gets most of the data → bottleneck. Fix with salting or skew hints. |
| **Small files problem** | Too many tiny files → slow metadata ops. Use `coalesce` or compaction jobs. |
| **Serialization** | Python UDFs are slow (JVM → Python → JVM). Prefer native Spark SQL functions. |
| **Fault tolerance** | Spark re-computes lost partitions from lineage (RDD DAG). No manual failover needed. |

---

## Practice Questions

### Q1: Design a pipeline to ingest daily claims data from an external source into Snowflake

**Sample Answer:**

1. **Extract** — Use an Airflow DAG triggered daily (`@daily`). A `PythonOperator` calls the external API/SFTP and downloads the claims file to S3 (staged).

2. **Validate** — Check file exists, row count > 0, schema matches expected. Fail fast before loading.

3. **Load (Raw)** — Use `COPY INTO` to load raw JSON/CSV into a `claims_raw` table in Snowflake. This is append-only; each batch tagged with `load_date`.

4. **Transform** — A `SnowflakeOperator` runs a MERGE into `claims_final`, deduplicating on `claim_id` and updating changed records.

5. **Idempotency** — DELETE + INSERT by `claim_date` partition, or MERGE on `claim_id`. Re-running the DAG for the same date is safe.

6. **Monitoring** — Airflow SLAs alert if pipeline doesn't complete by 8 AM. Row count checks log anomalies.

---

### Q2: Difference between a fact table and a dimension table — healthcare example

**Fact table** (`fact_claims`): Records individual claim submissions. Each row is one event. Contains foreign keys to dimensions and numeric measures (`billed_amount`, `paid_amount`, `days_to_process`).

**Dimension table** (`dim_patient`): Describes *who* or *what* was involved. Each row is one entity. Contains descriptive attributes (`patient_name`, `DOB`, `insurance_plan`). Stable, relatively small.

*Simple rule:* "Did something happen?" → fact. "What is it / who is it?" → dimension.

---

### Q3: How do you ensure a pipeline is idempotent? What happens if it runs twice?

Use a **MERGE (upsert)** on a natural key (`claim_id`) rather than a plain INSERT. A second run will find existing records and update them (no duplicates) rather than inserting again.

Alternatively, **partition-replace**: `DELETE WHERE claim_date = run_date` then re-insert. The second run deletes what was inserted by the first run, then re-inserts cleanly.

If the pipeline runs twice *without* these protections, you get **duplicate rows** — inflated counts, double-paid amounts in aggregations, broken downstream reports.

---

### Q4: Debug a pipeline suddenly producing duplicate rows

**Systematic approach:**

1. **Confirm the duplicates** — How many? On which columns (`claim_id`? full row?)
2. **Check when it started** — Was there a code change, data source change, or schema change?
3. **Trace to the source** — Are duplicates in the raw/staging layer, or only in the final table?
4. **Common culprits:**
   - A `JOIN` exploding rows (many-to-many relationship)
   - A pipeline was changed from MERGE to INSERT
   - An upstream source started sending the same records twice
   - A backfill ran on top of existing data
   - A fanout issue in Spark (incorrect `explode` or `cross join`)
5. **Fix** — Add or restore the deduplication step. Backfill the affected date range.
6. **Prevent** — Add a `DISTINCT` count assertion in post-load validation. Alert if `count(*) != count(distinct claim_id)`.

---

## Resources

- [Apache Airflow — Official Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html)
- [dbt Docs — Data Modeling Concepts](https://docs.getdbt.com/docs/build/models)
- [Snowflake MERGE Documentation](https://docs.snowflake.com/en/sql-reference/sql/merge)
- [The Data Warehouse Toolkit (Kimball)](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/) — canonical reference for star schemas & SCDs
- [Apache Spark — Quick Start](https://spark.apache.org/docs/latest/quick-start.html)

---

*Study tip: For interviews, always tie abstract concepts back to a concrete healthcare/claims example. The interviewers want to see you apply these patterns, not just define them.*
