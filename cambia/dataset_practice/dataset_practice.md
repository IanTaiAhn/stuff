## Place to dump notes for the machine leanring practice with medical jargon.

This file is about 21gb and it has 1 million patient records.
Mess around with it.
https://synthea.mitre.org/downloads

Found a dataset from this website...


This website yielded this dataset:
https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files/cms-2008-2010-data-entrepreneurs-synthetic-public-use-file-de-synpuf


### DE1_0_2008_Beneficiary_Summary_File_Sample_11 columns:
* Demographics
* Geography
* Coverage (insurance months)
* Chronic condition flags
* Annual spending (IP/OP/Carrier)

### 🧬 1. Demographics
Column	Meaning
* DESYNPUF_ID	Synthetic unique member ID
* BENE_BIRTH_DT	Birthdate (YYYYMMDD)
* BENE_DEATH_DT	Death date (if any)
* BENE_SEX_IDENT_CD	Sex: 1 = Male, 2 = Female
* BENE_RACE_CD	Race code (CMS categories)
* BENE_ESRD_IND	End‑Stage Renal Disease indicator (0 = No, 1 = Yes)
Example:
* 19370501 → born May 1, 1937
* BENE_DEATH_DT blank → still alive in the synthetic dataset

### 🗺️ 2. Geography
Column	Meaning
* SP_STATE_CODE	State code (01–99, synthetic)
* BENE_COUNTY_CD	County code (synthetic)
These are not real FIPS codes — they’re anonymized but preserve distributional patterns.

### 🛡️ 3. Coverage Months (Insurance Enrollment)
These tell you how many months in the year the member had each type of Medicare coverage.

Column	Meaning
* BENE_HI_CVRAGE_TOT_MONS	Part A (Hospital Insurance) months
* BENE_SMI_CVRAGE_TOT_MONS	Part B (Supplementary Medical Insurance) months
* BENE_HMO_CVRAGE_TOT_MONS	Medicare Advantage (HMO) months
* PLAN_CVRG_MOS_NUM	Part D (drug plan) months
Example:
12, 12, 0, 12 → full-year Part A, Part B, Part D, no Medicare Advantage.

### 🩺 4. Chronic Condition Flags (CMS CCW Indicators)
* These are binary indicators (1 = condition present, 2 = condition absent).
* Yes — CMS uses 1 = Yes, 2 = No in SynPUF.

Column	Condition
* SP_ALZHDMTA	Alzheimer’s / dementia
* SP_CHF	Congestive heart failure
* SP_CHRNKIDN	Chronic kidney disease
* SP_CNCR	Cancer
* SP_COPD	COPD
* SP_DEPRESSN	Depression
* SP_DIABETES	Diabetes
* SP_ISCHMCHT	Ischemic heart disease
* SP_OSTEOPRS	Osteoporosis
* SP_RA_OA	Rheumatoid arthritis / osteoarthritis
* SP_STRKETIA	Stroke / TIA

Example:
2,2,2,2,... → no chronic conditions
1 → condition present

### 💵 5. Annual Spending (Medicare Payments)
These are annual totals for the beneficiary:

Inpatient (IP)
* MEDREIMB_IP – Medicare reimbursement
* BENRES_IP – Beneficiary responsibility (deductible/coinsurance)
* PPPYMT_IP – Primary payer payment (if Medicare secondary)

Outpatient (OP)
* MEDREIMB_OP
* BENRES_OP
* PPPYMT_OP

Carrier (CAR)
(Physician/supplier claims — office visits, imaging, labs, etc.)

* MEDREIMB_CAR
* BENRES_CAR
* PPPYMT_CAR

Example row:
140.00, 10.00, 0.00 → Medicare paid $140, member paid $10, no secondary payer.