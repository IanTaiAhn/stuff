# Healthcare Data Study Guide
### Section 6 — Healthcare Data Context

> **Goal:** You don't need to be an expert. Being able to speak fluently to these concepts will make you stand out in interviews and on the job.

---

## 📋 Key Concepts

### 🏥 EHR — Electronic Health Records
- **What it is:** Structured clinical data stored by healthcare providers (hospitals, clinics, physician offices)
- **Common formats:** HL7 (older messaging standard), FHIR (modern, API-friendly standard)
- **What's in it:** Patient demographics, diagnoses, medications, lab results, visit notes, procedures
- **Why it matters:** Primary source of clinical truth; complex, often messy, requires normalization

---

### 💰 Claims Data
- **What it is:** Billing records submitted by providers to insurers for reimbursement
- **Key code types:**
  - **ICD-10** — Diagnosis codes (e.g., E11.9 = Type 2 diabetes without complications)
  - **CPT** — Current Procedural Terminology; codes for procedures and services performed
  - **Member IDs** — Links a claim to a specific insured individual
- **Why it matters:** Highly structured and comprehensive; used for cost analysis, utilization tracking, and population health

---

### 📊 HEDIS Measures
- **Full name:** Healthcare Effectiveness Data and Information Set
- **What it is:** Standardized quality metrics used to evaluate and compare health plans
- **Who uses it:** Health insurers, employers, regulators, and CMS (Centers for Medicare & Medicaid Services)
- **Example measures:**
  - Rates of preventive screenings (mammograms, colorectal cancer screening)
  - Medication adherence (e.g., for diabetes, hypertension)
  - Childhood immunization rates
- **Why it matters:** Drives quality improvement initiatives; plans are publicly ranked on HEDIS scores

---

### ⚖️ Medicare Risk Adjustment
- **What it is:** A model that adjusts payments to insurers based on the predicted health costs of their enrolled members
- **The logic:** Sicker members cost more to cover → insurers get higher payments for them → prevents insurers from cherry-picking healthy members
- **Key mechanism:** **HCC codes** (Hierarchical Condition Categories) — derived from ICD-10 diagnosis codes; each HCC maps to a risk score
- **Data source:** Claims and EHR diagnosis data are used to assign HCC codes annually
- **Why it matters:** Directly ties data quality to revenue; inaccurate or incomplete diagnosis coding = underpayment

---

## 💬 What to Say If Asked

You don't need prior healthcare experience. A strong answer sounds like:

> *"I haven't worked directly with HEDIS or risk adjustment data, but I've picked up new data domains quickly in past roles — I'd lean on documentation, SMEs on the team, and existing data dictionaries to get up to speed fast."*

**Why this works:**
- Honest and self-aware
- Demonstrates a concrete learning strategy
- Shows confidence without overclaiming

---

## 🔗 How These Concepts Connect

```
EHR / Claims Data
       ↓
  Diagnosis Codes (ICD-10)
       ↓
  ┌────────────────────────────────────┐
  │  HEDIS Measures   │  HCC Codes     │
  │  (quality)        │  (risk scores) │
  └────────────────────────────────────┘
       ↓                      ↓
  Plan quality rankings   Risk-adjusted payments
  (public reporting)      (Medicare Advantage)
```

---

## 📝 Quick Reference Glossary

| Term | Stands For | One-Line Definition |
|------|-----------|---------------------|
| EHR | Electronic Health Record | Digital clinical record kept by a provider |
| HL7 | Health Level 7 | Legacy healthcare data messaging standard |
| FHIR | Fast Healthcare Interoperability Resources | Modern API-based health data standard |
| ICD-10 | International Classification of Diseases, 10th Revision | Standardized diagnosis codes |
| CPT | Current Procedural Terminology | Codes for medical procedures/services |
| HEDIS | Healthcare Effectiveness Data and Information Set | Standardized health plan quality metrics |
| HCC | Hierarchical Condition Category | Risk score categories used in Medicare |
| CMS | Centers for Medicare & Medicaid Services | Federal agency overseeing Medicare/Medicaid |
| SME | Subject Matter Expert | Internal expert to consult when learning a domain |

---

*Study tip: Focus on understanding the **purpose** of each concept (what problem it solves) rather than memorizing details. That's what interviewers are really testing.*
