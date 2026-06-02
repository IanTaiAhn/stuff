# Backend Software Engineer II — Study Guide
### Prepared for: Aledade-Style Roles | Ian Tai Ahn

---

## Table of Contents

1. [Core: SQL & Databases](#1-core-sql--databases)
2. [Data Pipelines & ETL/ELT](#2-data-pipelines--etlelt)
3. [Database Internals](#3-database-internals)
4. [Observability & Performance Monitoring](#4-observability--performance-monitoring)
5. [Data Ingestion at Scale](#5-data-ingestion-at-scale)
6. [Docker & Kubernetes (Backend Context)](#6-docker--kubernetes-backend-context)
7. [CI/CD (Backend & Data Focus)](#7-cicd-backend--data-focus)
8. [Engineering Philosophy](#8-engineering-philosophy)
9. [Healthcare Domain Knowledge](#9-healthcare-domain-knowledge)
10. [Q&A Section](#qa-section)

---

## 1. Core: SQL & Databases

### Why It Matters
Aledade's JD explicitly requires 2+ years of SQL on **large multi-table datasets**. This means they expect you to not just write queries, but write *good* ones — fast, readable, and correct at scale.

### Key Concepts

**Window Functions**
Window functions perform calculations across a set of rows related to the current row, without collapsing them like `GROUP BY` does.

```sql
-- Rank patients by visit count within each provider
SELECT
  patient_id,
  provider_id,
  visit_count,
  RANK() OVER (PARTITION BY provider_id ORDER BY visit_count DESC) AS rank_in_provider
FROM patient_visits;
```

Common window functions: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LAG()`, `LEAD()`, `SUM() OVER`, `AVG() OVER`.

**CTEs (Common Table Expressions)**
CTEs (`WITH` clauses) make complex queries readable and reusable within a single query.

```sql
WITH eligible_patients AS (
  SELECT patient_id
  FROM enrollments
  WHERE plan_type = 'Medicare Advantage'
    AND enrollment_status = 'active'
),
visit_counts AS (
  SELECT patient_id, COUNT(*) AS visits
  FROM visits
  WHERE visit_date >= '2024-01-01'
  GROUP BY patient_id
)
SELECT e.patient_id, COALESCE(v.visits, 0) AS total_visits
FROM eligible_patients e
LEFT JOIN visit_counts v ON e.patient_id = v.patient_id;
```

**Query Optimization**
- Use `EXPLAIN` / `EXPLAIN ANALYZE` to inspect query plans before running expensive queries
- Prefer indexes on columns used in `WHERE`, `JOIN`, and `ORDER BY` clauses
- Avoid `SELECT *` — fetch only the columns you need
- Be aware of implicit type casts breaking index usage (e.g., comparing `VARCHAR` to `INT`)
- Use `LIMIT` during development to preview results cheaply

**Index Design**
- **B-tree indexes**: Default. Best for equality and range queries (`=`, `<`, `>`, `BETWEEN`)
- **Partial indexes**: Index only a subset of rows — efficient for filtering on a common condition
- **Composite indexes**: Cover multiple columns; column order matters (most selective first, or match query order)
- **Index bloat**: Indexes grow with writes and need maintenance (`REINDEX`, `VACUUM` in PostgreSQL)

**Joins at Scale**
- Understand the difference between `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, and `FULL OUTER JOIN`
- For large tables, joining on indexed foreign keys is critical
- Be cautious of **cartesian products** (missing join condition = every row × every row)

---

## 2. Data Pipelines & ETL/ELT

### Why It Matters
One of Aledade's preferred KSAs is designing, building, and optimizing ETL processes. Healthcare data pipelines are high-stakes — bad data means bad patient outcomes or billing failures.

### Key Concepts

**ETL vs. ELT**
- **ETL (Extract → Transform → Load)**: Transform data *before* loading into the destination. Common in older data warehouses with limited compute.
- **ELT (Extract → Load → Transform)**: Load raw data first, then transform inside the warehouse (e.g., Snowflake, BigQuery, dbt). Better for modern cloud data stacks.

**Pipeline Design Patterns**
- **Idempotency**: Running a pipeline multiple times should produce the same result. Use upserts (`INSERT ... ON CONFLICT`) instead of plain inserts.
- **Incremental loading**: Process only new/changed records using watermarks (e.g., `updated_at > last_run_timestamp`) rather than full reloads.
- **Backfilling**: Reprocessing historical data when logic changes. Design pipelines to accept a date range parameter.
- **Error handling & retries**: Classify errors as transient (retry) vs. fatal (alert and stop). Use dead-letter queues for unprocessable records.
- **Checkpointing**: Save progress so a failed pipeline can resume mid-run rather than restart from scratch.

**Airflow (Most Common in Healthcare Data Stacks)**
- Pipelines are defined as **DAGs** (Directed Acyclic Graphs)
- Each step is a **Task**; tasks have dependencies
- Operators: `PythonOperator`, `BashOperator`, `SQLExecuteQueryOperator`
- Key concepts: task retries, SLAs, backfill, `execution_date`

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract(): ...
def transform(): ...
def load(): ...

with DAG("claims_pipeline", start_date=datetime(2024, 1, 1), schedule_interval="@daily") as dag:
    t1 = PythonOperator(task_id="extract", python_callable=extract)
    t2 = PythonOperator(task_id="transform", python_callable=transform)
    t3 = PythonOperator(task_id="load", python_callable=load)
    t1 >> t2 >> t3
```

**dbt (Data Build Tool)**
- Transforms data inside your warehouse using SQL + Jinja templating
- Enforces modular, version-controlled SQL transformations
- Models: `source` → `staging` → `intermediate` → `mart`
- Supports tests (`not_null`, `unique`, `accepted_values`), documentation, and lineage

---

## 3. Database Internals

### Why It Matters
The JD asks for "in-depth knowledge of database systems" and specifically mentions replication, sharding, and high availability. These are common topics in backend/data engineering interviews.

### Key Concepts

**ACID Properties**
- **Atomicity**: A transaction either fully completes or fully rolls back — no partial states
- **Consistency**: A transaction brings the database from one valid state to another
- **Isolation**: Concurrent transactions don't interfere with each other
- **Durability**: Once committed, data persists even through crashes

**Transaction Isolation Levels** (from weakest to strongest)
| Level | Dirty Read | Non-Repeatable Read | Phantom Read |
|---|---|---|---|
| Read Uncommitted | ✅ Possible | ✅ Possible | ✅ Possible |
| Read Committed | ❌ Prevented | ✅ Possible | ✅ Possible |
| Repeatable Read | ❌ Prevented | ❌ Prevented | ✅ Possible |
| Serializable | ❌ Prevented | ❌ Prevented | ❌ Prevented |

PostgreSQL default: **Read Committed**. Higher isolation = more locking overhead.

**Replication**
- **Primary/Replica (Primary/Secondary)**: Writes go to primary, reads can be distributed to replicas
- **Synchronous replication**: Primary waits for replica to confirm write before acknowledging client. Safer, but slower.
- **Asynchronous replication**: Primary doesn't wait. Faster, but replica may lag — risk of data loss on failover.
- Use cases: read scaling, high availability, backups, analytics offloading

**Sharding**
- Horizontal partitioning — split data across multiple database instances (shards) by a **shard key** (e.g., `patient_id % N`)
- Challenges: cross-shard joins are expensive, resharding is painful, hotspots if key is poorly chosen
- Alternatives: table partitioning (within one DB), read replicas (for read scaling)

**PostgreSQL-Specific**
- **VACUUM**: Reclaims storage from dead rows created by updates/deletes (PostgreSQL uses MVCC)
- **autovacuum**: Background process that runs VACUUM automatically; can cause performance issues if misconfigured
- **Connection pooling**: PostgreSQL forks a process per connection — heavy connection counts are expensive. Use **PgBouncer** to pool connections.
- **EXPLAIN ANALYZE**: Shows actual query execution plan with timing. Essential for tuning.

```sql
EXPLAIN ANALYZE
SELECT * FROM claims
WHERE patient_id = 12345
  AND service_date >= '2024-01-01';
```

---

## 4. Observability & Performance Monitoring

### Why It Matters
The JD's opening paragraphs call out "observability, alerting, metrics" as core to how Aledade engineers work. This is cultural — not just a skill checkbox.

### The Three Pillars of Observability

**1. Logs**
- Record discrete events ("user X requested claim Y at timestamp Z")
- Structured logs (JSON) are better than plaintext — easier to query in Splunk/ELK
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL — use them correctly
- In healthcare: be careful never to log PHI in plaintext

**2. Metrics**
- Aggregated numerical measurements over time (e.g., requests/sec, query latency p95, pipeline row count)
- **Prometheus**: Scrapes metrics endpoints from services; stores as time-series
- **Grafana**: Visualizes Prometheus metrics in dashboards; supports alerting rules
- Common metric types: Counter (cumulative), Gauge (point-in-time), Histogram (distribution)

**3. Traces**
- Follow a single request through multiple services (distributed tracing)
- Tools: Jaeger, Zipkin, AWS X-Ray, OpenTelemetry
- Helps identify which service in a chain is causing latency

### Alerting Best Practices
- Alert on **symptoms**, not causes (e.g., "pipeline SLA missed" not "CPU high")
- Avoid alert fatigue — noisy alerts get ignored; tune thresholds carefully
- Use **runbooks**: documented steps for responding to each alert
- Key pipeline alerts: row count anomalies, processing time > SLA, error rate spike, data freshness (last updated > N hours ago)

### Splunk (You Have This on Your Resume)
- Log aggregation and search platform — used heavily in regulated industries
- SPL (Search Processing Language): `index=app_logs source=pipeline | stats count by status`
- Dashboards, saved searches, and alerts all configurable
- Be able to describe a time you used Splunk to diagnose a production issue

### Grafana (You Have This on Your Resume)
- Connects to Prometheus, CloudWatch, Splunk, and many other data sources
- Dashboards show real-time and historical metrics
- Can define alert rules that page on-call engineers

---

## 5. Data Ingestion at Scale

### Why It Matters
A preferred KSA in the JD. Healthcare companies ingest data from many sources: EHRs, claims clearinghouses, pharmacy systems, lab systems — all with different formats and cadences.

### Key Concepts

**Batch vs. Streaming**
- **Batch ingestion**: Process records in scheduled chunks (hourly, daily). Simpler, higher latency. Common for claims data.
- **Streaming ingestion**: Process records as they arrive (near real-time). More complex, lower latency. Common for clinical alerts.
- Most healthcare companies use batch for the majority of workflows.

**CDC (Change Data Capture)**
- Captures row-level changes (inserts, updates, deletes) from a source database's transaction log
- Avoids full-table scans for incremental loads
- Tools: Debezium (open source), AWS DMS, Fivetran
- Common in healthcare for syncing EHR data into analytics platforms

**Backpressure**
- When a consumer can't keep up with a producer, backpressure signals the producer to slow down
- Important in streaming systems to prevent queue overflow and data loss
- Handled differently by Kafka (consumer offset model), RabbitMQ (prefetch count), etc.

**Data Quality Checks on Ingestion**
- Row count validation (source vs. destination should match)
- Schema validation (reject malformed records early)
- Null checks on required fields
- Range checks (e.g., `service_date` can't be in the future)
- Duplicate detection (use composite keys or hash-based deduplication)

**Common Formats in Healthcare Ingestion**
- CSV/TSV: Claims files from clearinghouses
- JSON: API responses from modern EHR systems
- HL7 v2: Legacy pipe-delimited messages from older systems
- FHIR JSON/XML: Modern standard for health data exchange

---

## 6. Docker & Kubernetes (Backend Context)

### Why It Matters
You already have this experience — but in interviews, you'll need to frame it in a *backend service/data pipeline* context, not just DevOps/infrastructure.

### Key Concepts

**Docker**
- Packages an application and its dependencies into a portable image
- `Dockerfile`: Defines how to build the image
- Key commands: `docker build`, `docker run`, `docker ps`, `docker logs`, `docker exec`
- **Multi-stage builds**: Keep production images small by separating build and runtime layers
- For data pipelines: containerize ETL scripts so they run consistently in dev, staging, and prod

**Kubernetes (K8s)**
- Orchestrates containers at scale — handles scheduling, scaling, restarts, networking
- **Pod**: Smallest deployable unit (one or more containers)
- **Deployment**: Manages a set of identical pods; handles rolling updates
- **Service**: Stable network endpoint for a set of pods
- **CronJob**: Run a containerized task on a schedule — perfect for batch ETL pipelines
- **ConfigMap / Secret**: Inject configuration and credentials into pods at runtime
- **Health checks**: `livenessProbe` (restart if unhealthy), `readinessProbe` (remove from load balancer if not ready)

**Connecting to Databases in K8s**
- Use Secrets for DB credentials (never hardcode)
- Use connection pooling (PgBouncer sidecar) to manage connection limits
- Persistent volumes for stateful workloads (though databases typically run outside K8s in production)

---

## 7. CI/CD (Backend & Data Focus)

### Why It Matters
You have this experience — frame it around deploying *backend services and data pipelines*, which is what Aledade cares about.

### Key Concepts

**CI (Continuous Integration)**
- Every commit triggers automated tests and builds
- Goals: catch bugs early, maintain a always-deployable main branch
- Key practices: fast test suites, linting, type checking, test coverage gates

**CD (Continuous Deployment/Delivery)**
- **Continuous Delivery**: Every passing build is *ready* to deploy (manual trigger to prod)
- **Continuous Deployment**: Every passing build *automatically deploys* to prod
- Most healthcare companies use Continuous Delivery due to compliance requirements

**Pipeline Stages (Typical)**
1. Lint & type check
2. Unit tests
3. Integration tests (against test DB)
4. Build Docker image
5. Push to container registry
6. Deploy to staging
7. Run smoke tests
8. Deploy to production (manual gate or automatic)

**Safe Deployment Strategies**
- **Rolling deployment**: Replace old pods gradually with new ones — zero downtime
- **Blue/Green deployment**: Run old (blue) and new (green) environments in parallel; switch traffic atomically; easy rollback
- **Canary deployment**: Send a small % of traffic to new version, watch metrics, then ramp up
- **Feature flags**: Deploy code that's turned off; enable for specific users/segments without a new deploy

**Testing Strategies for Data Pipelines**
- Unit test transformation logic with sample data
- Integration test against a real (test) database
- Data contract tests: verify schema between producer and consumer
- Backfill testing: verify pipeline handles historical data correctly

---

## 8. Engineering Philosophy

### Why It Matters
Aledade's JD is unusually explicit about *how* they want engineers to think. This will come up in behavioral interviews.

### Core Principles

**"Writing new code is not always the solution"**
- First ask: can this be solved with configuration, existing tooling, or a process change?
- Over-engineering is a real failure mode
- Know when to reach for a library vs. building from scratch

**Minimize Risk**
- Prefer small, frequent releases over large, infrequent ones
- Each release should be independently reversible
- If something goes wrong, you want to know *which* small change caused it

**Observability First**
- Before shipping, ask: "How will I know if this is broken?"
- Add logging, metrics, and alerts as part of the feature — not as an afterthought
- "If it's not monitored, it doesn't exist in production"

**High Test Coverage**
- Not 100% for its own sake, but meaningful coverage of business logic
- Test the happy path, edge cases, and failure modes
- In healthcare: data correctness bugs have patient impact — test thoroughly

**Incremental Value**
- Ship the smallest version that provides real value
- Use feature flags to decouple deployment from release
- Get feedback early and iterate

**Trunk-Based Development**
- Everyone commits to `main` (or a short-lived branch); no long-running feature branches
- Requires strong CI discipline and feature flags
- Reduces merge conflicts and integration hell

---

## 9. Healthcare Domain Knowledge

### Why It Matters
This is your differentiator. Aledade is deeply embedded in value-based care — understanding their business makes you a stronger candidate in interviews and on the job.

### Key Concepts

**Value-Based Care vs. Fee-for-Service**
- **Fee-for-service**: Providers get paid per visit/procedure — incentive is volume
- **Value-based care**: Providers get paid based on patient *outcomes* and cost efficiency — incentive is quality
- Aledade helps independent physician practices succeed in value-based care contracts

**ACOs (Accountable Care Organizations)**
- Groups of providers (doctors, hospitals) that coordinate care for a population of patients
- Share in savings (and sometimes losses) against a benchmark cost
- Aledade manages ACOs — their software tracks quality metrics, cost of care, and care gaps

**Medicare Advantage**
- A private insurance alternative to traditional Medicare — patients choose a plan from an insurer
- Plans are paid a fixed amount per member per month (capitation) — insurer takes on risk
- Prior authorization is a major workflow (you have project experience here — leverage it)

**HIPAA & PHI**
- **PHI (Protected Health Information)**: Any individually identifiable health information
- 18 HIPAA identifiers include: name, DOB, SSN, address, medical record numbers, etc.
- Engineering implications: encrypt at rest and in transit, audit logging, access controls, minimum necessary principle
- Never log PHI; anonymize/pseudonymize for analytics workloads

**FHIR (Fast Healthcare Interoperability Resources)**
- The modern standard for exchanging healthcare data between systems
- Resources are structured JSON/XML objects: `Patient`, `Encounter`, `Claim`, `Observation`, `Condition`
- RESTful API: `GET /Patient/12345`, `POST /Observation`
- FHIR R4 is the current widely adopted version
- CMS mandates FHIR APIs for payer data exchange — Aledade almost certainly uses FHIR

**HL7 v2**
- Older pipe-delimited messaging standard, still ubiquitous in clinical systems
- Messages have segments: `MSH` (header), `PID` (patient), `OBR`/`OBX` (lab results), `DG1` (diagnosis)
- Example: `PID|1||12345^^^MRN||Doe^John^A||19800101|M`
- You'll likely encounter HL7 v2 feeds from hospital systems

**ICD-10 Codes**
- Standardized diagnosis codes (e.g., `E11.9` = Type 2 diabetes without complications)
- Used for billing, quality measurement, and clinical decision support
- Your Prior Authorization project used these — be ready to discuss

**CPT Codes**
- Standardized procedure codes used for billing (e.g., `99213` = office visit, established patient)
- Claims data is full of CPT codes — you'll query them frequently in a healthcare data role

---

## Q&A Section

### SQL & Databases

**Q: What's the difference between `WHERE` and `HAVING`?**
> `WHERE` filters rows *before* aggregation. `HAVING` filters groups *after* aggregation. Use `HAVING` when your filter references an aggregate function (e.g., `HAVING COUNT(*) > 5`).

**Q: How would you optimize a slow query joining three large tables?**
> First, run `EXPLAIN ANALYZE` to see the actual execution plan and find the bottleneck. Check if indexes exist on the join columns. Consider query structure — are you filtering early enough before the join? Look for implicit type casts breaking index usage. For very large tables, consider materializing intermediate results into a temp table, or restructuring with CTEs that filter down row counts before joining.

**Q: What is a covering index?**
> An index that contains all the columns a query needs, so the DB can answer the query from the index alone without reading the table. For example, if a query does `SELECT name, email FROM users WHERE id = 5`, an index on `(id, name, email)` covers it entirely.

**Q: Explain the difference between OLTP and OLAP databases.**
> **OLTP** (Online Transaction Processing) is optimized for high-volume, short, transactional queries — insert, update, delete single records. Highly normalized. **OLAP** (Online Analytical Processing) is optimized for complex analytical queries over large datasets — aggregations, scans across millions of rows. Often denormalized or columnar. In healthcare: the EHR is OLTP; the data warehouse is OLAP.

**Q: What is database normalization and when would you denormalize?**
> Normalization organizes data to reduce redundancy (1NF, 2NF, 3NF). Denormalization intentionally introduces redundancy for read performance — common in analytics/reporting where join cost at query time is too high. In healthcare data warehouses, you might store a flattened claims table so analysts don't have to join 6 tables every time.

---

### Data Pipelines & ETL

**Q: How do you handle a pipeline that partially fails halfway through?**
> Design for idempotency and use checkpointing. If I'm loading 1M records in batches of 10K, I track which batches completed. On restart, I skip completed batches. I use upserts rather than inserts so re-running a batch doesn't create duplicates. I also log failures to a dead-letter table for review.

**Q: What's the difference between idempotent and non-idempotent operations?**
> An idempotent operation produces the same result whether run once or many times. `INSERT ... ON CONFLICT DO UPDATE` is idempotent — re-running it updates existing records rather than duplicating them. A plain `INSERT` is not idempotent — re-running it creates duplicates.

**Q: How would you build a pipeline to ingest daily claims files from a health insurer?**
> I'd: (1) land raw files in S3 with a dated prefix, (2) validate schema and row counts against expected values, (3) parse and normalize into staging tables, (4) apply business rules and transformations, (5) upsert into the production claims table using claim ID as the key, (6) emit metrics (row counts, error rates, processing time) and alert if anything looks anomalous. Schedule in Airflow with retry logic and SLA alerts.

**Q: What is a DAG and why does it matter for pipeline orchestration?**
> A Directed Acyclic Graph defines tasks and their dependencies — which tasks must complete before others can start. "Acyclic" means no circular dependencies (task A can't depend on task B if B depends on A). In Airflow, pipelines are DAGs. This matters because it lets the orchestrator run independent tasks in parallel and only trigger dependent tasks when prerequisites finish.

---

### Database Internals

**Q: What is MVCC?**
> Multi-Version Concurrency Control. PostgreSQL keeps multiple versions of a row so readers never block writers and vice versa. When you update a row, the old version is retained until VACUUM reclaims it. This is why `VACUUM` is important — without it, dead row versions accumulate and bloat the table.

**Q: When would you use replication vs. sharding?**
> **Replication** (primary/replica) is for read scaling and high availability — you have one authoritative primary and copies that serve reads. Use this first. **Sharding** is for write scaling when a single primary can't handle write throughput. Sharding is complex — cross-shard queries are expensive and resharding is painful. Only shard when you've exhausted vertical scaling and replication options.

**Q: What happens if a replica falls behind the primary?**
> With asynchronous replication, the replica has **replication lag** — it's behind by some amount of time. Reads from the replica may return stale data. In healthcare, this matters: if a clinician's recent note isn't replicated yet, a query against the replica won't see it. Design read-sensitive workflows to query the primary, or check replication lag before routing reads.

**Q: What is connection pooling and why does it matter?**
> PostgreSQL forks a new OS process for each client connection — expensive in memory and CPU. Under high connection load (e.g., 500 app servers each with 10 connections), the database struggles. A connection pooler like PgBouncer sits in front of PostgreSQL and multiplexes many client connections onto fewer actual database connections. Essential for production backend services.

---

### Observability & Monitoring

**Q: How do you know if a data pipeline is healthy?**
> I monitor: (1) **data freshness** — was the last successful run within the expected window? (2) **row counts** — does today's volume match historical baselines? Sudden drops or spikes are signals. (3) **error rate** — what % of records failed to process? (4) **processing time** — is the pipeline meeting its SLA? I'd set alerts on all four with appropriate thresholds.

**Q: What's the difference between logging and metrics?**
> Logs capture discrete events with context ("record X failed due to null patient_id at 14:32:07"). Metrics are aggregated numerical measurements over time ("error rate: 2.3% over the last 5 minutes"). Logs help you diagnose *what* happened; metrics help you see *patterns* and set alerting thresholds.

**Q: What would you do if a production pipeline stopped producing output but wasn't throwing errors?**
> This is a silent failure — often harder to catch than noisy failures. I'd check: Is the scheduler triggering runs? (Airflow DAG paused? Cron silent?) Is the source data arriving? (Is the upstream feed empty or late?) Are records being filtered out silently? (Did a filter condition change?) This is exactly why data freshness alerts ("last successful load > 2 hours ago") are important — they catch silent failures that error-rate alerts miss.

---

### Engineering Philosophy

**Q: Describe a time you had to decide between building something new vs. using an existing solution.**
> Frame this around: what problem needed solving, what existing options you evaluated, what tradeoffs you considered (maintenance burden, fit to requirements, team expertise), and what you chose and why. Show that your default is to reach for existing tools and that you only build custom when there's a clear reason.

**Q: How do you approach deploying a risky database migration on a live system?**
> I'd: (1) test the migration on a staging environment with production-scale data, (2) take a backup immediately before, (3) use a blue/green approach or run the migration in a maintenance window if destructive, (4) for large tables, use online schema change tools (like `pg_repack` or `pt-online-schema-change`) that don't lock the table, (5) have a rollback script ready and tested, (6) monitor closely for 30 minutes after — watch query performance and error rates.

**Q: What does "incremental releases" mean to you?**
> Shipping small, focused changes frequently rather than large batches infrequently. Each release should be independently testable and reversible. I use feature flags to deploy code that's off by default, letting me merge early without exposing incomplete features to users. This reduces the blast radius of any single release and makes it easier to pinpoint regressions.

---

### Healthcare Domain

**Q: What is FHIR and why does it matter?**
> FHIR (Fast Healthcare Interoperability Resources) is the modern standard for exchanging health data between systems via RESTful APIs. It defines resource types like `Patient`, `Encounter`, `Claim`, and `Observation` in structured JSON/XML. It matters because healthcare data is historically siloed — FHIR enables interoperability. CMS mandates FHIR APIs, so any company working with Medicare data is likely consuming or producing FHIR.

**Q: How would you handle PHI in a data pipeline?**
> Minimize surface area: only access PHI when necessary, and only the specific fields required (minimum necessary principle). Encrypt at rest (AES-256) and in transit (TLS). Never log PHI — use patient IDs or anonymized tokens in logs. Implement access controls so only authorized services and people can read PHI. Audit log all access. For analytics, pseudonymize or aggregate data to remove direct identifiers where possible.

**Q: What is a prior authorization and why is it a data problem?**
> Prior authorization (PA) is a payer requirement that a provider get approval before performing certain procedures or prescribing certain drugs. It's a data problem because: PA rules are complex and constantly changing, encoded in lengthy policy documents; providers need to know which clinical criteria justify approval; and mismatches between what's submitted and what's required lead to denials that delay patient care. Automating PA requires ingesting policy documents, mapping clinical criteria to diagnosis/procedure codes, and surfacing the right checklist to the provider at the right time — exactly what your project does.

---

*Good luck, Ian. The healthcare domain knowledge you've built is a genuine edge — lean into it in every answer.*
