# Mock Interview Prep — Ian Tai Ahn

Organized by resume area, roughly in order of how likely an interviewer is to dig in. Each question includes what a strong answer needs to *contain* (not a script — fill in your real specifics) and the follow-up trap to expect.

---

## 1. Technical Lead & Scrum Master — File Sync Initiative (current role)

**Q: Walk me through the architecture of the file sync solution. What problem does it actually solve?**
A strong answer names: what's out of sync (build artifacts? config? Unity assets? code?), across how many bare-metal servers, and the core mechanism — polling vs. event-driven, how conflicts are detected and resolved, how versioning works, and what happens on failure/partial sync.
*Follow-up trap:* "What happens if two servers push conflicting changes at the same time?" — have a real answer, not "that shouldn't happen."

**Q: Why bare-metal servers instead of syncing at the container/microservice layer?**
This is a meaningful architecture choice, not a detail — be ready to explain it. Defense/Lockheed infrastructure often means air-gapped networks, no cloud orchestration layer available, hardware you don't control the provisioning of, or compliance requirements that rule out container-native sync tools. Name the actual constraint that pushed the solution to the OS/server level (file system access, network topology, security boundary, lack of a shared orchestrator) rather than a framework decision.
*Follow-up trap:* "Your summary mentions a platform spanning 30+ microservices — how does that reconcile with syncing across 'several' bare-metal servers?" Have a clean answer ready: e.g., the 30+ microservices run *on top of* a smaller number of physical/bare-metal hosts, and File Sync operates at the host level, not per-service. If you don't have a clean reconciliation, that's worth sorting out before an interview asks it, since two numbers describing "the platform" that don't obviously connect is the kind of thing interviewers probe.

**Q: What tooling are you actually using to do the sync — rsync, a custom script, something else?**
Needs the real tool and why: reliability over a flaky link, handling large files, incremental vs. full sync, how you detect drift between servers in the first place.

**Q: You said ~70% technical ownership. What does the other 30% — the Scrum Master work — actually look like day to day?**
Name the ceremonies you run (standups, sprint planning, retro, backlog grooming), and one concrete example of a *decision* you made as Scrum Master, not just a facilitation task.
*Follow-up trap:* "Tell me about a time the team disagreed with your prioritization call." — needs a real conflict, not a hypothetical.

**Q: Give me a specific example of a blocker you cleared for the team.**
Needs: what was blocking, whose problem it technically was, what you did (escalated? built a workaround? changed a requirement?), and the outcome in days/effort saved.

**Q: How do you coordinate with the Unity and systems modeling teams when requirements are ambiguous?**
Needs a real example of translating an ambiguous ask into a sprint-ready ticket — what was ambiguous, what questions you asked, what the final scoped ticket looked like.

---

## 2. React Refactor — LODEM Modernization

**Q: What was actually wrong with the component library before your refactor?**
Needs specifics: duplicated components across how many places, what pain that caused (bug fixes needed in 3 places, inconsistent UI, slow onboarding), and your new structure (shared component lib, design system, folder architecture).

**Q: How does the React frontend talk to Unity WebGL? What's hard about that integration?**
Needs to explain `react-unity-webgl` message passing (JS↔Unity bridge), state sync issues, and a real bug you hit at that boundary.

**Q: Why PostgreSQL for this app, and what's the schema roughly look like for damage/repair entries?**
Should be able to sketch 3–4 core tables and one non-trivial query or constraint you had to handle (e.g., versioned repair entries, audit trail).

---

## 3. Kubernetes / Service Mesh (CS3 Platform Engineer)

**Q: Explain a Kyverno policy deadlock in plain terms. How did your Robot Framework tests surface it?**
This is the detail most likely to expose padding if you can't explain it crisply. Needs: what Kyverno enforces (admission control policies), what a *deadlock* looks like in that context (e.g., a policy blocking a resource that another policy requires to exist first, or a validating webhook creating a circular dependency), and what your test actually checked for and how it failed loudly enough to catch it.
*Follow-up trap:* "How did you fix it?" — have the actual remediation, not just detection.

**Q: What was wrong with the original Helm charts, and what did you change?**
Needs specifics: hardcoded values, missing templating, chart sprawl, version pinning issues — and your fix.

**Q: How do Flux and Ansible divide responsibilities in your CI/CD pipeline?**
Should be able to draw the line cleanly: Flux = GitOps continuous deployment/reconciliation from a repo state; Ansible = configuration management / provisioning. If your setup blurs that line, explain how and why.

**Q: Walk me through what Prometheus/Grafana/Splunk each do in your monitoring stack — don't just list them.**
Needs: what metrics Prometheus scrapes, what dashboards you actually built in Grafana, what you use Splunk for that the others don't cover (usually log aggregation/search).

---

## 4. F-35 OBPHM — Test Automation

**Q: You reduced a 30-minute manual process to seconds. What was the actual bottleneck, and what did you change?**
This number invites scrutiny — be ready to explain mechanism, not just outcome: was the bottleneck manual data entry/lookups, repeated recomputation, or slow serial processing of the tabular data? What made it fast — vectorized pandas operations, caching, eliminating manual steps entirely?
*Follow-up trap:* "Was that 30 minutes mostly compute time or mostly a human doing manual steps?" — the honest answer changes what the achievement actually demonstrates.

**Q: What kind of data pipeline did you build for engine health monitoring — batch or streaming? What tools?**
Needs actual pipeline shape: ingestion source (what format is the raw F-135 sensor/regression data in — CSV, exported logs?), what transformations you applied to the tabular data (cleaning, reshaping, aggregating across regression cycles), and where the output lands.
*Follow-up trap:* Since this is described as tabular rather than multi-table relational data, be ready to say plainly whether there was any join/merge logic at all, or whether it was single-table transformation (filtering, reshaping, computing derived columns). Don't imply relational complexity that isn't there — a simpler, well-optimized tabular pipeline is still a legitimate win, and overstating it is an easy thing for an interviewer to unravel with one follow-up.

---

## 5. RAG Pipeline / Prior Authorization Project (your differentiator — expect the deepest questions here)

**Q: Walk me through your chunking strategy. Why that approach?**
Needs: fixed-size vs. semantic vs. recursive chunking, chunk size/overlap chosen, and *why* — e.g., LCD policy documents have structured sections, so chunking by section/heading preserves context better than fixed token windows.
*Follow-up trap:* "What happens when a requirement spans two chunks?" — if you haven't handled this, say so honestly rather than inventing a fix on the spot.

**Q: Which sentence-transformer model did you use, and how did you evaluate retrieval quality?**
If you didn't do formal evaluation (precision/recall on a labeled query set), don't claim you did. A credible answer: "I did qualitative spot-checks against known policy requirements rather than a formal eval set — that's a known gap I'd want to close with a labeled benchmark."

**Q: Why Groq instead of OpenAI or Anthropic's API for this pipeline?**
Needs a real tradeoff: inference speed/latency, cost per token, or model availability — not just "it was available."

**Q: How does the ICD-10/CPT coding logic actually get grounded? Is the LLM inferring codes, or is there a rules layer?**
This is the single most important question to nail — it's the easiest part of the pitch to hand-wave. Be precise: is retrieval pulling passages that *contain* the codes (so the LLM extracts rather than infers), or is there a separate lookup/validation step against a codebook? If the LLM is generating codes from context without a hard validation step, that's a real limitation — say so, because a good interviewer will find the gap anyway, and naming it yourself reads as engineering maturity rather than a weakness.

**Q: What does Pydantic actually validate in this pipeline, and what happens when the LLM's output doesn't conform?**
Needs: schema shape (fields for requirement, code, denial-prevention guidance), and your actual failure handling — retry with a corrective prompt? Reject and log? Best-effort parse?

**Q: Walk me through one real LCD policy end to end — ingestion to final checklist output.**
Have one specific example memorized cold: the policy name/topic, what the raw document looked like, what got chunked, what got retrieved for a sample query, and what the final structured output was.

---

## 6. Cross-cutting / behavioral

**Q: You've moved from IC to tech lead to Scrum Master responsibilities in under a year. What's been the hardest part of that transition?**
Needs a real tension — e.g., context-switching cost, delegating code you'd normally write yourself, or a time you over- or under-stepped as "lead."

**Q: Why the M.S. in Data Science alongside a defense software engineering career — how do the two connect for you going forward?**
Should tie your independent ML projects (RAG, healthcare tooling) to a coherent narrative about where you want to go next, not two disconnected tracks.

**Q: Everything on this resume is impressive — what's something you'd do differently if you rebuilt one of these projects today?**
Have one honest answer ready (e.g., "I'd build a real eval harness for the RAG pipeline from day one instead of relying on spot checks"). Interviewers trust self-critique more than polish.

---

## How to use this
Run through each section out loud, not just in your head — the gap between "I know this" and "I can say this fluently in 45 seconds" is usually where interviews go sideways. The Kyverno deadlock, the RAG grounding mechanism, and the 30-minutes-to-seconds claim are your three highest-risk spots — those are where padding is easiest to spot and hardest to recover from live.