# Humana Data Engineer 2 — Interview Study Guide

> **Role summary:** Mid-level data engineering position on the Integrated Health technology team. You'll build pipelines, data models, and cloud-native architectures — and be expected to work with some autonomy. Healthcare domain knowledge is a bonus, not a blocker.

---

## Priority Legend

| Label | Meaning |
|---|---|
| 🔴 Must know | Explicitly listed as a required qualification |
| 🟡 Nice to have | Listed as a preferred qualification — will set you apart |
| 🔵 Soft / context | Behavioral or domain knowledge — good to be aware of |

---

## Section 1 — SQL 🔴

SQL is a required qualification and will almost certainly be tested directly.

### Topics to cover

- **Window functions** — `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LAG()`, `LEAD()`, `PARTITION BY`. These are the most commonly tested.
- **Joins & aggregations** — `INNER`, `LEFT`, anti-joins, `GROUP BY`, `HAVING`, CTEs (`WITH` clauses)
- **Query optimization** — reading explain plans, avoiding `SELECT *`, indexing concepts, partitioning
- **Root cause analysis on data** — diagnosing nulls, duplicates, unexpected row counts in a dataset

### Practice questions

1. Find the second-highest salary in a table without using `LIMIT` or `TOP`
2. Given a table of member visits, find members who had visits in consecutive months
3. Write a query to deduplicate records keeping only the most recent row per member ID
4. Explain the difference between `RANK()`, `DENSE_RANK()`, and `ROW_NUMBER()` — when would you use each?

### Resources

- [LeetCode — Top SQL 50](https://leetcode.com/studyplan/top-sql-50/) *(free, great window function practice)*
- [StrataScratch](https://www.stratascratch.com/) *(real interview SQL questions filtered by company)*

---

## Section 2 — Python 🔴

Also a required qualification. Expect at least one coding question.

### Topics to cover

- **pandas basics** — DataFrames, `groupby`, `merge`, `apply`, handling nulls and duplicates
- **Writing clean functions** — list comprehensions, error handling, type hints, readable code
- **REST APIs & file I/O** — `requests` library, reading/writing CSVs, parsing JSON responses

### Practice questions

1. Write a function to compute a moving window average given a list and a window size
2. Given a DataFrame with nulls and duplicates, clean it and compute a grouped summary
3. Write a function to flatten a nested JSON response from a REST API
4. Find the longest common prefix in a list of strings

### Resources

- [LeetCode — Medium Arrays & Strings](https://leetcode.com/problemset/?difficulty=MEDIUM&topicSlugs=array%2Cstring) *(good Python warm-up)*

---

## Section 3 — Pipelines & Data Architecture 🔴

The JD explicitly mentions data pipelines, ELT/ETL, data lakes, and data warehouses.

### Topics to cover

- **ELT vs ETL** — when to transform in the warehouse vs. before loading; trade-offs for each
- **Apache Airflow concepts** — DAGs, tasks, operators, scheduling, retries, XComs, SLAs
- **Data modeling basics** — star schema, fact vs. dimension tables, slowly changing dimensions (SCDs)
- **Idempotency** — why pipelines must be safely re-runnable; deduplication and upsert patterns
- **Big data concepts** — Spark basics, partitioning strategies, distributed processing trade-offs

### Practice questions

1. How would you design a pipeline to ingest daily claims data from an external source into Snowflake?
2. What's the difference between a fact table and a dimension table? Give a healthcare example.
3. How do you ensure a pipeline is idempotent? What happens if it runs twice?
4. Walk me through how you'd debug a pipeline that suddenly started producing duplicate rows.

### Resources

- [Apache Airflow — Official Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html)

---

## Section 4 — Snowflake & dbt 🟡

Listed as preferred qualifications — if you know these, say so early. Even surface-level familiarity is a plus.

### Snowflake topics

- Virtual warehouses (compute vs. storage separation)
- Stages and data loading (`COPY INTO`, Snowpipe)
- Time travel and zero-copy cloning
- Clustering keys and micro-partitions

### dbt topics

- Models, sources, and refs
- Tests (schema tests, custom tests)
- Macros and Jinja templating
- Incremental models — how they work and when to use them
- Lineage / DAG in dbt

### Resources

- [Snowflake Quickstarts](https://quickstarts.snowflake.com/) *(free hands-on labs)*
- [dbt Docs — Introduction](https://docs.getdbt.com/docs/introduction) *(read the first 3 sections)*

---

## Section 5 — Azure Ecosystem 🟡

Also a preferred qualification. You don't need deep expertise — familiarity with the services and how they connect is enough.

### Services to know conceptually

| Service | What it does |
|---|---|
| Azure Data Factory (ADF) | Orchestration — pipelines, linked services, triggers |
| Azure Data Lake Storage (ADLS) | Cloud object storage, organized in tiers |
| Azure Databricks | Spark-based analytics and ML platform |
| Azure Synapse Analytics | Combined data warehouse + analytics workspace |
| Delta Lake | Open-source storage layer for ACID transactions on ADLS |

### Resources

- [Microsoft Learn — Azure Data Engineer Path](https://learn.microsoft.com/en-us/training/paths/data-engineer-azure/) *(free, ~8–10 hours total — skim the parts most relevant to the JD)*

---

## Section 6 — Healthcare Data Context 🟡

You don't need to be an expert, but being able to speak to these concepts will make you stand out.

### Key concepts to be aware of

- **EHR (Electronic Health Records)** — structured clinical data stored by providers; formats include HL7 and FHIR
- **Claims data** — billing records from providers to insurers; includes diagnosis codes (ICD-10), procedure codes (CPT), and member IDs
- **HEDIS measures** — Healthcare Effectiveness Data and Information Set; standardized quality metrics used to evaluate health plans (e.g., rates of preventive screenings, medication adherence)
- **Medicare Risk Adjustment** — a model that adjusts payments to insurers based on the health risk of their members; uses HCC (Hierarchical Condition Category) codes derived from diagnosis data

### What to say if asked

You don't need to have worked in healthcare before. A good answer sounds like: *"I haven't worked directly with HEDIS or risk adjustment data, but I've picked up new data domains quickly in past roles — I'd lean on documentation, SMEs on the team, and existing data dictionaries to get up to speed fast."*

---

## Section 7 — Behavioral Questions 🔵

Humana's interview process includes a culture/fit round. Use the **STAR format**: Situation → Task → Action → Result.

### Stories to prepare (have 4–5 ready, adaptable to multiple questions)

1. A time you diagnosed and fixed a bad data pipeline or data quality issue
2. A time you had to influence a technical decision without direct authority
3. A time you balanced speed vs. quality under a tight deadline
4. A time you explained complex data findings to a non-technical stakeholder
5. A time you proactively identified a problem before it became critical
6. A conflict with a teammate or another team — and how you resolved it

### Humana-specific angles

- **Mission tie-in** — Have a genuine 2–3 sentence answer to "why Humana / why healthcare data?" Tie it to real impact on patient outcomes or health equity if you can.
- **Autonomy and initiative** — The JD says you'll "shape departmental strategy." In behavioral answers, highlight moments where you suggested improvements or took ownership beyond your assigned scope.
- **AI awareness** — Based on real interview reports, they may ask a quick question about AI (e.g., "what excites you about AI in data engineering?"). Have a brief, grounded answer ready.

---

## Study Plan (1–2 weeks)

| Days | Focus |
|---|---|
| Days 1–2 | SQL practice — LeetCode Top SQL 50, window functions especially |
| Days 3–4 | Python practice — pandas, writing functions, LeetCode medium strings/arrays |
| Days 5–6 | Pipeline & architecture concepts — Airflow, ELT/ETL, data modeling |
| Day 7 | Snowflake quickstart + skim dbt docs intro |
| Day 8 | Azure services overview (Microsoft Learn — skim) |
| Day 9 | Healthcare context — HEDIS, risk adjustment, claims data basics |
| Days 10–11 | STAR story prep + mock behavioral answers |
| Day 12 | Review weak spots; revisit any SQL/Python problems you struggled with |

---

## Quick-Reference Checklist

### Technical
- [ ] Window functions (`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`)
- [ ] CTEs and complex joins
- [ ] Query optimization concepts
- [ ] pandas: `groupby`, `merge`, `apply`, null handling
- [ ] Python: writing clean reusable functions
- [ ] ETL vs ELT trade-offs
- [ ] Airflow: DAGs, operators, scheduling, retries
- [ ] Star schema / fact-dimension modeling
- [ ] Idempotency in pipelines
- [ ] Snowflake architecture basics
- [ ] dbt: models, tests, incremental, lineage
- [ ] Azure: ADF, ADLS, Databricks at a conceptual level

### Behavioral
- [ ] 5–6 STAR stories drafted and practiced
- [ ] "Why Humana / why healthcare?" answer ready
- [ ] "What excites you about AI?" answer ready
- [ ] Conflict resolution story ready
- [ ] Example of taking initiative beyond assigned scope
