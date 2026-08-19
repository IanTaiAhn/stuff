# Incident/postmortem finder — RAG agent design & implementation plan

A pull-style, doc-heavy agent: given a new problem's symptoms, environment, and repro steps, it finds and ranks similar past incidents across Jira, Confluence, and GitLab — with sources — instead of someone manually searching three separate tools. Builds on the Phase 1/Phase 2 infrastructure plan (Ollama + Open WebUI → Onyx CE), not a replacement for it.

---

## What makes this different from generic knowledge search

A generic assistant treats every source as equal and fans out across all of them. This agent has a known, fixed structure to exploit instead: a Jira ticket usually links to a Confluence postmortem, which usually links to (or is referenced by) the GitLab commit/MR that fixed it. That means retrieval isn't just "search three sources and merge" — it's **find the entry point via RAG, then walk the known link graph** from there. This is the piece that should use Onyx's Deep Research / agentic multi-step search rather than a single retrieval pass: once a plausible past incident is found, the agent should follow its links outward (ticket → postmortem → commit, and back) rather than stopping at the first hit.

---

## Input design

Three structured fields, not one chat box — because the actual input (per how this gets used in practice) is symptoms, environment/status, and reproducible steps, and collapsing that into one free-text query throws away structure that retrieval can otherwise exploit directly:

| Field | Purpose |
|---|---|
| Symptom description (prose) | Semantic similarity against past incident descriptions |
| Environment / component / status | Graded closeness signal — same service scores higher than unrelated, but never a hard cutoff |
| Reproducible steps | Semantic (or field-to-field, if data supports it) similarity — a matching sequence of actions is a stronger signal than matching prose alone |

**Open question to confirm before building ingestion:** does the team's Jira template have a real, separate "Steps to Reproduce" field, or is it free text inside the description? If structured, match field-to-field directly. If not, an extraction pass at ingestion time is needed to pull symptom/environment/repro-steps back out of historical tickets before structural matching is possible.

---

## Retrieval & scoring design

**Decision: recall over precision.** Environment/component is a *weighted signal*, not a hard filter — mismatched-environment incidents still surface, just ranked lower, rather than being excluded outright. This was a deliberate tradeoff: more noise to sift through, in exchange for not silently hiding a genuinely relevant cross-service incident.

**Scoring model — a transparent weighted sum, not a black-box reranker.** For a system still being learned and tuned, being able to see *why* something ranked where it did (and hand-adjust weights) is worth more than a marginal accuracy gain from an opaque model:

```
score = w1 * symptom_similarity        (semantic)
      + w2 * repro_step_similarity     (semantic)
      + w3 * environment_closeness     (graded: same service > same team > unrelated)
      - staleness_penalty              (step function, not a smooth decay)
```

**Staleness rule:** age doesn't matter across most of the range — a 3-year-old exact match shouldn't be quietly penalized. Only apply a flat discount past a **10-year threshold**. Use **resolution date**, not creation date, as the age reference — it reflects how long the fix has been sitting there (and possibly gone stale as the system evolved), not how long ago the ticket was filed. (Open question: if a very old ticket has recent follow-up activity, "last activity date" might be the more honest signal — worth checking whether that pattern exists in the real data before deciding it's needed.)

**Per-result explanation tags.** Since noisier results are allowed through, each one needs to explain itself, not just carry a number — a short tag like "same symptom, different service" or "same service, different symptom" lets someone triage 6-8 candidates fast. This is close to free: the three sub-scores are already computed before summing, so surfacing which one drove the match is formatting, not extra work.

---

## Where this lives architecturally (and why it's possible)

Both Open WebUI and Onyx implement RAG as an explicit, replaceable multi-stage pipeline (retrieve → rerank → generate) rather than a black box — because they're open source, this stage is something you can extend, not just configure:

- **Open WebUI**: has a dedicated **Pipelines** framework — a separate service specifically built for custom RAG logic in plain Python, sitting in front of the model call. This is where the weighted scoring function, the staleness step-function, and the explanation-tag formatting would live. Its built-in retrieval system already supports pluggable rerankers, so this isn't fighting the tool — it's using a documented extension point.
- **Onyx**: same seam — hybrid search plus reranking is already a distinct stage in its architecture, and Community Edition explicitly supports running custom code and building custom agents with their own actions. The multi-signal scorer can be registered as a custom action an agent calls with structured parameters (symptom, environment, repro_steps), or wired into the reranking stage directly.
- **Why the metadata-based signals are even possible**: connectors preserve structured metadata (dates, source system, tags) alongside document text rather than flattening everything into plain chunks. The environment/component signal and the staleness penalty only work because that metadata survives ingestion — this is the one place where the earlier ingestion design (Phase 2 connectors) is what makes today's retrieval design feasible at all.
- **Model decoupling**: Ollama only ever receives whatever context the pipeline hands it — none of this scoring logic touches the LLM. That means the ranking math is testable in isolation, against synthetic data, before a single token gets generated.

---

## Evaluation approach — synthetic enterprise data toolkit

Real company data isn't usable for this (correctly so). Three complementary sources, layered rather than picking just one:

**1. Hand-written fictional incident triples — start here, cheapest and most targeted.** A small number of fictional Jira ticket + Confluence postmortem + GitLab commit/MR sets, deliberately cross-referenced the way real ones are:

- Include **decoys** — a near-miss incident that sounds similar (same symptom wording) but has a different root cause and a different environment. This is the case that actually tests whether the multi-signal scoring works, versus a dataset with only obviously-distinct incidents.
- Deliberately stale one incident to test the 10-year step function.
- This handful of hand-built triples is what validates the *scoring logic itself* — small enough to reason about by hand, precisely targeted at the specific failure modes (decoys, staleness) this design is meant to catch.

**2. EnterpriseRAG-Bench's generation framework — for scaling past a handful of examples.** This is the closest existing analog to this exact problem: a synthetic enterprise corpus *and its generation framework*, spanning GitHub, Jira, and Confluence among other source types, deliberately built with realistic distractors — off-topic threads, half-finished drafts, near-duplicate pages. Worth drawing on its generation approach (or its released corpus directly, swapping GitHub for GitLab conceptually) once the hand-written triples confirm the scoring logic works and a larger volume is needed to stress-test it.

**3. RAGAS synthetic test generation — for auto-expanding whatever seed corpus you have.** Once there's a base set of documents (real, fictional, or from EnterpriseRAG-Bench), RAGAS can auto-generate question/context/answer triples from them, including multi-hop questions that require synthesizing across documents — useful for generating a larger evaluation set without hand-writing every question.

**Other production-grade generators worth knowing about if scale becomes a real constraint:** Red Hat's SDG Hub (question-answer-context triplet generation via a pipeline: topic extraction → question generation → groundedness filtering) and Google Research's Simula framework (fine-grained control over diversity/complexity in generated data) — both built specifically for the "no real data available" situation, not incident-finding specifically, but directly applicable.

**4. Real public OSS repos — a free, zero-confidentiality sanity check.** Any large, mature open-source project has genuine multi-source sprawl already: years of GitHub issues, PRs, and wikis where an old issue references a since-deleted wiki page. This won't match your company's structure, but it's real, uncurated messiness rather than synthetic — useful as an outside check that the traversal logic (walking ticket → doc → commit links) works on real link rot and inconsistency, not just on clean fictional examples.

**Recommended order**: hand-written triples with decoys first (validates the scoring math), then EnterpriseRAG-Bench-style generation or RAGAS expansion once that passes (validates it holds up at volume), with a public OSS repo as an occasional outside check that the traversal logic isn't just working on data shaped exactly the way you expected it to be.

---

## Implementation steps, in order

1. **Stand up base infrastructure** — Ollama + Open WebUI (Phase 1), then Onyx CE (Phase 2), per the earlier plan doc. Not repeated here.
2. **Build the synthetic incident corpus** — start with hand-written fictional ticket/postmortem/commit triples (including decoys and one deliberately stale example), then expand using EnterpriseRAG-Bench's generation approach or RAGAS synthetic test generation once the scoring logic passes on the small set. This is the test fixture everything else gets validated against.
3. **Resolve the open ingestion question** — confirm (or simulate, given synthetic data) whether repro-steps exist as a structured field; decide whether an extraction pass is needed.
4. **Implement the scoring layer** — as an Open WebUI Pipeline or an Onyx custom action/reranker: symptom similarity, repro-step similarity, environment closeness, staleness step-function, weighted combination, explanation-tag generation. Pure Python, testable without the LLM.
5. **Build the input interface** — either a small structured form (three fields) hitting the pipeline directly, or a lightweight extraction step that splits one free-text message into the three fields.
6. **Wire in the traversal/Deep Research layer** — once a retrieval hit is found, follow its known links (ticket ↔ postmortem ↔ commit) outward rather than stopping at the first match.
7. **Evaluate on the synthetic corpus** — check whether decoys get correctly down-ranked, tune `w1/w2/w3`, confirm the staleness cutoff behaves as intended.
8. **Only after the above is validated**: pursue a small, explicitly scoped, sanctioned pilot with real (non-sensitive, permissioned) data — this is the only way to get signal on real jargon and real linking patterns, and shouldn't be attempted before the design is validated synthetically.

---

## Open questions to resolve as you build

- Does Jira actually separate symptoms / environment / repro-steps into distinct fields, or is it one free-text description box?
- Is "last activity date" ever meaningfully different from "resolution date" for stale-but-still-touched tickets in this team's data — worth checking once real data is accessible?
- Starting weight values for `w1/w2/w3` are unknown until the synthetic eval produces a signal — don't hand-guess these as final.

---

## References

- Open WebUI Pipelines: https://github.com/open-webui/pipelines
- Open WebUI retrieval/reranking docs: https://docs.openwebui.com/features/extensibility/pipelines/
- Onyx: https://github.com/onyx-dot-app/onyx
- RAGAS synthetic test generation: https://docs.ragas.io
- EnterpriseRAG-Bench (dataset + generation framework): https://arxiv.org/abs/2605.05253 / https://onyx.app/enterpriserag-bench
- SDG Hub (Red Hat): `pip install sdg-hub`
- Simula framework (Google Research) — synthetic data generation for evaluation
