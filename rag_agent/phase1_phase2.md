# Internal RAG/agent tool — phase 1 & phase 2 plan

A self-hosted, local-model agent for surfacing and reasoning over internal documentation (and, later, structured enterprise data), built entirely on free/open-source software and running on a single NVIDIA RTX 30-series GPU.

---

## Goal

Let an agent answer questions grounded in internal documents — with sources and links — and, in a later phase, query structured enterprise data (databases) as a separate tool. Everything runs locally: no internal data leaves the machine, no per-seat licensing cost.

---

## Phase 1 — MVP: Ollama + Open WebUI

**Objective:** prove the core loop works — a local model, retrieving from real internal docs, giving usable answers — before investing in a heavier stack.

### Components

| Piece | Choice | Why |
|---|---|---|
| Inference runtime | Ollama | No telemetry, MIT-licensed, direct GGUF pulls from Hugging Face |
| Harness / chat UI | Open WebUI | Free self-hosted (no branding restriction under 50 users), built-in RAG, points at any Ollama/OpenAI-compatible backend |
| Model | `qwen3.5:9b`, Q4_K_M quant | Strong local tool-calling/reasoning at ~6–8GB VRAM — fits an 8GB+ RTX 30-series card. Drop to `qwen3.5:4b` on lower-VRAM cards (6GB) |
| Embedding model | `nomic-embed-text` | Small (~275MB), runs fine alongside the main model |
| Deployment | `docker-compose.yml` (provided) | GPU passthrough via NVIDIA Container Toolkit |

### Setup steps

1. Confirm GPU visibility: `nvidia-smi`, and install the NVIDIA Container Toolkit so Docker can see the GPU.
2. `docker compose up -d` to bring up Ollama + Open WebUI.
3. Pull models into the running Ollama container: `qwen3.5:9b` and `nomic-embed-text` (one-time, needs internet).
4. In Open WebUI: set the embedding model, then create a **Knowledge** collection and upload/point it at an internal doc export.
5. Query the collection directly in chat (`#collection-name`) and sanity-check answers against docs you already know well.

### Evaluation

- Run **EnterpriseRAG-Bench** (Onyx's open, MIT-licensed benchmark simulating Slack/Confluence/Jira/Drive/GitHub-style internal docs) as a rough sanity check on the model + retrieval combo.
- Use **RAGAS** to auto-generate a small question/answer set from your *actual* internal docs and score faithfulness, answer relevancy, and context precision/recall — this is the number that actually matters, since it's your data, not a simulated corpus.

### Known limitations (by design — this is the MVP, not the end state)

- Single-shot retrieval only — no multi-hop research or query reformulation.
- No native connectors — docs go in via manual upload/export, not live sync from Confluence/Jira/etc.
- No inline citations back to the source system, no permission-awareness (ACLs).
- RAG quality needs manual tuning (chunk size, retrieval settings) — not zero-config.
- Built for a personal/small-team scale, not multi-user production load.

### Exit criteria → move to Phase 2

Move on once Phase 1 proves the core value (people actually use it, answers are useful) **and** the gaps that show up are specifically: need for live connector sync, need for citation-backed sourcing, or need for multi-step research across documents — all things Phase 2 adds directly.

---

## Phase 2 — Onyx Community Edition

**Objective:** add the agentic research layer, native connectors, and citation-rich sourcing, without changing the underlying model or hardware.

### What Onyx CE adds on top of Phase 1

| Capability | Detail |
|---|---|
| Deep Research | Multi-step agentic search: reformulates the query, runs multiple retrieval passes, synthesizes a cited report — not single-shot RAG |
| Native connectors | 40+ connectors (Confluence, Jira, GitHub, Slack, Google Drive, and more), with continuous sync and permission syncing |
| Citations | Inline citations linking answers back to the source document/page |
| Optional web search | Pulls in current external articles alongside internal docs (disable if fully air-gapped) |
| Optional DB tool | Add an MCP server (e.g. Google's MCP Toolbox for Databases, or a Snowflake/Postgres-specific server) as a second tool alongside document RAG, for structured-data queries |

### License / cost

Onyx **Community Edition is MIT-licensed and free**, and covers all of Chat, RAG, Agents, Actions — Deep Research is part of that core set, not gated. Enterprise Edition only gates governance features (SSO, SCIM, group-based permission inheritance, dedicated support) — not needed at small-team scale.

### Hardware note

Onyx is a heavier stack than Phase 1 — it adds its own Postgres, Redis, vector index, and separate indexing/inference model-server containers. It still runs on the same single-GPU machine; the model inference backend (Ollama) doesn't change. Onyx's own guidance recommends a recent, non-quantized model for best Deep Research quality — quantized still works, just worth validating against your own docs (via the RAGAS eval loop from Phase 1) before deciding whether the quality bar is acceptable.

### Air-gapped note (if relevant)

Fully supported — zero outbound traffic once set up. Standard approach: assemble docker images + model weights on a connected machine, transfer into the closed network as a bundle (sneakernet or one-way data diode), verify hashes. Disable the optional web-search connector, since there's no external web to reach.

---

## Summary comparison

| | Phase 1 | Phase 2 |
|---|---|---|
| Stack complexity | Ollama + Open WebUI (2 containers) | + Onyx CE (Postgres, Redis, vector index, model servers) |
| Retrieval style | Single-shot RAG | Multi-step agentic Deep Research |
| Doc ingestion | Manual upload/export | Live-syncing connectors |
| Citations | No | Yes, inline, linked to source |
| Structured data (DB) tool | Not included | Optional, via MCP server |
| Cost | Free | Free (Community Edition) |
| Time to stand up | Same afternoon | Days, given added infra |

---

## References

- Ollama: https://github.com/ollama/ollama
- Open WebUI: https://github.com/open-webui/open-webui
- Onyx: https://github.com/onyx-dot-app/onyx
- EnterpriseRAG-Bench: https://github.com/onyx-dot-app (search "EnterpriseRAG-Bench") / HuggingFace
- RAGAS: https://github.com/explodinggradients/ragas
- Google MCP Toolbox for Databases: https://github.com/googleapis/genai-toolbox
