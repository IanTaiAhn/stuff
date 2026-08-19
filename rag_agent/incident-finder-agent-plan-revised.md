# Incident/postmortem finder — RAG agent design & implementation plan (revised)

A pull-style, doc-heavy agent: given a new problem's symptoms, environment, and repro steps, it finds and ranks similar past incidents across Jira, Confluence, and GitLab — with sources — instead of someone manually searching three separate tools. Builds on the Phase 1/Phase 2 infrastructure plan (Ollama + Open WebUI → Onyx CE), not a replacement for it.

> **Revision note.** This version corrects four things in the original that were verified against current upstream docs (August 2026): Open WebUI Pipelines is deprecated, the Onyx "wire into the reranking stage" path is Enterprise-gated, the staleness threshold was set so wide it could never fire, and the link-traversal layer — the actual differentiator — was written as a one-line configuration step. Corrections to the Phase 1/2 prerequisite doc are collected at the end. Changes are flagged inline as **[REVISED]**.
---

### search terms:

duplicate bug report retrieval, incident similarity search, case-based reasoning retrieval, issue-commit link recovery, structure-aware retrieval. Those will get you further than agentic RAG, which mostly returns framework tutorials.

## What makes this different from generic knowledge search

A generic assistant treats every source as equal and fans out across all of them. This agent has a known, fixed structure to exploit instead: a Jira ticket usually links to a Confluence postmortem, which usually links to (or is referenced by) the GitLab MR that fixed it. That means retrieval isn't just "search three sources and merge" — it's **find the entry point via RAG, then walk the known link graph** from there.

**[REVISED] — what the traversal step actually requires.** The original assumed Onyx's Deep Research would provide this. It won't, and this is the single biggest scoping correction in the document. Deep Research reformulates the query, runs multiple retrieval passes, and synthesizes a cited report — it is multi-step *search*, not graph traversal. Onyx does not build or store a cross-document link graph, so there is nothing for it to walk. Following ticket → postmortem → MR is a component you build:

1. **Extract link references at ingestion.** Parse Jira issue keys, Confluence page IDs/URLs, and GitLab MR/issue references out of document bodies and metadata. Mostly regex against known key formats, plus whatever native link fields the connectors preserve.
2. **Store an edge table.** A small relational table (`source_doc_id`, `target_doc_id`, `edge_type`, `confidence`) alongside the vector index — not in it. Edges are bidirectional in practice: a postmortem that names JIRA-1234 and a JIRA-1234 that names the postmortem are the same edge discovered from two directions, and should be deduplicated.
3. **Expose lookup as a tool.** "Given document X, return everything linked to it, one or two hops out" becomes an Action the agent can call after a retrieval hit. This is what makes the agentic loop useful — Deep Research supplies the multi-step *reasoning* over results; your edge table supplies the *edges*.

Treat this as its own workstream with its own tests, not a wiring step at the end.

---

## Input design

Three structured fields, not one chat box — because the actual input is symptoms, environment/status, and reproducible steps, and collapsing that into one free-text query throws away structure that retrieval can otherwise exploit directly:

| Field | Purpose |
|---|---|
| Symptom description (prose) | Semantic similarity against past incident descriptions |
| Environment / component / status | Graded closeness signal — same service scores higher than unrelated, but never a hard cutoff |
| Reproducible steps | Semantic (or field-to-field, if data supports it) similarity — a matching sequence of actions is a stronger signal than matching prose alone |

**[REVISED] — resolve the Jira field question before writing anything else.** The original listed this as an open question to resolve during the build. It shouldn't be: does the team's Jira template have a real, separate "Steps to Reproduce" field, or is it free text inside the description? Anyone with Jira access can answer it in five minutes, and the answer determines whether you need an LLM extraction pass over the entire historical ticket corpus to recover symptom/environment/repro-steps. That's a large, uncertain chunk of work sitting behind a trivially cheap question — so it moves to step 0 of the implementation order below.

---

## Retrieval & scoring design

**Decision: recall over precision.** Environment/component is a *weighted signal*, not a hard filter — mismatched-environment incidents still surface, just ranked lower, rather than being excluded outright. A deliberate tradeoff: more noise to sift through, in exchange for not silently hiding a genuinely relevant cross-service incident.

**Scoring model — a transparent weighted sum, not a black-box reranker.** For a system still being learned and tuned, being able to see *why* something ranked where it did (and hand-adjust weights) is worth more than a marginal accuracy gain from an opaque model:

```
score = w1 * symptom_similarity        (semantic)
      + w2 * repro_step_similarity     (semantic)
      + w3 * environment_closeness     (graded: same service > same team > unrelated)
      - staleness_penalty              (step function, not a smooth decay)
```

**[REVISED] Staleness rule — derive the threshold from the corpus, don't hardcode ten years.** The original applied a flat discount past a 10-year threshold. In practice that's a no-op: most Jira instances aren't that old, so the penalty would never fire, and the eval could only "validate" it by fabricating a 10-year-old ticket — which tests the code path, not the policy. It also gets the incident domain backwards. A decade-old fix to a system since rewritten twice has close to zero transfer value, which is the opposite of the original's premise that age barely matters.

Instead: keep the step function (a smooth decay would quietly penalize a 3-year-old exact match, which is the thing worth avoiding), but set the cutoff as a percentile of the corpus's own resolution-date distribution — start around the 90th percentile of age and tune from there. On a five-year-old Jira instance that lands somewhere near four years, not ten, and the penalty actually fires often enough to be measurable.

Keep **resolution date**, not creation date, as the age reference — it reflects how long the fix has been sitting there, not how long ago the ticket was filed. (Open question retained: if a very old ticket has recent follow-up activity, "last activity date" may be the more honest signal — worth checking whether that pattern exists in real data.)

**Per-result explanation tags.** Since noisier results are allowed through, each one needs to explain itself, not just carry a number — a short tag like "same symptom, different service" or "same service, different symptom" lets someone triage 6-8 candidates fast. This is close to free: the three sub-scores are already computed before summing, so surfacing which one drove the match is formatting, not extra work.

---

## Where this lives architecturally

**[REVISED] — build the scorer once, as a standalone service.** The original offered a fork: implement it as an Open WebUI Pipeline *or* as an Onyx custom action. Since Phase 2 replaces Phase 1's retrieval entirely, taking the first branch means throwing the work away at the phase boundary.

Build it instead as a **standalone HTTP service with an OpenAPI 3.0/3.1 spec**, harness-agnostic. Pure Python, no dependency on either UI, testable in isolation with no LLM in the loop. Phase 1 calls it from a Pipe Function; Phase 2 registers the same spec as an Onyx Action. One implementation, one test suite, survives the migration.

- **Open WebUI — use Functions, not Pipelines. [REVISED]** The original placed the scoring function in Open WebUI's Pipelines framework. Upstream now marks Pipelines as legacy and no longer recommended: both pipe-type and filter-type Pipelines have in-process replacements (Pipe Functions and Filter Functions) that are built in, easier to configure, and need no separate worker container. The docs pages are kept only for reference and existing deployments. So: a **Pipe Function** that calls the scoring service, retrieves, reranks, and hands context to the model. Same Python, one fewer container. Note that Functions execute arbitrary Python on the server and creation is admin-restricted — fine for this deployment, worth knowing.
- **Onyx — register as an Action, not a pipeline hook. [REVISED]** The original suggested wiring the scorer into the reranking stage directly. That path is **Enterprise Edition**: Onyx's EE feature list includes Hook Extensions ("inject custom logic into Onyx's pipeline at defined stages without modifying source code"), and the README's "run custom code" bullet sits in the enterprise block too. The Community Edition route is the other one the original mentioned, and it works: Onyx ships five built-in Actions and lets you configure additional ones via OpenAPI or MCP. Register the scoring service's OpenAPI spec as a custom Action, then build a custom agent that calls it with structured parameters (`symptom`, `environment`, `repro_steps`). The edge-table lookup from the traversal workstream registers the same way. Both are CE-compatible and free. Modifying the reranker itself would mean forking — possible under MIT, but that's a fork, not an extension point.
- **Why the metadata-based signals are possible.** Connectors preserve structured metadata (dates, source system, tags) alongside document text rather than flattening everything into plain chunks. The environment/component signal and the staleness penalty only work because that metadata survives ingestion — the Phase 2 connector design is what makes this retrieval design feasible at all.
- **[REVISED] Connector caveat — the "commit" leg may not exist.** The Onyx GitLab connector indexes merge requests (open and closed, title and summary) and issues/incidents including comments. Commits are not in the documented list, though an open parity issue suggests the GitLab connector may index more of the repository than the GitHub one does. Verify this against your own GitLab before designing around it. If commits aren't indexed, the triple is **ticket → postmortem → MR**, which is fine — MRs carry the diff reference anyway — but the edge extractor needs to target MR references, not commit SHAs.
- **Model decoupling.** Ollama only ever receives whatever context the pipeline hands it — none of this scoring logic touches the LLM. The ranking math is testable in isolation, against synthetic data, before a single token gets generated.

---

## Evaluation approach — synthetic enterprise data toolkit

Real company data isn't usable for this (correctly so).

**[REVISED] — the central validity problem.** The original's recommended order was: hand-written triples first, then scale up, with public OSS repos as an occasional outside check. The problem is that hand-written decoys authored by the person who designed the scorer are decoys the scorer already anticipates. That evaluation can pass without telling you anything — it can't fail informatively, because the failure modes it tests are exactly the ones the design was built to catch. Hand-written triples are still the right *first* step, but as a smoke test for the code, not as validation of the design. Adversarial and outside-sourced data has to arrive earlier than the original allowed.

**1. Hand-written fictional incident triples — smoke test, not validation.** A small number of fictional Jira ticket + Confluence postmortem + GitLab MR sets, deliberately cross-referenced the way real ones are:

- Include **decoys** — a near-miss incident with similar symptom wording but a different root cause and environment.
- Deliberately stale one incident, dated past whatever percentile threshold the corpus produces, to exercise the staleness branch.
- Small enough to reason about by hand. Confirms the scoring math runs and the sub-scores move in the right direction. It does not confirm the design generalizes.

**2. EnterpriseRAG-Bench — including the metadata question set. [REVISED]** This is the closest existing analog: roughly 500,000 documents across nine enterprise source types (Slack, Gmail, Linear, Google Drive, HubSpot, Fireflies, GitHub, Jira, Confluence) with 500 questions, generated with cross-document coherence and augmented with realistic noise — misfiled documents, near-duplicates, conflicting information. MIT-licensed, on GitHub and HuggingFace, with a released generation framework for producing variants tuned to your own industry and source mix.

The detail the original missed: the repo ships an **additional 100 metadata-dependent questions in `extra_questions.jsonl`**, excluded from the leaderboard because their evaluation criteria differ, explicitly aimed at teams doing metadata-aware RAG. The environment-closeness signal and the staleness penalty *are* metadata-aware RAG. That file is the nearest off-the-shelf test for the specific thing this design does differently, and it wasn't written by you — which is exactly what the hand-written set can't offer. Use it early, not late.

Note it uses GitHub rather than GitLab; conceptually interchangeable for these purposes.

**3. Real public OSS repos — move this earlier. [REVISED]** Any large, mature open-source project has genuine multi-source sprawl: years of issues, PRs, and wikis where an old issue references a since-deleted wiki page. It won't match your company's structure, but it's real, uncurated messiness — and it's the only proposed source that wasn't shaped by your own assumptions. This is where the traversal logic gets its real test, against actual link rot and inconsistent referencing. It should run as soon as the edge extractor exists, in parallel with the synthetic work, rather than as an occasional later check.

**4. RAGAS synthetic test generation — for auto-expanding a seed corpus.** Once there's a base set of documents, RAGAS can auto-generate question/context/answer triples from them, including multi-hop questions requiring synthesis across documents — useful for volume without hand-writing every question.

**Other production-grade generators, if scale becomes a real constraint:** Red Hat's SDG Hub (question-answer-context triplet generation via topic extraction → question generation → groundedness filtering) and Google/EPFL's Simula (seedless, taxonomy-driven generation with fine-grained control over coverage, diversity, and complexity). **[REVISED]** Simula is aimed primarily at generating fine-tuning data for specialized domains and, as of this writing, appears to be a published framework rather than a released package — treat it as a source of method, not a tool to install.

**[REVISED] Recommended order:** hand-written triples (smoke test) → edge extractor against a public OSS repo (traversal reality check) → EnterpriseRAG-Bench, `extra_questions.jsonl` first (outside validation of the metadata signals) → RAGAS or EnterpriseRAG-Bench generation for volume.

---

## Implementation steps, in order

**[REVISED] — reordered. Step 0 is new, the traversal layer is expanded from one step to three, and the scorer moved before the harness decision.**

0. **Answer the Jira field question.** Does Jira separate symptoms / environment / repro-steps into distinct fields? Five minutes with Jira access. If not, scope the extraction pass now — it's a substantial workstream and everything downstream assumes an answer.
1. **Stand up base infrastructure** — Ollama + Open WebUI (Phase 1), then Onyx CE (Phase 2), per the earlier plan doc, with the GPU correction noted at the end of this document.
2. **Build the synthetic incident corpus** — hand-written fictional ticket/postmortem/MR triples with decoys and one deliberately stale example. The test fixture everything else validates against.
3. **Implement the scoring service** — standalone HTTP service with an OpenAPI spec: symptom similarity, repro-step similarity, environment closeness, percentile-derived staleness step-function, weighted combination, explanation-tag generation. Pure Python, no LLM, no UI dependency, unit-tested against the fixtures from step 2.
4. **Build the link extractor and edge table** — parse Jira keys, Confluence page references, and GitLab MR references out of ingested documents; store deduplicated bidirectional edges; expose one- and two-hop lookup behind its own OpenAPI endpoint.
5. **Validate traversal against a public OSS repo** — run the extractor over a large real project's issues, PRs, and wiki. Measure how many extracted edges resolve to something that still exists. This is where link rot shows up, and it will not show up in the synthetic corpus.
6. **Wire into the harness** — Phase 1: a Pipe Function calling both services. Phase 2: register both OpenAPI specs as Onyx Actions and build a custom agent that calls them. The services themselves don't change between the two.
7. **Build the input interface** — either a small structured form (three fields) hitting the scoring service directly, or a lightweight extraction step splitting one free-text message into the three fields.
8. **Evaluate** — hand-written corpus first (do decoys get down-ranked?), then EnterpriseRAG-Bench's metadata question set (do the metadata signals hold up on data you didn't write?). Tune `w1/w2/w3`; confirm the staleness cutoff fires at a sensible rate rather than never.
9. **Only after the above is validated:** pursue a small, explicitly scoped, sanctioned pilot with real (non-sensitive, permissioned) data — the only way to get signal on real jargon and real linking patterns, and not to be attempted before the design is validated synthetically.

---

## Open questions to resolve as you build

- ~~Does Jira separate symptoms / environment / repro-steps?~~ **Moved to step 0** — answer it before building.
- Does your GitLab instance expose commits through the Onyx connector, or only MRs and issues?
- Is "last activity date" ever meaningfully different from "resolution date" for stale-but-still-touched tickets in this team's data?
- What percentile of the resolution-date distribution makes a sensible staleness cutoff, once there's a real corpus to measure?
- Starting weight values for `w1/w2/w3` are unknown until the eval produces a signal — don't hand-guess these as final.
- **[NEW]** How many extracted edges resolve to documents that still exist? A low rate changes the traversal design from "walk the graph" to "walk the graph and handle dead ends gracefully."

---

## Corrections to the Phase 1/2 prerequisite plan

These affect the infrastructure this agent sits on and should be applied to that document.

**GPU sizing is too optimistic.** `qwen3.5:9b` is real and Apache-2.0, but the official Q4_K_M build is 9.65B parameters at **6.6GB of weights alone** — not the "~6–8GB VRAM" total the plan claims for the whole workload. Add `nomic-embed-text`, KV cache, and desktop overhead, and an 8GB card spills to CPU at any useful context length; the community Modelfile for this exact model targets 16GB, budgeting ~9GB of headroom for a 32K context. Phase 2 then adds Onyx's own indexing and inference model-server containers, which also want GPU. **Revised floor: 12GB (RTX 3060). Comfortable target: 16GB.** Below that, drop to `qwen3.5:4b` as the plan already suggests, or expect CPU offload.

**Permission syncing is Enterprise, not Community.** The Phase 2 capability table lists "40+ connectors ... with continuous sync and permission syncing" under CE. Continuous sync is CE; **Permission Sync Connectors are an Enterprise Edition feature**, alongside OIDC/SAML SSO, user groups and RBAC, group-based permissions, usage analytics, encrypted secrets, and Hook Extensions. The doc half-catches this later — it correctly lists group-based permission inheritance as EE-gated — so as written it contradicts itself. For an incident corpus spanning Jira, Confluence, and GitLab, ACL awareness is worth a deliberate decision rather than an assumption. Note also that **encrypted secrets is EE**, which matters when you're storing Jira/GitLab/Confluence API tokens on a self-hosted box.

Deep Research does hold up: CE covers the core Chat, RAG, Agents, and Actions feature set, and Deep Research is not on the EE list. Connector count is now 50+, not 40+.

**Phase 1's exit criteria carry a hidden risk.** The plan proposes proving the concept on Open WebUI's built-in RAG, then running EnterpriseRAG-Bench as a sanity check, and moving to Phase 2 "once Phase 1 proves the core value." On that benchmark's published leaderboard, Onyx scores 72.4 and **Open WebUI scores 24.9 — last of the ten systems listed**, below LlamaIndex and LangChain. If Phase 1 is evaluated against that number, it will look like a failure of the idea when it's substantially a limitation of the harness, and the exit criteria could kill a good project at the wrong gate.

Two caveats worth holding: Onyx authored the benchmark and tops its own leaderboard, so treat the absolute ordering with some skepticism; and RAG quality is corpus-specific, so neither number predicts performance on your documents. But a roughly 3x gap is large enough to act on. **Suggested revision:** judge Phase 1 on whether people use it and whether retrieval-grounded answers are directionally useful — not on benchmark score — and treat weak retrieval quality as an argument *for* Phase 2 rather than evidence against the concept. If the team has appetite for the heavier stack up front, going straight to Onyx CE is defensible.

---

## References

- Open WebUI Functions (current extension point): https://docs.openwebui.com/features/extensibility/plugin/functions/
- Open WebUI Pipelines (deprecated, reference only): https://docs.openwebui.com/features/extensibility/pipelines/
- Onyx: https://github.com/onyx-dot-app/onyx
- Onyx Actions & MCP: https://docs.onyx.app/overview/core_features/actions
- Onyx Enterprise Edition feature list: https://docs.onyx.app/deployment/miscellaneous/enterprise_edition
- Onyx GitLab connector: https://docs.onyx.app/connectors/gitlab
- EnterpriseRAG-Bench (dataset, generation framework, `extra_questions.jsonl`): https://github.com/onyx-dot-app/EnterpriseRAG-Bench
- EnterpriseRAG-Bench paper: https://arxiv.org/abs/2605.05253
- EnterpriseRAG-Bench leaderboard: https://onyx.app/enterpriserag-bench
- RAGAS synthetic test generation: https://docs.ragas.io
- SDG Hub (Red Hat): `pip install sdg-hub`
- Simula (Google Research / EPFL): https://research.google/pubs/reasoning-driven-synthetic-data-generation-and-evaluation/
- `qwen3.5:9b` model card (size, quantization, license): https://ollama.com/library/qwen3.5:9b
