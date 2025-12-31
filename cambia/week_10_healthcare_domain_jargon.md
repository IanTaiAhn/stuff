### PHASE 4 — Healthcare + Engineering Context (Weeks 10–12)

### Week 10 — Healthcare Domain Knowledge

#### Goal: Speak healthcare fluently without being clinical.

This week focuses on **understanding how healthcare data and systems actually work**. Strong candidates don’t need to practice medicine—but they must understand the constraints, risks, and trust requirements that make healthcare AI fundamentally different from other domains.

---

## Study

### Claims vs Clinical Data

#### Claims data
- Generated for billing and reimbursement
- Includes:
  - Diagnoses (ICD codes)
  - Procedures (CPT codes)
  - Costs and utilization
- Strengths:
  - Large scale
  - Longitudinal coverage
- Limitations:
  - Lagged in time
  - Optimized for billing, not clinical accuracy

#### Clinical data
- Generated during patient care
- Includes:
  - Notes
  - Labs
  - Vitals
  - Imaging
- Strengths:
  - Rich clinical detail
  - Closer to ground truth
- Limitations:
  - Noisy and unstructured
  - Fragmented across systems

---

### Delayed and Biased Data

#### Data delay
- Claims can lag weeks or months
- Outcomes may be recorded long after decisions are made

#### Sources of bias
- Access bias
  - Who receives care vs who does not
- Documentation bias
  - What clinicians choose to record
- Coding bias
  - Financial incentives influence codes

#### Why this matters for ML
- Labels may be incomplete or stale
- Models can learn system artifacts
- Evaluation can look strong while real-world impact is weak

---

### Importance of Interpretability

#### Why interpretability matters
- Clinicians must understand recommendations
- Patients deserve transparency
- Regulators require explainability

#### Interpretability vs performance
- Slightly lower accuracy is often acceptable
- Black-box models reduce trust and adoption

#### Common interpretability approaches
- Simple models where possible
- Feature attribution methods
- Clear decision thresholds
- Human-readable explanations

---

### Regulatory Mindset (HIPAA)

#### What HIPAA governs
- Protection of patient health information (PHI)
- Privacy and security requirements

#### Engineering implications
- Data minimization
- Access controls
- Audit logs
- Secure storage and transmission

#### Practical mindset
- Assume all data is sensitive
- Design for least privilege
- Log and monitor access continuously

---

### Why Healthcare AI Fails in Practice

#### Common failure modes
- Training on biased or incomplete data
- Ignoring clinical workflows
- Poor interpretability
- Overpromising automation
- Lack of clinician trust

#### Deployment realities
- Models assist, not replace, clinicians
- Human oversight is mandatory
- Incremental improvements outperform radical changes

---

## Interview-Ready When You Can:

- Explain differences between claims and clinical data
- Discuss how data delays affect modeling
- Justify interpretability over raw performance
- Show awareness of regulatory constraints
- **Tie AI decisions to patient safety and trust**
  - Explain how errors impact real patients
  - Emphasize transparency and human oversight
  - Frame AI as decision support, not authority
