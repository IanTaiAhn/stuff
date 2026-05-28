# Study Guide — Azure Ecosystem (Section 5)

> **Goal:** You don't need deep expertise. Focus on *what each service does*, *how they connect to each other*, and *where they fit in a typical data pipeline*.

---

## 🗺️ The Big Picture

These five services together form a complete cloud data platform. A typical data flow looks like this:

```
Raw Data Sources
      ↓
Azure Data Factory (ADF)      ← orchestrates movement & transformation
      ↓
Azure Data Lake Storage (ADLS) ← stores raw and processed data
      ↓
Azure Databricks / Synapse     ← transforms, analyzes, and models the data
      ↓
Delta Lake (on ADLS)           ← adds reliability (ACID) to the storage layer
      ↓
Consumers (dashboards, ML models, reports)
```

---

## 📦 Service-by-Service Breakdown

### 1. Azure Data Factory (ADF)
**Role in the stack:** Orchestration layer — the "control plane"

- Builds and schedules **pipelines** to move and transform data
- Uses **linked services** to connect to external sources (databases, APIs, storage accounts)
- **Triggers** kick off pipelines on a schedule, on an event, or manually
- Think of it as the glue that connects everything else together

**Key concepts to know:**
- Pipeline → a workflow of activities
- Linked Service → a connection string to a data source or destination
- Dataset → a reference to the data within a linked service
- Trigger → what causes a pipeline to run (schedule, tumbling window, event-based)

---

### 2. Azure Data Lake Storage (ADLS)
**Role in the stack:** Central storage — the "data at rest" layer

- Cloud object storage built for large-scale analytics workloads
- Organized in **tiers** (hot, cool, archive) to balance cost vs. access speed
- Hierarchical namespace enables folder-like structure (unlike flat blob storage)
- Commonly the landing zone for raw ingested data and the output of transformations

**Key concepts to know:**
- Gen2 is the current version (built on Azure Blob Storage)
- Supports fine-grained access control via ACLs
- Works natively with Databricks, Synapse, and ADF

---

### 3. Azure Databricks
**Role in the stack:** Compute layer for large-scale processing and ML

- Managed **Apache Spark** platform — distributed compute for big data
- Supports Python (PySpark), Scala, SQL, and R
- Used for ETL/ELT pipelines, feature engineering, and training ML models
- Collaborative notebooks make it accessible for both engineers and data scientists

**Key concepts to know:**
- Cluster → a pool of VMs that runs Spark jobs
- Notebook → interactive compute environment (like Jupyter, but collaborative)
- Job → a scheduled or triggered run of a notebook or script
- Unity Catalog → governance layer for data access control
- Integrates tightly with ADLS and Delta Lake

---

### 4. Azure Synapse Analytics
**Role in the stack:** Unified analytics workspace — warehouse + big data in one

- Combines a **dedicated SQL pool** (data warehouse) with **serverless SQL** and Spark
- Designed for structured analytical queries at scale (think: business reporting, BI)
- Built-in integration with ADF-style pipelines, Power BI, and ADLS
- Synapse vs. Databricks: Synapse leans toward SQL/BI workloads; Databricks leans toward engineering and ML

**Key concepts to know:**
- Dedicated SQL Pool → provisioned data warehouse (replaces Azure SQL DW)
- Serverless SQL Pool → query data in ADLS without a dedicated cluster (pay per query)
- Apache Spark Pool → Spark compute inside Synapse
- Synapse Link → connects to Cosmos DB for real-time analytics

---

### 5. Delta Lake
**Role in the stack:** Reliability layer on top of ADLS

- Open-source storage format that adds **ACID transactions** to data lake files
- Solves the classic data lake problem: files can be corrupted or inconsistent under concurrent writes
- Stores data as **Parquet files** + a **transaction log** that tracks every change
- Enables features like: time travel, schema enforcement, upserts (MERGE)

**Key concepts to know:**
- ACID = Atomicity, Consistency, Isolation, Durability
- Time Travel → query data as it existed at a past point in time
- Schema enforcement → prevents bad data from being written
- Delta table → a directory on ADLS with Parquet files + `_delta_log/`
- Native to Databricks but also supported in Synapse and open-source Spark

---

## 🔗 How the Services Connect

| From | To | How |
|---|---|---|
| ADF | ADLS | Reads/writes files via linked service |
| ADF | Databricks | Triggers notebooks/jobs as pipeline activities |
| ADF | Synapse | Triggers SQL scripts or Spark jobs |
| Databricks | ADLS | Reads/writes directly via storage mount or credential |
| Databricks | Delta Lake | Delta is the default table format in Databricks |
| Synapse | ADLS | Serverless SQL queries files directly |
| Delta Lake | ADLS | Delta tables *are* files on ADLS + a transaction log |

---

## ✅ Quick-Reference Cheat Sheet

| Service | One-liner | Key buzzwords |
|---|---|---|
| **ADF** | Orchestrates data movement | Pipelines, linked services, triggers |
| **ADLS** | Cloud storage for analytics | Data lake, tiers, Gen2, hierarchical namespace |
| **Databricks** | Spark platform for big data + ML | Clusters, notebooks, PySpark, Unity Catalog |
| **Synapse** | SQL warehouse + analytics workspace | Dedicated pool, serverless SQL, BI-ready |
| **Delta Lake** | ACID transactions on a data lake | Parquet + transaction log, time travel, MERGE |

---

## 🧠 Study Questions

1. What problem does Delta Lake solve that plain ADLS does not?
2. When would you choose Synapse over Databricks (and vice versa)?
3. What is a "linked service" in ADF and why does it exist?
4. How does ADF interact with Databricks in a production pipeline?
5. What does "serverless SQL pool" in Synapse mean — what are you *not* paying for?
6. Describe a simple end-to-end pipeline using at least three of these services.

---

## 📚 Resource

- [Microsoft Learn — Azure Data Engineer Path](https://learn.microsoft.com/en-us/training/paths/data-engineer-azure/)
  *Free, ~8–10 hours total. Skim the modules most relevant to the job description.*
