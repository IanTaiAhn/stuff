
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