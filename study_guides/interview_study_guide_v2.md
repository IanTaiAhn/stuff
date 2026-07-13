# Interview Study Guide — Data Science / ML / AI Engineer Roles
### Ian Tai Ahn — calibrated to actual profile: 3 YOE SWE (defense/high-compliance), M.S. Data Science, Tech Lead/Scrum Master scope, production RAG project work, Active Secret clearance
### Guidehouse · Acentra Health · City of Hope · ManTech · RealmOne · Rackner · Cadence Solutions

## How to use this guide

Each topic is tagged by tier:
- **[FOUNDATION]** — must be zero-hesitation. Getting these wrong is a hard stop regardless of level.
- **[CORE]** — the actual bar for these postings at your experience level. This is where most of your prep time should go.
- **[STRETCH]** — senior/staff-adjacent depth. Not required, but you asked to be over-prepared, and a couple of these employers (Guidehouse especially) do sometimes push technical-lead-track candidates here given your Tech Lead title. Worth a pass, not worth obsessing over.

Given your resume, two things are worth saying up front:
1. **Your GenAI/RAG depth is a genuine strength, not a hedge.** Don't undersell it as "a personal project" — you built chunking, embedding, retrieval, and structured output generation against real regulatory documents (Medicare LCD policy, ICD-10/CPT). That's production-grade thinking. Treat GenAI questions as home turf.
2. **Classical ML (regression/classification/ensembles) is your one real, specific, nameable gap**, per your own resume. I've built in a shoring-up plan for exactly that below, plus a note on what to say if it comes up honestly.

---

## 1. SQL — [FOUNDATION]

Every one of these companies touches large, messy datasets (claims, EHR, DoD big data, patient monitoring). This is tested somewhere in nearly every loop, including SWE/AI-engineer titles.

- Window functions: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LAG()`/`LEAD()`, running totals with `SUM() OVER (...)`, `PARTITION BY` vs `ORDER BY`
- CTEs — multi-step queries where each step builds on the last, cold, no reference
- Joins: inner/left/right/full, and when a join silently duplicates rows
- Sessionization (gap-based session detection via `LAG` + cumulative `SUM`), cohort windows
- `GROUP BY` with conditional aggregation (`CASE WHEN` inside `SUM`/`COUNT`)

**Practice prompts:**
- Sessionize timestamped events (new session if gap > 30 min)
- Users with ≥3 events in 30 days before churn, where churn = no activity in the following 30 days
- Given a claims/encounters table, calculate a rolling 7- or 30-day metric
- Median without `MEDIAN`/`PERCENTILE`

**Your specific proof point:** your F-35 OBPHM bullet mentions "transforming multi-table relational data across regression cycles" — that *is* SQL/relational work. Be ready to describe the actual joins/aggregations you did there in technical detail; right now it's phrased generically enough that an interviewer may probe it as a bluff-check.

---

## 2. Statistics & Experimentation — [FOUNDATION] core concepts, [CORE] applied depth

- Hypothesis testing: null/alternative, Type I/II errors, p-values (what they do and don't mean)
- Confidence intervals — what "95% CI" actually means
- A/B testing basics: randomization, sample size intuition, the peeking problem, guardrail metrics
- **Class imbalance — know this cold**: why accuracy fails on rare-event data (fraud, disease incidence, denial prediction). This is asked almost verbatim across healthcare and security-adjacent employers in your batch.
- Precision/recall/F1, and why PR-AUC beats ROC-AUC on imbalanced classes
- Regression fundamentals: interpreting coefficients, what Ridge/Lasso do conceptually

**Guaranteed framing:** "Your model has 94% accuracy but the [fraud/denial] team is unhappy — walk me through your diagnosis." Answer: check the base rate first, recognize a trivial always-negative classifier could hit that accuracy, pivot to precision/recall.

**[STRETCH]:** experiment design nuances — novelty effects, multiple-comparison correction (Bonferroni), stratified sampling by segment. Senior DS loops probe this; entry/mid loops rarely do, but knowing it costs you nothing and signals more maturity than the question requires.

---

## 3. Classical ML / DS Fundamentals — your flagged gap area, [CORE] priority

This is the one area where your resume shows a real hole relative to City of Hope's and Guidehouse's Health AI/ML DS postings (both explicitly want Random Forest/XGBoost/CNN/RNN-style predictive modeling). Here's a tight shoring-up plan, not a full curriculum:

**[FOUNDATION] — must be able to explain simply:**
- Supervised vs. unsupervised learning with concrete examples (recurring opener across this whole batch — Guidehouse and Acentra both ask it near-verbatim)
- Bias-variance tradeoff, overfitting/underfitting
- Cross-validation, and specifically **why grouped/time-based splits matter** for patient-level or user-level data to avoid leakage — this is a good one to know cold because it signals production maturity, not textbook knowledge

**[CORE] — the actual gap to close before interviews:**
- Logistic regression: what it outputs, how to interpret coefficients/odds ratios
- Random Forest and XGBoost/LightGBM: conceptually how ensembles reduce variance, why gradient boosting tends to outperform on tabular data, and the interpretability trade-off vs. logistic regression
- k-means, k-NN, Naive Bayes at a "know what it's for and its assumptions" level
- Feature engineering and handling missing/dirty data
- Model evaluation beyond accuracy: confusion matrix, calibration

**Your honest talking point if pressed on this gap:** you don't need to fake production experience with XGBoost. A strong, honest answer is something like: "My hands-on production work has been concentrated in NLP/RAG systems, but I've built classical models in my M.S. coursework and can walk through when I'd reach for logistic regression vs. a tree ensemble." Confident honesty about scope reads far better than overclaiming — interviewers at this level are specifically listening for candidates who inflate to sound senior.

**Concrete move before interviews (not just for the interview, for your resume too):** if you have even one regression/classification project from your M.S. coursework, resurface it — a single added bullet turns "no visible classical-ML proof point" into a real answer instead of a gap you're talking around.

**[STRETCH]:** CNN/RNN/LSTM at a conceptual level (what problem each architecture is suited for) — City of Hope's JD lists deep learning explicitly. You don't need implementation depth; you need to be able to say what a CNN is good at (spatial/image data) vs. an RNN/LSTM (sequential data) and why, in under 30 seconds.

---

## 4. GenAI / LLM / RAG — your strongest area, [CORE] and genuinely [STRETCH]-ready

Treat this section as home turf, not hedge material. Given your Prior Auth project, you should be able to go *deeper* here than most candidates at your level — this is where you differentiate.

**[CORE] — be fluent and specific, using your own project as the walkthrough:**
- RAG architecture end to end: ingestion → chunking strategy → embedding → vector store → retrieval → (re-ranking) → generation → grounding/citation. Be ready to describe **your actual chunking strategy decisions** on the Prior Auth project — why you chunked the way you did against LCD policy documents, and what would break if chunks were too large/small
- Vector databases and embedding models (sentence-transformers, in your case) — know trade-offs, not just names
- Structured output generation with Pydantic — this is a real differentiator most candidates can't speak to; be ready to explain why structured output matters for downstream reliability (e.g., a denial-prevention checklist can't be freeform text)
- Prompt engineering as the cheapest/fastest lever vs. fine-tuning or retrieval changes
- Evaluating LLM output with no single right answer: eval sets, LLM-as-judge and its failure modes

**[STRETCH] — worth rehearsing since you can actually answer these credibly:**
- **Evaluation rigor**: how would you build a regression test suite for your Prior Auth pipeline so a prompt or model swap doesn't silently break checklist accuracy?
- **Cost/latency trade-offs**: given you used Groq specifically (a low-latency inference provider), be ready to explain *why* — that's a real production decision most candidates haven't had to make
- **Guardrails/governance**: since Guidehouse's Health AI/ML JD explicitly lists fairness, bias, explainability, and reproducibility — connect this to your own project: how would you validate that your ICD-10/CPT extraction is *correct*, not just plausible-sounding, given the compliance stakes of prior authorization?
- Agentic workflows: definitionally (LLM in a loop, choosing tools, observing results) — you likely haven't built a multi-agent system, and it's fine to say so plainly while reasoning through a hypothetical one

**A likely real question given your background:** "Walk me through your Prior Auth project end to end." Prepare this as a 2-3 minute narrative: the problem (unstructured LCD policy → structured, actionable checklists), your architecture decisions, what you'd change with more time (e.g., adding an eval harness, human-in-the-loop review), and why it matters in a compliance-heavy domain. This single answer will probably do more work in your interviews than any other single prep item.

---

## 5. System Design & Distributed Systems — [CORE] given your actual experience, don't undersell this

Because you've genuinely operated at a Tech Lead level across 30+ microservices with Kubernetes, Helm, service mesh, and CI/CD, you have real material here that most "mid-level" candidates don't — use it rather than defaulting to textbook system design.

**[CORE] — lightweight system design, scoped to a single service or component:**
- Design a rate limiter, a URL shortener, an API for X — focus on clear API contracts, sensible data modeling, and naming trade-offs (consistency vs. availability, sync vs. async) rather than drawing every AWS box you know
- Design a document ingestion pipeline for an AI chatbot (directly relevant to Guidehouse/Acentra) — you can answer this from lived experience, not theory

**[STRETCH] — distributed systems concepts you can speak to from real experience, don't leave these on the table:**
- Idempotency, retries with backoff, observability (you've directly worked with Prometheus/Grafana/Splunk — be ready to describe a real incident you diagnosed using these tools)
- Service mesh routing/policy concepts (Kyverno policy deadlocks is a genuinely good "tell me about a bug you diagnosed" story — it's specific, technical, and shows real production judgment)
- CI/CD pipeline design trade-offs (Flux/Ansible) — GitOps vs. push-based deploys, why you'd choose one

**A likely real question:** "Tell me about the most complex distributed-systems bug you've debugged." Your Kyverno policy deadlock story is strong material for this — rehearse it as a full narrative (symptom → investigation → root cause → fix → what you changed to prevent recurrence), not just a bullet point.

---

## 6. Leadership & Behavioral — you have real scope now, don't undersell it

Because you're an actual Scrum Master and Technical Lead with ~70% hands-on ownership across a cross-functional team, this is different advice than generic "mid-level" guidance: **you have legitimate leadership stories and should use them directly**, not hedge them into individual-contributor framing.

- **Use STAR** (Situation, Task, Action, Result) for 5-7 stories, and let some of them be genuinely leadership-scoped: running Agile ceremonies, clearing blockers across teams (Unity/systems modeling coordination), translating ambiguous requirements into sprint-ready work, mentoring/onboarding developers during the React refactor
- A strong, honest answer to "tell me about a time you led something" is your actual Scrum Master role — don't manufacture a bigger story when you have a real one
- Keep one or two individual-contributor-scoped stories ready too (the React refactor, the OBPHM automation work) for questions specifically probing hands-on technical depth, since interviewers sometimes worry that a "lead" title means someone's gone rusty on hands-on work
- Quantify where you can: "~10 hours/month saved," "reduced a 30-minute manual process to seconds" — these are good, specific numbers, keep using them
- "Why [Company]" — for City of Hope, Guidehouse's federal health work, and ManTech/RealmOne's national security framing, connect your own motivation genuinely; a generic answer under-uses a resume this specific
- City of Hope weights DEI/inclusion values explicitly — have a genuine answer ready
- Guidehouse consulting-track rounds ask directly: "give an example of a challenging project," "what interests you about Guidehouse," "describe a conflict you had to resolve" — your file-sync/cross-team coordination work is strong material for the conflict question
- Cadence Solutions requires a **project pitch presentation** — budget real time (candidates report the "4-5 hour" assignment takes closer to 10) and rehearse it as a persuasive pitch, not a technical readout

---

## 7. Domain Knowledge

### Healthcare/health-data track (Guidehouse Health AI/ML DS, Acentra, City of Hope — both listings)
- **You already have real depth here** — ICD-10/CPT, Medicare LCD policy, prior authorization logic are all in your project. Lead with this rather than treating it as background reading.
- EHR familiarity, especially **EPIC** (named explicitly in City of Hope Revenue Cycle) — you likely need to shore this up specifically, since your project touches coding/policy but not EHR systems directly
- Interoperability standards: **FHIR, HL7** at minimum — know what each is for in one sentence
- **HIPAA basics** — why PHI handling constrains model design and deployment
- Claims/denials/AR-days vocabulary for the City of Hope Revenue Cycle role specifically

### Federal/government contracting track (Guidehouse, ManTech, RealmOne, Rackner)
- Your **active Secret clearance** is a real asset — state it early and plainly. For Guidehouse specifically (Public Trust required), you exceed the bar, which is worth surfacing explicitly since it removes their biggest hiring friction point
- **Important distinction for RealmOne**: that posting requires clearance *with polygraph* — materially different and more invasive than Secret alone. Don't assume your current clearance transfers; ask the recruiter directly and early whether your existing investigation covers it or whether a new poly process would be required
- Responsible/governed AI vocabulary (model risk management, human-in-the-loop) — Guidehouse's language almost verbatim
- MLOps lifecycle end-to-end (ManTech JD calls this out directly) — you have real material here via Kubernetes/Helm/CI-CD experience, connect it explicitly to model deployment even though your production experience is with services rather than models specifically

---

## 8. Company-Specific Notes (recap)

- **Guidehouse**: multiple reports of **timed logic/coding puzzles** sprung with little warning during phone screens — be mentally ready for this format specifically. DS-track loops sometimes include a live Python evaluation.
- **Acentra Health**: overall moderate difficulty; expect supervised-vs-unsupervised and model-evaluation-metric questions even at a technical level, plus a straightforward behavioral round.
- **City of Hope**: recruiter screen → technical interview → panel (often 3-4 hours) → DEI/mission-fit questions woven throughout.
- **ManTech**: recruiter screen → technical interview with program managers, heavy emphasis on communicating technical concepts to non-technical government stakeholders.
- **RealmOne**: thin public data; the real gate is the clearance/poly process, not a heavy technical bar — confirm poly requirements early.
- **Rackner**: recruiter screen + 1-2 technical rounds; expect a prototype/demo-walkthrough conversation given the R&D framing.
- **Cadence Solutions**: the most demanding loop in the batch — 4 interviews plus a required project-pitch presentation; recent candidate reports flag inconsistent recruiter warmth, so don't read a cold interviewer as a bad signal about your performance.

---

## 9. Pre-Interview Checklist

- [ ] Can I write a 3-step CTE with a window function cold, no reference?
- [ ] Can I explain why accuracy fails on imbalanced data, unprompted, in under 30 seconds?
- [ ] Can I explain logistic regression vs. Random Forest/XGBoost trade-offs simply, and name a project (even coursework) as evidence?
- [ ] Can I walk through my Prior Auth RAG project end-to-end in 2-3 minutes, including what I'd improve with more time?
- [ ] Do I have a full narrative (not just a bullet) ready for the Kyverno policy deadlock bug?
- [ ] Do I have both leadership-scoped and IC-scoped STAR stories ready, so I can match whichever the question is probing?
- [ ] Do I know my clearance status precisely, including that it does NOT cover polygraph-required roles, and can I state this plainly?
- [ ] Can I name FHIR/HL7/EPIC/claims-denials vocabulary if it's a health-data role?
- [ ] Have I confirmed with the recruiter (for RealmOne specifically) what clearance level the role actually requires before investing prep time?
- [ ] Do I have 2-3 smart questions ready about team, tech stack, and current projects?
- [ ] For Guidehouse: am I ready for a timed logic/coding puzzle sprung with little warning?
- [ ] For Cadence Solutions: is my project pitch deck built and rehearsed *before* the loop starts?

---

*Compiled from current job postings, candidate-reported interview experiences (Glassdoor, InterviewQuery), level-specific interview research, and your actual resume as of July 2026. Company processes and interviewer panels change — treat this as a strong baseline, not a guarantee of what you'll be asked.*
