
## New Projects baby!
🔴 Tier 1 — Do These First (Highest Signal, Broadest Coverage)
Project 1: FHIR R4 Ingestion & Clinical Data Pipeline
This is the single most important project you can build. FHIR is the universal language of modern healthtech and almost every company on your list speaks it.
What to build:

Use Synthea (open source) to generate synthetic patient populations
Ingest FHIR R4 bundles (Patient, Condition, Observation, MedicationRequest, Claim, Encounter resources)
Normalize and store in PostgreSQL or Snowflake
Build a dbt transformation layer on top
Expose a lightweight FastAPI layer for querying

Why it works: It hits FHIR literacy, dbt/Snowflake (your existing stack), data modeling, and pipeline engineering all in one project. Health Catalyst, Innovaccer, Arcadia, and Waystar will all recognize this as real work immediately.
Stack: Python, Synthea, dbt, Snowflake or PostgreSQL, FastAPI, Docker

Project 2: CMS-HCC Risk Score Engine
HCC (Hierarchical Condition Category) risk adjustment is how Medicare Advantage plans get paid. Every payer on your list — Optum, CVS, Humana, Elevance — lives and dies by this model.
What to build:

Pull CMS's publicly available HCC mapping tables (ICD-10 → HCC category crosswalk)
Build a scoring pipeline against synthetic patient data from your FHIR project above
Calculate risk scores, flag high-risk members, surface a simple dashboard
Bonus: add a simple SHAP or feature importance layer to explain which diagnoses drive scores highest

Why it works: This shows you understand how payers make money, not just how to write code. That business domain awareness is rare at the engineer level and gets noticed.
Stack: Python, pandas, Snowflake/dbt (reuse from Project 1), Streamlit or React for dashboard

🟡 Tier 2 — Build These Next (Domain Depth + Differentiation)
Project 3: HEDIS Quality Measure Engine
HEDIS measures are how health plans and health systems are graded on care quality. Every analytics company you're targeting either sells HEDIS reporting or consumes it.
What to build:

Pick 2–3 measures: Diabetes HbA1c Testing (CDC), Breast Cancer Screening (BCS), Medication Adherence for Cholesterol (MAC) are good starters
Implement denominator and numerator logic against your synthetic patient dataset
Build it as a dbt project with documented models — this is exactly how it's done in production
Output a simple quality report / compliance dashboard

Why it works: Health Catalyst, Arcadia, and Cotiviti literally sell this as a product. Showing you've hand-rolled the logic signals deep domain understanding.
Stack: dbt, Snowflake/PostgreSQL, Python, Streamlit

Project 4: Clinical NLP — ICD-10 Auto-Coder / Note Summarizer
You already have the foundation in your Prior Auth project with Groq. Extend it or build separately.
What to build:

Feed synthetic clinical notes (you can generate these with an LLM or use i2b2 public datasets)
Use an LLM (Groq, OpenAI, or a local model via Ollama) to extract diagnoses, procedures, and suggest ICD-10/CPT codes
Add a human-review interface where a "coder" can accept/reject/override suggestions
Track precision/recall of the model's suggestions vs. ground truth

Why it works: Episource, Veradigm, and Change Healthcare pay enormous amounts for this capability. You already have the LLM integration pattern — this is a natural, high-value extension of work you've already done.
Stack: Python, FastAPI, Groq or OpenAI API, React (your existing frontend skills), PostgreSQL

🟢 Tier 3 — High Differentiation if You Have Time
Project 5: SMART on FHIR App (Epic Sandbox)
What to build:

Register for Epic's free developer sandbox at fhir.epic.com
Build a minimal SMART on FHIR OAuth app that launches from within a (simulated) EHR context
Pull patient context (demographics, active medications, recent encounters) and surface a simple clinical decision support alert

Why it works: Most software engineers have never touched an EHR integration. This is a concrete differentiator for Cleveland Clinic, Mount Sinai, Kaiser, and Intermountain — and it signals you're serious about the clinical workflow layer, not just the data layer.
Stack: React or Next.js, SMART on FHIR OAuth, Epic sandbox APIs

Project 6: EDI 837/835 Claims Parser
What to build:

Write a parser for X12 EDI 837P (professional claims) and 835 (remittance/EOB) files
Normalize the parsed data into a relational schema
Build a simple denial analysis dashboard — which payers deny most, which CPT codes, what denial reason codes

Why it works: EDI transaction literacy is extremely niche and extremely valued at Waystar, Change Healthcare, and any revenue cycle company. Very few engineers have ever actually parsed an 837 file — if you have, you're immediately more credible than 90% of applicants.
Stack: Python, custom parser or x12 library, PostgreSQL, Streamlit

⚪ Tier 4 — Nice Polish, Low Effort
Project 7: OMOP CDM Conversion
Take your FHIR synthetic data and convert it into the OMOP Common Data Model (used by most academic medical centers and research networks). Adds one more vocabulary to your profile and signals research/clinical informatics awareness. The OHDSI community has good tooling for this (ETL-Synthea).

Months 1–2: FHIR R4 pipeline (foundational, everything else builds on it)
Month 3: HCC Risk Score Engine (reuses FHIR data, adds payer domain layer)
Month 4: HEDIS Measure Engine (extends dbt models from Project 1)
Month 5: Clinical NLP ICD-10 coder (extends your existing Prior Auth project)
Month 6: SMART on FHIR app or EDI parser depending on which companies you're targeting most

🥇Health CatalystLocal HQ, exact domain match, dbt/Snowflake stack
🥈WaystarLocal, revenue cycle = your prior auth background
🥉Intermountain HealthLocal, massive data org, stable
4RecursionAI/ML ceiling is exceptional, SLC HQ
5Innovaccer (remote)FHIR-first, population health, fast growth
6Myriad GeneticsLocal, precision medicine, strong pay
7U of U HealthStable, clinical data depth, familiar environment

## Interview Prep for Data Engineering and adjacent AI/ML stuff
What You Need to Know Cold
Break this into four buckets:

### 1. SQL — Must Be Sharp
This is non-negotiable. Every data engineering role will test SQL, and healthtech schemas are complex with many joins. You need to be fluent in:

Window functions (ROW_NUMBER, RANK, LAG, LEAD, PARTITION BY)
CTEs, including recursive CTEs
Aggregations with HAVING, GROUP BY on multi-table joins
Date/time arithmetic (claim dates, enrollment periods, gap-in-care logic)
Self joins (hierarchical data like HCC parent/child categories)
Handling NULLs correctly — this comes up constantly in claims data

Practice resource: StrataScratch has healthcare-flavored SQL problems. Mode Analytics and LeetCode's database section are also solid. Aim to do 2–3 problems a day for a few weeks.

### 2. Python Data Engineering — Comfortable, Not Expert
You already have this from your resume, but be ready to write clean, working Python from scratch for:

Reading, parsing, and transforming JSON (FHIR bundles are JSON)
pandas operations — filtering, merging, groupby, reshaping
Writing a basic ETL function — extract from source, transform, load to a target
Error handling and logging patterns in a pipeline context
Basic OOP — a clean class structure for a pipeline or parser

### 3. System Design — Health Data Flavor
For senior-leaning roles they'll ask you to design something. You don't need to know everything, but you should be able to reason through:

How would you design a pipeline that ingests FHIR data from 10 different hospital systems daily?
How would you design a member risk stratification system that updates monthly?
How would you ensure HIPAA compliance in a cloud data pipeline?

The framework they want to see: data sources → ingestion layer → storage/schema design → transformation → serving layer → monitoring. Being able to draw and talk through that coherently is the bar, not memorizing every AWS service.

### 4. Domain Vocabulary — Know These Cold
This is the part most software engineers skip and it's what separates you at healthtech companies specifically. You should be able to define and discuss these without hesitation:

FHIR R4 — what it is, key resources (Patient, Encounter, Condition, Observation, Claim), what a Bundle is
ICD-10 vs. CPT — what each codes for and when each is used
HCC / Risk Adjustment — the basic concept of how CMS-HCC scoring works
Prior Authorization — the workflow, why denials happen, what an LCD is (you already have this)
HIPAA / PHI — what counts as PHI, the 18 identifiers, de-identification standards (Safe Harbor vs. Expert Determination)
837/835 EDI — what they are at a high level, even if you haven't built a parser yet
HEDIS — what it measures and why payers care
HL7 v2 vs. FHIR — why the industry is migrating and what the difference is

#### Should You Do LeetCode?
Yes, but don't make it your primary focus. Here's the realistic breakdown:
For Health Catalyst, Waystar, Intermountain, U of U Health — LeetCode-style algorithmic questions are unlikely. Maybe one easy/medium problem to assess basic coding ability, but they're not going to ask you to implement Dijkstra's algorithm.
For Recursion — more likely to have a real algorithms/data structures round given their engineering culture. Medium LeetCode difficulty is a reasonable bar to aim for.
For Innovaccer, Arcadia — somewhere in between. More likely a domain-relevant coding problem than pure algorithms.
Practical LeetCode strategy for your profile:

Be solid on Easy problems across the board — no reason to stumble on these
Be comfortable with Medium problems in: arrays/strings, hashmaps, SQL, and basic tree traversal
Don't stress Hard problems for this job tier — that's FAANG prep, not healthtech prep
Spend no more than 30% of your prep time here — SQL and domain knowledge will move the needle more



# Health Data Engineering — Interview Study Guide

---

## Section 1: SQL — Must Be Sharp

### Key Concepts

**Window Functions**
Used to perform calculations across a set of rows related to the current row, without collapsing rows the way `GROUP BY` does.

- `ROW_NUMBER()` — assigns a unique sequential integer per row within a partition
- `RANK()` — like ROW_NUMBER but ties get the same rank, with gaps after
- `LAG(col, n)` / `LEAD(col, n)` — access a value n rows behind or ahead in the window
- `PARTITION BY` — splits the window into groups (like a GROUP BY that doesn't collapse)

**CTEs (Common Table Expressions)**
Named subqueries defined with `WITH` that make complex queries readable. Recursive CTEs let a query reference itself, useful for traversing hierarchical data (e.g., HCC parent/child categories).

**Aggregations**
- `GROUP BY` collapses rows into groups; combine with `JOIN`s carefully — aggregating before or after a join changes results
- `HAVING` filters on aggregated values (use it instead of `WHERE` when filtering on `SUM`, `COUNT`, etc.)

**Date/Time Arithmetic**
Critical in claims data: calculating enrollment gaps, days between service and claim submission, identifying care gaps. Know `DATEDIFF`, `DATE_ADD`, `INTERVAL`, and how your database handles NULL dates.

**Self Joins**
Joining a table to itself — used for hierarchical structures like HCC categories where a row references a parent in the same table.

**NULL Handling**
`NULL` is not zero and is not empty string. `NULL = NULL` is false. Use `IS NULL`, `IS NOT NULL`, `COALESCE(col, default)`, and `NULLIF(a, b)`. In claims data, a NULL claim amount is very different from a $0 claim.

---

### Practice Questions

**Q1:** You have a `claims` table with columns `member_id`, `claim_date`, `claim_amount`, and `claim_status`. Write a query that returns each member's most recent claim, along with the dollar difference between their most recent and second most recent claim.

<details>
<summary>Answer</summary>

```sql
WITH ranked_claims AS (
  SELECT
    member_id,
    claim_date,
    claim_amount,
    ROW_NUMBER() OVER (PARTITION BY member_id ORDER BY claim_date DESC) AS rn,
    LAG(claim_amount) OVER (PARTITION BY member_id ORDER BY claim_date DESC) AS prev_claim_amount
  FROM claims
)
SELECT
  member_id,
  claim_date,
  claim_amount,
  claim_amount - prev_claim_amount AS amount_diff
FROM ranked_claims
WHERE rn = 1;
```

`ROW_NUMBER()` with `PARTITION BY member_id` gives each member their own numbering. `LAG` looks at the previous row within that same partition — the second most recent claim. Filtering `WHERE rn = 1` returns only the most recent row per member.

</details>

---

**Q2:** You have an `enrollments` table with `member_id`, `enrollment_start`, and `enrollment_end`. Find all members who had a gap in coverage of more than 30 days at any point.

<details>
<summary>Answer</summary>

```sql
WITH ordered_enrollment AS (
  SELECT
    member_id,
    enrollment_start,
    enrollment_end,
    LEAD(enrollment_start) OVER (PARTITION BY member_id ORDER BY enrollment_start) AS next_start
  FROM enrollments
)
SELECT
  member_id,
  enrollment_end AS gap_start,
  next_start AS gap_end,
  DATEDIFF(next_start, enrollment_end) AS gap_days
FROM ordered_enrollment
WHERE DATEDIFF(next_start, enrollment_end) > 30;
```

`LEAD` peeks at the next enrollment period's start date for the same member. The gap is the time between when the current period ended and the next one began. A NULL `next_start` means no subsequent enrollment — handle that based on your business logic (e.g., treat as an open-ended gap or exclude).

</details>

---

## Section 2: Python Data Engineering

### Key Concepts

**JSON Parsing**
FHIR data arrives as JSON bundles. Know `json.loads()` for strings and `json.load()` for file objects. FHIR bundles nest deeply — practice extracting fields from nested dicts and lists defensively (use `.get()` to avoid `KeyError`).

**pandas Operations**
- Filtering: `df[df['col'] == value]` or `df.query()`
- Merging: `pd.merge(left, right, on='key', how='left')` — know when to use left/inner/outer
- `groupby` + `agg`: collapse rows and compute multiple aggregates at once
- `pivot_table` / `melt`: reshape between wide and long format

**ETL Function Pattern**
A basic pipeline has three stages: extract data from a source, transform it (clean, filter, reshape, join), and load it to a destination. Each stage should be its own function for testability.

**Error Handling and Logging**
Use `try/except` blocks around I/O and parsing operations. Use Python's `logging` module (not `print`) in pipeline code — it gives you severity levels and timestamps. Log both successes and failures with context (e.g., which file or record failed).

**Basic OOP for Pipelines**
A pipeline class should encapsulate its configuration and expose a `run()` method. Each logical unit (a FHIR parser, a database loader) should be its own class with a clear interface.

---

### Practice Questions

**Q1:** Write a function that takes a FHIR Patient bundle (as a Python dict) and returns a flat dict with `patient_id`, `birth_date`, `gender`, and the patient's first given name. Handle missing fields gracefully.

<details>
<summary>Answer</summary>

```python
import logging

logger = logging.getLogger(__name__)

def extract_patient_fields(bundle: dict) -> dict | None:
    try:
        entries = bundle.get("entry", [])
        patient_resource = next(
            (e["resource"] for e in entries
             if e.get("resource", {}).get("resourceType") == "Patient"),
            None
        )
        if not patient_resource:
            logger.warning("No Patient resource found in bundle")
            return None

        name_list = patient_resource.get("name", [])
        given_names = name_list[0].get("given", []) if name_list else []
        first_name = given_names[0] if given_names else None

        return {
            "patient_id": patient_resource.get("id"),
            "birth_date": patient_resource.get("birthDate"),
            "gender": patient_resource.get("gender"),
            "first_given_name": first_name,
        }
    except (KeyError, TypeError, StopIteration) as e:
        logger.error(f"Failed to parse patient bundle: {e}")
        return None
```

Notice the use of `.get()` at every level to avoid `KeyError` on missing fields. Logging with `logger.warning` and `logger.error` (not `print`) is correct pipeline practice. The function returns `None` on failure rather than raising, which keeps a batch pipeline running even if one record is malformed.

</details>

---

**Q2:** Given a pandas DataFrame with columns `member_id`, `diagnosis_code`, and `service_date`, write code to find the most recent service date per member for each unique diagnosis code, then reshape the result so each row is a member and each column is a diagnosis code containing the latest service date (or NaN if they never had that code).

<details>
<summary>Answer</summary>

```python
import pandas as pd

# Sample data
df = pd.DataFrame({
    "member_id": [1, 1, 1, 2, 2],
    "diagnosis_code": ["E11", "I10", "E11", "I10", "E11"],
    "service_date": pd.to_datetime(["2024-01-01", "2024-03-01", "2024-06-01",
                                    "2024-02-01", "2024-04-01"])
})

# Get most recent date per member + diagnosis combo
latest = (
    df.groupby(["member_id", "diagnosis_code"])["service_date"]
    .max()
    .reset_index()
)

# Pivot so each diagnosis code becomes a column
result = latest.pivot_table(
    index="member_id",
    columns="diagnosis_code",
    values="service_date",
    aggfunc="max"
)

print(result)
```

`groupby` + `max()` finds the latest date per combination. `pivot_table` reshapes from long to wide format. Cells for codes a member never had will be `NaT` (the datetime equivalent of `NaN`). This wide format is common for building member-level feature matrices in risk stratification.

</details>

---

## Section 3: System Design — Health Data Flavor

### Key Concepts

**The Standard Framework**
When asked to design a health data pipeline, walk through these layers in order:

1. **Data sources** — What systems are sending data? (EHRs, claims clearinghouses, labs) What format? (FHIR, HL7 v2, 837 EDI, flat files)
2. **Ingestion layer** — How does data arrive? (API polling, SFTP drop, event stream) How do you handle late arrivals and duplicates?
3. **Storage / schema design** — Raw landing zone (store as-is), then a transformed layer. Think about partitioning (by date, by member) for query efficiency.
4. **Transformation** — Parsing, normalization, deduplication, enrichment (e.g., mapping ICD-10 codes to HCC categories)
5. **Serving layer** — Who queries this? A BI tool? An ML model? An operational dashboard? This drives the schema design.
6. **Monitoring** — Row count checks, schema drift alerts, SLA tracking, data quality rules (e.g., flag claims with no diagnosis code)

**HIPAA Compliance in the Cloud**
- Encryption at rest and in transit (TLS, KMS)
- Access controls — least privilege, role-based access, audit logging
- PHI never in logs or error messages
- Business Associate Agreements (BAAs) with all cloud vendors
- De-identification before sharing data downstream if the use case allows it

**Key Design Tradeoffs to Mention**
- Batch vs. streaming — monthly risk scores don't need real-time; claims fraud detection might
- Schema-on-read vs. schema-on-write — a raw JSON landing zone gives you flexibility; a rigid schema gives you reliability
- Idempotency — your pipeline should produce the same result if run twice on the same data

---

### Practice Questions

**Q1:** Walk through how you would design a pipeline to ingest FHIR data from 10 different hospital systems and make it available for downstream analytics.

<details>
<summary>Answer</summary>

**Sources:** 10 hospital EHR systems, each sending FHIR R4 bundles via REST API or SFTP on a daily schedule. Each system may use slightly different profiles/extensions.

**Ingestion:** An orchestrator (e.g., Airflow) triggers a daily pull per hospital. Raw FHIR bundles are written as-is to a raw storage bucket (e.g., S3 or GCS), partitioned by `hospital_id` and `ingestion_date`. This preserves the original data and decouples ingestion from parsing failures.

**Transformation:** A parsing job extracts resources (Patient, Encounter, Condition, Observation) from each bundle and writes structured records to a staging schema. Deduplication logic handles the same patient appearing across multiple hospital feeds using a master patient index (MPI) or matching on demographics + identifiers.

**Storage:** A normalized analytical schema with one table per resource type. Partitioned by date and indexed on `member_id` and `encounter_id` for fast joins.

**Serving:** Exposed to BI tools via a curated mart layer. ML pipelines access the normalized tables directly.

**Monitoring:** Row count checks per hospital per day, schema validation on incoming bundles, alerting if a hospital's feed goes silent, and PHI audit logging on all access.

**HIPAA:** PHI stays within the secure environment. De-identified views are published for research. All storage encrypted, all access logged, BAAs in place with cloud provider.

</details>

---

**Q2:** A stakeholder asks why you'd store raw FHIR JSON before parsing it, since it takes up more space. How do you respond?

<details>
<summary>Answer</summary>

The raw landing zone is your safety net. If a parsing bug silently drops fields, or business requirements change and you need a new field you didn't extract originally, the raw data lets you re-derive the correct output without going back to the source system. Source systems have retention limits, APIs go down, and EHR vendors change data formats — your raw archive is the authoritative record of what you actually received. The storage cost is almost always worth it compared to the operational cost of re-ingesting from a hospital's EHR system. You can also tier raw storage to cheaper cold storage after a defined period to control costs.

</details>

---

## Section 4: Domain Vocabulary

### Key Concepts

**FHIR R4 (Fast Healthcare Interoperability Resources)**
A modern HL7 standard for exchanging healthcare data via REST APIs using JSON or XML. A **Bundle** is a container that holds multiple resources together. Key resources:
- `Patient` — demographics
- `Encounter` — a visit or episode of care
- `Condition` — a diagnosis
- `Observation` — a measurement (labs, vitals)
- `Claim` — a bill submitted to a payer

**ICD-10 vs. CPT**
- **ICD-10** (International Classification of Diseases, 10th revision) — codes *diagnoses* and *reasons for a visit*. Used by providers and payers. Example: `E11.9` = Type 2 diabetes without complications.
- **CPT** (Current Procedural Terminology) — codes *procedures and services* performed. Used for billing. Example: `99213` = office visit, established patient, moderate complexity.

**HCC / Risk Adjustment**
Hierarchical Condition Categories (HCCs) are CMS's system for predicting a Medicare Advantage member's expected healthcare costs. Diagnosis codes (ICD-10) map to HCC categories. A member's HCC score (RAF score) is used to adjust payments to health plans — sicker members have higher scores, so plans receive more funding to care for them.

**Prior Authorization**
A payer's requirement that a provider get approval *before* delivering certain services or medications. Denials happen when the service isn't covered, documentation is insufficient, or a cheaper alternative wasn't tried first. An **LCD** (Local Coverage Determination) is a Medicare contractor's decision about whether a specific service is covered in a geographic area.

**HIPAA (Health Insurance Portability) and Accountability Act/ PHI (Protected Health Information)**
- **PHI** (Protected Health Information) — any health information linked to an individual
- The **18 identifiers** that make data PHI include: name, address, dates (birth, death, admission), phone, SSN, MRN, and more
- **De-identification methods**: Safe Harbor (remove all 18 identifiers) vs. Expert Determination (a statistician certifies the re-identification risk is very small)

**837 / 835 EDI**
HIPAA-standard electronic transaction formats:
- **837** — the electronic claim submitted from a provider to a payer (837P for professional, 837I for institutional)
- **835** — the payment remittance advice sent from a payer back to a provider, explaining what was paid and why

**HEDIS (Healthcare Effectiveness Data and Information Set)**
A set of standardized performance measures developed by NCQA that payers use to evaluate quality of care. Examples: mammography rates, blood sugar control in diabetics, medication adherence. Payers are publicly rated on HEDIS scores, which affects Star Ratings and revenue.

**HL7 v2 vs. FHIR**
- **HL7 v2** — (Health Level Seven) a legacy pipe-delimited message format from the 1980s–90s. Widely deployed but brittle, inconsistently implemented, and hard to parse.
- **FHIR** — (Fast Healthcare Interoperability Resources) modern, REST-based, JSON/XML, with well-defined resource schemas and a public API standard. The industry is migrating because FHIR is interoperable across systems, developer-friendly, and mandated by CMS regulations (21st Century Cures Act).

---

### Practice Questions

**Q1:** An interviewer asks: "We receive 837 transaction files from provider groups daily. Walk me through what's in one of those files and what we'd do with it." How do you answer?

<details>
<summary>Answer</summary>

An 837 is the electronic claim a provider submits to a payer for reimbursement. It contains the member's ID, the provider's NPI, the dates of service, the diagnosis codes (ICD-10), and the procedure codes (CPT/HCPCS) with billed amounts. The 837P variant covers professional (outpatient) claims; 837I covers institutional (hospital) claims.

On receipt, you'd parse the EDI format into structured records and load them into a claims processing table. From there, you'd run adjudication logic — checking eligibility, verifying coverage, applying prior authorization rules, and determining the allowed amount. The output is an 835 remittance file sent back to the provider explaining the payment or denial. For analytics use cases, the parsed 837 data feeds cost analysis, utilization management, HEDIS measure calculation, and HCC risk scoring.

</details>

---

**Q2:** What's the difference between Safe Harbor and Expert Determination de-identification, and when would you use each?

<details>
<summary>Answer</summary>

Both are HIPAA-recognized methods for creating de-identified data that is no longer considered PHI and can be shared more freely.

**Safe Harbor** is prescriptive: you remove all 18 specific identifiers (name, zip codes below 3 digits, dates more specific than year for patients over 89, etc.) and have no actual knowledge that the remaining data could re-identify someone. It's straightforward to implement and audit — you follow a checklist. It's the right choice when you need a simple, defensible process and your data doesn't require date-level precision.

**Expert Determination** is flexible: a qualified statistician applies generally accepted principles to certify that the risk of re-identification is very small. This allows retaining data elements Safe Harbor would strip (like more precise zip codes or service dates), as long as the expert concludes the re-identification risk is acceptably low. It's the right choice when date granularity matters for your use case — for example, longitudinal research that needs to track a patient's care sequence over time.

In practice: Safe Harbor for most operational data sharing; Expert Determination for research datasets where the stripped data would lose analytical value.

</details>