# Humana Data Engineer — Interview Prep Guide

---

## Table of Contents
1. [SQL & Python (Core Technical)](#1-sql--python-core-technical)
2. [Data Engineering Fundamentals](#2-data-engineering-fundamentals)
3. [Healthcare / Humana-Specific](#3-healthcare--humana-specific)
4. [Cloud & Modern Stack](#4-cloud--modern-stack)
5. [Root Cause Analysis & Problem Solving](#5-root-cause-analysis--problem-solving)
6. [Behavioral / Situational](#6-behavioral--situational)
7. [Things to Proactively Mention](#7-things-to-proactively-mention)

---

## 1. SQL & Python (Core Technical)

### SQL

**Q: Write a query to find duplicate records in a table.**
```sql
SELECT column_name, COUNT(*) AS occurrences
FROM table_name
GROUP BY column_name
HAVING COUNT(*) > 1;
```

---

**Q: What is the difference between `INNER JOIN`, `LEFT JOIN`, and `FULL OUTER JOIN`?**

| Join Type | Returns |
|---|---|
| `INNER JOIN` | Only rows with matching values in **both** tables |
| `LEFT JOIN` | All rows from the **left** table + matched rows from the right (NULLs for no match) |
| `FULL OUTER JOIN` | All rows from **both** tables (NULLs where no match on either side) |

---

**Q: What is the difference between `WHERE` and `HAVING`?**

- `WHERE` filters rows **before** aggregation.
- `HAVING` filters groups **after** aggregation.

```sql
-- WHERE filters individual rows
SELECT department, COUNT(*) FROM employees
WHERE status = 'active'
GROUP BY department;

-- HAVING filters aggregated groups
SELECT department, COUNT(*) FROM employees
GROUP BY department
HAVING COUNT(*) > 10;
```

---

**Q: Write a query using window functions.**
```sql
-- ROW_NUMBER: assigns a unique rank per partition
SELECT
    member_id,
    claim_date,
    claim_amount,
    ROW_NUMBER() OVER (PARTITION BY member_id ORDER BY claim_date DESC) AS row_num
FROM claims;

-- LAG: compare current row to the previous row
SELECT
    member_id,
    claim_date,
    claim_amount,
    LAG(claim_amount) OVER (PARTITION BY member_id ORDER BY claim_date) AS prev_claim_amount
FROM claims;
```

---

**Q: How do you optimize a slow-running query?**

- Use indexes on frequently filtered/joined columns
- Avoid `SELECT *` — select only needed columns
- Use CTEs or temp tables to break up complex logic
- Filter early with `WHERE` to reduce row scans
- Analyze the query execution plan (`EXPLAIN` / `EXPLAIN ANALYZE`)
- Avoid functions on indexed columns in `WHERE` clauses

---

**Q: What are CTEs and when would you use them vs. subqueries?**

A **CTE (Common Table Expression)** is a named temporary result set defined with `WITH`. It improves readability and can be referenced multiple times in a query.

Use a **CTE** when:
- Logic is complex and needs to be broken into readable steps
- You need to reference the same subquery more than once

Use a **subquery** when:
- The logic is simple and only used once
- Performance is critical and the optimizer handles it better inline

```sql
WITH active_members AS (
    SELECT member_id FROM members WHERE status = 'active'
)
SELECT * FROM claims
WHERE member_id IN (SELECT member_id FROM active_members);
```

---

### Python

**Q: How do you handle missing/null values in a pandas DataFrame?**

```python
import pandas as pd

df = pd.read_csv("data.csv")

# Check for nulls
df.isnull().sum()

# Drop rows with any null
df.dropna(inplace=True)

# Fill nulls with a value
df['column'].fillna(0, inplace=True)

# Fill with column mean
df['column'].fillna(df['column'].mean(), inplace=True)
```

---

**Q: Write a function to clean or transform a dataset.**

```python
def clean_member_data(df):
    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Fill missing values
    df['age'].fillna(df['age'].median(), inplace=True)

    # Convert date strings to datetime
    df['enrollment_date'] = pd.to_datetime(df['enrollment_date'])

    return df
```

---

**Q: Explain list comprehensions and when to use them.**

```python
# Standard loop
squares = []
for x in range(10):
    squares.append(x ** 2)

# List comprehension (preferred for simple transformations)
squares = [x ** 2 for x in range(10)]

# With condition
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
```

Use list comprehensions for simple, readable transformations. Avoid them when logic is complex — a regular loop is clearer.

---

**Q: What libraries do you use for data manipulation?**

| Library | Purpose |
|---|---|
| `pandas` | DataFrames, data wrangling, I/O |
| `numpy` | Numerical operations, array math |
| `sqlalchemy` | Database connections |
| `pyarrow` / `fastparquet` | Reading/writing Parquet files |
| `boto3` | AWS/Azure blob storage interactions |

---

## 2. Data Engineering Fundamentals

**Q: What is the difference between ETL and ELT?**

| | ETL | ELT |
|---|---|---|
| **Order** | Extract → Transform → Load | Extract → Load → Transform |
| **Where transform happens** | Outside the warehouse (e.g., Spark, Python) | Inside the warehouse (e.g., Snowflake, BigQuery) |
| **Best for** | Legacy systems, sensitive data masking before load | Cloud data warehouses with abundant compute |
| **Tools** | Talend, Informatica, custom Python | dbt, Snowflake, BigQuery |

---

**Q: What is the difference between a data warehouse, data lake, and data lakehouse?**

| | Data Warehouse | Data Lake | Data Lakehouse |
|---|---|---|---|
| **Data type** | Structured only | Structured, semi, unstructured | All types |
| **Schema** | Schema-on-write | Schema-on-read | Schema-on-read with governance |
| **Examples** | Snowflake, Redshift | S3, Azure Data Lake | Databricks, Delta Lake |
| **Use case** | BI, reporting | Raw storage, ML | Unified analytics + ML |

---

**Q: How do you handle schema changes in a data pipeline?**

- Use schema evolution features in tools like dbt or Snowflake
- Version your data models and use migrations
- Implement schema validation checks at ingestion
- Alert downstream consumers when breaking changes occur
- Use `MERGE` statements to handle new columns gracefully

---

**Q: What strategies do you use to ensure data quality?**

- Row count checks between source and destination
- Null checks on required fields
- Referential integrity checks (e.g., every `member_id` exists in the members table)
- Range checks (e.g., age must be between 0–120)
- Use dbt tests (`not_null`, `unique`, `accepted_values`, `relationships`)
- Log anomalies and alert on threshold breaches

---

**Q: How do you handle pipeline failures and ensure idempotency?**

- **Idempotency**: Running a pipeline multiple times produces the same result (use `MERGE`/upsert instead of raw `INSERT`)
- Implement retry logic with exponential backoff
- Use checkpointing to resume from the last successful step
- Log all failures with timestamps and context
- Design pipelines to be stateless where possible

---

## 3. Healthcare / Humana-Specific

**Q: What is HEDIS and why does it matter?**

**HEDIS (Healthcare Effectiveness Data and Information Set)** is a standardized set of performance measures developed by NCQA (National Committee for Quality Assurance). It is used by health plans to measure quality of care across dimensions like:

- Preventive care (mammograms, colonoscopies)
- Chronic disease management (diabetes, hypertension)
- Medication adherence
- Behavioral health

Insurers like Humana use HEDIS scores to demonstrate quality to employers, CMS, and regulators. Poor scores can affect star ratings and revenue.

---

**Q: What is Medicare Risk Adjustment and what is an HCC?**

**Medicare Risk Adjustment** is a system used by CMS to adjust payments to Medicare Advantage (MA) plans based on the health status of their enrolled members. Sicker members = higher payments to the plan.

**HCC (Hierarchical Condition Category)** is the coding system used to classify diagnoses. Each HCC maps to a risk score that reflects expected healthcare cost.

Key points:
- Based on ICD-10 diagnosis codes from claims data
- Must be documented and submitted annually
- Accurate coding directly impacts plan revenue

---

**Q: What is an EHR and what challenges come with ingesting EHR data?**

An **EHR (Electronic Health Record)** is a digital record of a patient's health history. Common EHR systems include Epic, Cerner, and Allscripts.

**Challenges:**
- Non-standardized formats across systems (HL7, FHIR, CSV exports)
- Inconsistent coding practices between providers
- Data completeness — not all encounters are captured
- HIPAA compliance requirements for handling PHI (Protected Health Information)
- Deduplication of patients across systems

---

**Q: What is Membership data and how is it used?**

Membership data tracks who is enrolled in a health plan — including enrollment dates, plan type, geographic region, demographics, and coverage details.

It is used to:
- Determine eligibility for claims processing
- Identify members for outreach and care management programs
- Calculate HEDIS denominators (who *should* have received care)
- Support Medicare Risk Adjustment submissions

---

**Q: How would you handle HIPAA compliance when working with patient data?**

- Never expose PHI (names, SSNs, DOBs, addresses, member IDs) in logs or outputs
- Use role-based access control (RBAC) on data platforms
- Encrypt data at rest and in transit
- Anonymize or de-identify data in development/test environments
- Audit data access and maintain access logs
- Follow your organization's data governance and security policies

---

## 4. Cloud & Modern Stack

### Snowflake

**Q: What makes Snowflake different from traditional databases?**

- **Separation of compute and storage**: Scale each independently
- **Virtual warehouses**: Isolated compute clusters — multiple teams can query simultaneously without contention
- **Time Travel**: Query data as it existed at a prior point in time
- **Zero-copy cloning**: Instantly clone databases/tables without duplicating storage
- **Native semi-structured data support**: Query JSON with `VARIANT` type

---

**Q: What Azure services are commonly used in data engineering?**

| Service | Purpose |
|---|---|
| **Azure Data Factory (ADF)** | Orchestration and ETL pipelines |
| **Azure Blob Storage / ADLS Gen2** | Raw data lake storage |
| **Azure SQL Database** | Relational database |
| **Azure Synapse Analytics** | Unified analytics platform |
| **Azure Databricks** | Spark-based big data processing |
| **Azure Key Vault** | Secrets and credentials management |

---

### dbt (Data Build Tool)

**Q: What is dbt and how does it fit in the modern data stack?**

**dbt** is a transformation framework that allows data analysts and engineers to write SQL `SELECT` statements and dbt handles the DDL/DML (`CREATE TABLE AS`, `INSERT`, etc.).

**Key features:**
- Transforms data **inside** the warehouse (ELT pattern)
- Built-in testing (`not_null`, `unique`, `accepted_values`)
- Auto-generated documentation and data lineage
- Modular SQL with `ref()` to manage dependencies between models
- Supports Jinja templating for dynamic SQL

**Where it fits:**
```
Source Data → (ADF / Fivetran) → Raw Layer → [dbt transforms] → Staging → Mart → BI Tool
```

---

## 5. Root Cause Analysis & Problem Solving

**Q: A dashboard metric suddenly looks wrong — how do you investigate?**

1. **Confirm the issue**: Is it one metric or many? One date or all history?
2. **Check recency**: Did a pipeline run recently? Check logs for failures or delays.
3. **Compare to source**: Does the warehouse data match the upstream source?
4. **Check for schema changes**: Were any columns renamed, added, or dropped?
5. **Check for data volume anomalies**: Sudden drop/spike in row counts?
6. **Trace the lineage**: Which models/tables feed the metric? (dbt lineage helps here)
7. **Document and communicate findings** to stakeholders with timeline and resolution

---

**Q: How do you validate data coming from a new source?**

- Profile the data: row counts, null rates, distinct value counts, min/max ranges
- Cross-check key metrics against the source system or a known report
- Check referential integrity (e.g., do all IDs in this table exist in the dimension table?)
- Look for unexpected duplicates
- Validate date ranges — are there gaps or future-dated records?
- Work with the source system owner to confirm expected volumes and formats

---

## 6. Behavioral / Situational

Use the **STAR format** (Situation, Task, Action, Result) for all behavioral questions.

| Question | What They're Looking For |
|---|---|
| Tell me about a project where you used data to drive a business decision | Impact, communication, business acumen |
| Describe a time you worked with a messy or incomplete dataset | Problem-solving, persistence, attention to detail |
| How do you communicate technical findings to non-technical stakeholders? | Clarity, empathy, visualization skills |
| Tell me about a time you had to learn something quickly on the job | Adaptability, resourcefulness |
| How do you manage competing priorities or deadlines? | Organization, communication, judgment |
| Tell me about a time a pipeline broke in production. What did you do? | Incident response, ownership, process improvement |

---

## 7. Things to Proactively Mention

Even if not directly asked, weave these into your answers where relevant:

- **Git / Version Control**: Branching strategies, pull requests, code reviews for dbt models or pipeline code
- **Agile / Scrum**: Sprint planning, backlog grooming, working with cross-functional teams
- **Documentation**: Writing READMEs, data dictionaries, pipeline runbooks
- **Slowly Changing Dimensions (SCDs)**: Type 1 (overwrite), Type 2 (versioned history rows), Type 3 (add a column) — relevant for membership and claims history
- **Data Lineage Awareness**: Understanding how data flows from source to consumption layer
- **Monitoring & Alerting**: Proactively catching pipeline issues before stakeholders do

---

> **Top priority prep areas for this role:**
> SQL window functions · ETL/ELT pipeline design · dbt basics · HEDIS & Medicare Risk Adjustment fundamentals · Snowflake architecture