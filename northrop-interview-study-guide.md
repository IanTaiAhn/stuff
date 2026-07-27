# Northrop Grumman — Principal/Sr. Principal AI Engineer — Study Guide

## Context: your background
NH-03, 1550 Computer Scientist = **GS-12/13 equivalent** federal band. Useful frame if grade/comp comes up in the call.

## Step 1 — Verify your clearance details (do this first, before the call)
Contact your **servicing security office / FSO directly** — they have DISS access, you don't (post-separation or even as a current employee, self-service isn't really a thing).

Ask them for exactly these three things:
- [ ] **Current eligibility level** (confirm it's Secret, active)
- [ ] **Investigation completion / adjudication date**
- [ ] **Any break in service or access gap** — matters if it's been over 24 months since you last held a cleared position

Also ask:
- [ ] Whether you've been enrolled in **Continuous Vetting (Trusted Workforce 2.0)** instead of periodic reinvestigation — this affects how you should answer "when was your reinvestigation" honestly and precisely
- [ ] Confirm you understand **SEAD 7 reciprocity** applies if you move from federal service to a contractor role — Northrop should accept your existing clearance without a new investigation, as long as it's current and in scope

**Have ready for the call:** eligibility level, investigation date, clearance type (Secret), citizenship status, SAP eligibility (may require separate discussion/sponsorship — ask your security office if you're unsure what this entails).

## Step 2 — What the call will probably look like
One 1-hour Teams call, likely combining:
1. Intro / "tell me about yourself" (60–90 sec, rehearsed but natural)
2. Resume deep-dive — expect them to pick 2–3 items and go deep
3. STAR-format behavioral questions
4. Clearance & logistics check (relocation to Roy, UT; travel 10%)

Technical assessment here is usually **conversational, via your resume**, not live coding.

## Step 3 — Technical focus areas (priority order)
1. **Local LLM deployment** — Ollama, Llama.cpp, quantization, VRAM/CPU tradeoffs, why this matters for restricted/air-gapped environments
2. **Multi-provider LLM APIs** — OpenAI, Anthropic, Google: prompting + fine-tuning differences
3. **Agentic frameworks** — LangChain/LangGraph; be ready to explain agent vs. simple prompt chain
4. **RAG pipeline design** — chunking, embeddings, vector store, retrieval + reranking
5. **Python + TypeScript/JS** — both named as core, not just Python
6. Secondary: graph DBs (Neo4j/Cypher), GNNs, classical ML/tracking — narrower but worth a baseline answer

## Step 4 — STAR stories to prep (pick 2–3, tailor to this role)
- [ ] Shipped an ML/AI feature to production
- [ ] Took a research paper/technique and made it deployable ("research mindset → practical solution")
- [ ] Navigated ambiguity or a technical disagreement on a project
- [ ] Managed integration challenges across a complex system or team

## Step 5 — Opening answers to rehearse out loud
- [ ] "Tell me about yourself" — background → AI/ML production experience → why this role
- [ ] "Why this role / why Northrop Grumman / why this mission"
- [ ] Be ready to speak plainly and confidently about clearance status — vague answers read worse than "let me confirm the exact date," so pin down Step 1 first
