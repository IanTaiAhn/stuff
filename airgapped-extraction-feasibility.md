# Airgapped & PHI-Restricted Extraction Agents: A Feasibility Brief

**Prepared:** August 17, 2026
**Question addressed:** Can a self-hosted, multi-agent extraction pipeline (the "classify → split → parse → extract → validate" pattern, sometimes called MADP) approach the accuracy of frontier hosted LLMs with very large context windows, when deployed in an airgapped or PHI-restricted environment with no external API access?

**Epistemic status:** Moderate-to-high confidence on the architectural claims (multiple independent lines of evidence converge). Lower confidence on precise numbers — the strongest quantitative source available is a single 2026 benchmark study that has not, as far as I found, been independently replicated, and it uses model versions that are already a generation behind the current frontier. Where I'm extrapolating rather than citing direct evidence, I've flagged it.

---

## How this brief was built

This is a synthesis of open-web research conducted in a single session (web search plus one full-text paper fetch), not a lab experiment. The research covered five separate lines of inquiry, each feeding a different part of the final answer:

1. **Current saturation of document-extraction verticals** (lease abstraction, insurance claims, customs declarations) — established the market context that motivated the technical deep-dive in the first place.
2. **The extraction infrastructure layer** (Reducto, LlamaParse/LlamaExtract, Unstructured, Extend, Docling, Datalab Lift) — established that parsing/extraction has become a commoditized, composable set of APIs rather than something built from scratch.
3. **Human-in-the-loop and active-learning architecture patterns**, including one directly relevant preprint describing a five-stage pipeline with a correction feedback loop.
4. **Long-context degradation research** ("lost in the middle" / "context rot") — this is what let me question the premise that a huge context window is the main thing an airgapped system is missing.
5. **A controlled multi-agent orchestration benchmark and the current (Aug 2026) open-weight model landscape** — this supplied the actual numbers behind the feasibility verdict.

The reasoning chain runs: *(a)* published research shows large-context accuracy gains are smaller and more fragile than advertised context-window sizes imply → *(b)* a controlled benchmark shows a well-orchestrated open-weight pipeline gets within a few F1 points of a frontier model doing single-shot extraction, using a now-dated open model → *(c)* a live example (NuExtract 3) shows a small model fine-tuned specifically for extraction can beat a larger general model on that narrow task → *(d)* therefore the "enterprise-level performance" gap is closable for narrow, repeated extraction work, through orchestration and fine-tuning rather than through raw context size or model scale. Each link in that chain is cited below.

---

## Part I — Why this question came up (brief recap)

Earlier research in this conversation found that three "obvious" extraction verticals — commercial lease abstraction, insurance claims processing, and customs declaration processing — are already served by multiple competing vendors, not open gaps [1][2][3][4][5][6]. That research also surfaced a horizontal "extraction infrastructure" layer (Reducto, LlamaParse/LlamaExtract, Unstructured, Extend, Datalab Lift) that most vertical products are quietly built on top of, offering composable parse/classify/split/extract/edit APIs with confidence scores and citations built in [7][8][9]. A recent preprint describing a five-agent pipeline (Classificator, Splitter, Parser, Extraction, Validator) with a feedback loop for continuous improvement without model retraining provided the reference architecture (referred to informally as "MADP") [10]. Standard human-in-the-loop practice routes only low-confidence output to a person, with corrections logged as future training signal [11].

None of that research, however, addressed environments where the document data legally or physically cannot reach a hosted API — which is the question this brief answers.

---

## Part II — Feasibility of airgapped / PHI-restricted extraction

### 1. The "large context window" advantage is smaller and less reliable than it looks

A body of independent research — spanning Stanford/University of Washington's original study and several 2025–2026 follow-ups across different model families — documents a consistent "lost in the middle" effect: LLM accuracy on multi-document retrieval and question-answering tasks follows a U-shaped curve, highest when the relevant evidence sits at the start or end of the context and 20–30 points lower when it sits in the middle [12]. A separate, compounding failure mode — "context rot" — shows accuracy declining as input length grows even when the relevant evidence is well-positioned; one controlled study found reasoning accuracy falling from 92% to 68% as inputs grew from a few hundred to three thousand tokens, and this pattern held even in models specifically advertised for long-context use [13].

**Implication:** a model's advertised context window is not a reliable proxy for how well it will actually use a long, messy real-world document. Decomposing a document into the sections that matter before extraction (the "classify → split" stage of the MADP pattern) is not merely a workaround for lacking a huge context window — the research suggests it is close to the correct approach regardless of context budget.

### 2. Controlled evidence: orchestration architecture closes most of the model gap

The strongest quantitative evidence found is a 2026 benchmark study (Kulkarni & Kulkarni, NYU) comparing four multi-agent orchestration patterns — sequential, parallel fan-out, hierarchical supervisor-worker, and reflexive self-correcting — across five models (three frontier: GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro; two open-weight, self-hostable: Llama 3 70B, Mixtral 8x22B) on 10,000 real SEC filings, 25 extraction field types [14].

Selected results (field-level micro-F1):

| Architecture | GPT-4o | Claude 3.5 Sonnet | Llama 3 70B (open, self-hostable) | Mixtral 8x22B (open, self-hostable) |
|---|---|---|---|---|
| Sequential | 0.897 | 0.903 | 0.834 | 0.812 |
| Parallel fan-out | 0.908 | 0.914 | 0.851 | 0.829 |
| **Hierarchical** | **0.921** | **0.929** | **0.869** | 0.843 |
| Reflexive | 0.936 | 0.943 | 0.878 | 0.851 |

Two findings matter most for this brief:

- **Hierarchical Llama 3 70B (0.869) landed within three points of sequential GPT-4o (0.897)** — a self-hostable model, run with no internet access required, approaching a frontier hosted model's single-shot performance purely through better orchestration.
- **Hierarchical architecture was also the best cost-accuracy tradeoff overall**, reaching 98.5% of the best-observed (reflexive) F1 at roughly 61% of the cost. Reflexive scored highest but its dominant failure mode — 39% of its errors — was the correction loop oscillating between interpretations on genuinely ambiguous text, and its accuracy collapsed under high processing volume due to timeout-truncated correction cycles. The paper's authors recommend hierarchical as the production default for most cases.

**Caveat:** this study used models that are now roughly 1.5–2 years old (GPT-4o, Claude 3.5 Sonnet, Llama 3 70B). Current open-weight options (DeepSeek V4, Qwen3 235B, Llama 4, GLM-5.2) are reported to be meaningfully stronger [15], so the real gap today is plausibly smaller — but I found no equally controlled benchmark using current-generation models to confirm this by how much.

### 3. Domain-specific fine-tuning can flip the gap entirely — for narrow tasks

Extraction is a narrower task than general reasoning, and there is a concrete, current example of a small fine-tuned model beating a larger general one specifically on it: NuExtract 3, a 4-billion-parameter open-weight model fine-tuned specifically for structured extraction, beat a general-purpose 9-billion-parameter model by 17 points on a 600-document benchmark spanning invoices, contracts, and forms — at less than half the parameter count [16]. It is Apache 2.0 licensed, fits on a single consumer GPU (12–16GB), and runs with no data leaving the host machine [17].

The NYU benchmark's own authors independently flagged this same direction as their top recommendation for future work, noting that in their model-routing experiments, task-specific smaller models handled 60–70% of extraction tasks without measurable quality loss compared to routing everything to the strongest model [14].

**Implication:** for a narrow, repeated document type — which is exactly what most airgapped/PHI extraction use cases look like — a small model fine-tuned on your own corrected examples is a more promising lever than trying to match a frontier model's general-purpose scale.

### 4. Current open-weight models suitable for self-hosting (as of August 2026)

Reported current options span a wide hardware range: DeepSeek V4 Flash is positioned as a default pick for high-volume extraction/classification workloads; Qwen3 235B-A22B (Apache 2.0) and Llama 4 are cited as strong general options; NuExtract 3 (4B) and distilled DeepSeek-R1 variants (1.5B–70B) are cited as options that run on consumer-grade GPUs rather than multi-GPU clusters [15][18]. Larger MoE models (Kimi K3, GLM-5.2) generally require multi-GPU A100/H100-class infrastructure [18]. Practitioner guidance generally frames self-hosting as most economical above roughly 10–30 million tokens/day of volume, and as the clear right call — independent of cost — under strict data-residency requirements [19].

### 5. Validation checks add accuracy for free, independent of model quality

The NYU benchmark's verifier agent applies deterministic, non-LLM checks — for example, a balance-sheet identity check (assets = liabilities + equity) — alongside LLM-based grounding checks [14]. These catch a category of error regardless of which model is running underneath, and cost effectively nothing per check. This is the one part of the pipeline where accuracy is not gated by model capability at all — it is a design decision that any airgapped deployment can and should include.

### 6. Human review carries more weight without a cloud fallback

Standard human-in-the-loop design routes only low-confidence fields (commonly the hardest ~5% of cases) to a reviewer, with active learning feeding corrections back into the system [11]. In a hosted-API deployment, a hard case can be escalated to a larger cloud model as a fallback. In an airgapped deployment, that fallback does not exist — the confidence threshold and the review queue become the actual safety net, which argues for calibrating thresholds more conservatively than a cloud-connected system would need to.

### 7. On-premises deployment for PHI is a recognized architecture, not a workaround

Independent of this benchmark evidence, current industry guidance for healthcare AI explicitly frames self-hosted open-weight models as the correct architecture for strict on-premises requirements — not a fallback for organizations that can't get a hosted contract — specifically because no patient data transits a vendor API and the model can be fine-tuned on an organization's own clinical terminology [20]. Commercial extraction vendors are also beginning to formalize PHI-safe, on-premises/zero-data-retention deployment paths for systems like Epic and Cerner, which further indicates this is a recognized production pattern in the market rather than a fringe one [21].

---

## Feasibility verdict

**Short version: feasible, with real conditions attached — and the airgap itself is not the limiting factor.**

- **Nothing about being airgapped inherently caps achievable accuracy.** The entire pipeline — model serving, extraction agents, validation, review UI, correction logging — can run inside a network boundary with no internet access. The airgap constrains *engineering convenience* (no elastic scaling, no easy model upgrades, no cloud fallback for hard cases), not the ceiling on what the system can eventually achieve.
- **For narrow, repeated, well-defined document types** — which describes most regulated-data extraction use cases — the combination of hierarchical orchestration, deterministic validation, and a model fine-tuned on your own corrected examples is a credible path to within single-digit F1 points of a frontier hosted model's single-shot performance, based on the controlled evidence above. This is the scenario the evidence most directly supports.
- **For open-ended, ambiguous, or reasoning-heavy extraction** (genuinely unclear disclosure language, cross-document inference, tasks requiring broad world knowledge) — the gap is real and will likely persist. The reflexive architecture's own dominant failure mode (oscillating on ambiguous text) is a reminder that more agentic machinery does not substitute for raw model reasoning capability in genuinely hard cases.
- **The single largest lever is not architecture — it's your own correction data.** Every piece of evidence above (the NYU paper's routing ablation, the NuExtract 3 result) points the same direction: a small model tuned tightly on your actual documents outperforms a much larger general model on that narrow task. This is also the one advantage a cloud-API approach cannot offer at all, since a hosted frontier model cannot be fine-tuned on data that never left your network.

**What I could not verify:** I found no benchmark that tests this exact configuration (MADP-style pipeline, current-generation open-weight model, genuinely airgapped hardware, PHI-type documents) end to end. The feasibility verdict above is a reasoned extrapolation from adjacent, credible evidence — not a direct measurement. Before committing significant engineering time, running your own small-scale benchmark against a frontier hosted model (on non-sensitive or synthetic documents, before any PHI is involved) would be the natural next step to validate these numbers against your specific document type.

---

## References

1. Lextract — "Best AI Lease Abstraction Software in 2026: Full Comparison." https://lextract.io/resources/comparisons
2. The AI Consulting Network — "Best AI Lease Abstraction Software: 2026 Comparison." March 5, 2026. https://www.theaiconsultingnetwork.com/blog/best-ai-lease-abstraction-software-2026-comparison
3. DDee.ai — "Best AI Lease Abstraction Software 2026 | Top 10 Compared." Feb 1, 2026. https://ddee.ai/resources/guides/best-lease-abstraction-software-2026
4. Infrrd — "Best Document Processing Software For Insurance Claims In 2026." April 14, 2026. https://www.infrrd.ai/blog/best-document-processing-software-for-insurance-claims-2026
5. Kognitos — "The 10 Best AI Tools for Insurance Claims Processing in 2026." May 8, 2026. https://www.kognitos.com/blog/ai-tools-for-insurance-claims-processing/
6. Digicust — "Beyond OCR: AI Customs Document Processing." June 6, 2026. https://digicust.com/en/blog/moving-beyond-ocr-future-automated-customs-clearance/
7. Reducto (llms.reducto.ai) — "Docling vs LlamaParse vs Unstructured vs Reducto: Document Parser Comparison." https://llms.reducto.ai/document-parser-comparison
8. Reducto — "Reducto vs LlamaParse | Agentic Document Platform vs Parser." https://reducto.ai/compare/reducto-vs-llamaparse
9. MarkTechPost — "Datalab Lift vs the Field: How a 9B Schema-First Extractor Compares with NuExtract3, LlamaExtract, Marker, and Docling." July 9, 2026. https://www.marktechpost.com/2026/07/09/datalab-lift-vs-the-field-how-a-9b-schema-first-extractor-compares-with-nuextract3-llamaextract-marker-and-docling/
10. arXiv — "MADP: A Multi-Agent Pipeline for Sustainable Document Processing with Human-in-the-Loop." https://arxiv.org/pdf/2605.17159
11. Mindee — "The role of human-in-the-loop (HITL) in document automation." April 3, 2026. https://www.mindee.com/blog/what-is-human-in-the-loop-automation
12. GetMaxim — "Solving the 'Lost in the Middle' Problem: Advanced RAG Techniques for Long-Context LLMs." October 29, 2025. https://www.getmaxim.ai/articles/solving-the-lost-in-the-middle-problem-advanced-rag-techniques-for-long-context-llms/
13. TMLS (The Machine Learning Society) — "Context Rot: Why Long-Context LLMs Degrade." June 17, 2026. https://www.tmls.nyc/research/context-rot-mechanistic
14. Kulkarni, S. & Kulkarni, Y. (New York University) — "Benchmarking Multi-Agent LLM Architectures for Financial Document Processing: A Comparative Study of Orchestration Patterns, Cost-Accuracy Tradeoffs and Production Scaling Strategies." https://arxiv.org/pdf/2603.22651
15. Hugging Face / D. Shankar — "Best Open-Source LLM Models in 2026: Coding, Local, Agentic AI, Benchmarks, and License." May 14, 2026. https://huggingface.co/blog/daya-shankar/open-source-llms
16. 7minAI — "NuExtract 3 released — a 4B open-weight VLM that beats 9B Qwen at structured extraction (Apache 2.0)." May 25, 2026. https://7minai.com/news/nuextract-3-4b-vlm-release/
17. BuildMVPFast — "NuExtract3: Self-Hosted 4B VLM for Document Extraction." May 30, 2026. https://www.buildmvpfast.com/blog/nuextract3-open-weight-vlm-structured-extraction-self-hosted-2026
18. Thunder Compute — "Best Open Source LLMs (August 2026)." https://www.thundercompute.com/blog/best-open-source-llms
19. SitePoint — "Open-Source vs Commercial LLMs: The Complete Guide (2026)." https://www.sitepoint.com/opensource-vs-commercial-llms-the-complete-guide-2026/
20. ideas2it — "LLM Comparison 2026: Top Models for Enterprise Use." https://www.ideas2it.com/blogs/llm-comparison
21. Reducto (llms.reducto.ai) — "Reducto: The Complete Agentic Document Platform." https://llms.reducto.ai/

*All sources accessed August 17, 2026. Dates in brackets reflect each source's own publication date where available.*
