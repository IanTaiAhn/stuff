# Fine-Tuning a Small Language Model: A Learning Project

A hands-on project guide for going from "I've never fine-tuned anything" to "I have a specialised model serving locally and I know whether it actually helped."

The task used throughout is **structured extraction from messy text into a strict JSON schema**. It's chosen deliberately: correctness is mechanically measurable, ground truth is cheap to produce, and it sits in the one category where fine-tuned small models have documented production wins.

---

## Table of contents

1. [Mental model: what fine-tuning actually is](#1-mental-model)
2. [Distillation, disambiguated](#2-distillation-disambiguated)
3. [The ladder: cheapest intervention first](#3-the-ladder)
4. [Where Ollama fits (and doesn't)](#4-where-ollama-fits)
5. [The project](#5-the-project)
6. [Milestone-by-milestone walkthrough](#6-milestone-walkthrough)
7. [Configuration reference](#7-configuration-reference)
8. [Failure modes and how to spot them](#8-failure-modes)
9. [Extending to tool-calling](#9-extending-to-tool-calling)
10. [Further reading](#10-further-reading)

---

## 1. Mental model

**You are not changing the architecture.** No new layers, no added activation functions, no modified output head. The network stays exactly as it shipped.

What you are doing is nudging the existing weights with gradient descent on examples of the behaviour you want. The model already knows how to read English and emit JSON; fine-tuning makes it do *your* version of that reliably, in *your* format, without needing a 2,000-token prompt to explain itself every time.

Three things fine-tuning is genuinely good at:

| Goal | Does fine-tuning help? |
|---|---|
| Locking output format / schema compliance | **Yes — this is the strongest case.** Typical reports: 70–80% compliance with prompting to 95%+ after tuning. |
| Domain vocabulary and narrow terminology | **Yes.** 15–30 point accuracy gains on tasks like medical coding or internal taxonomies, with 2k–10k examples. |
| Cutting latency and cost on a hot path | **Yes.** Self-hosted 7B at a fraction of frontier API cost and latency. |
| Adding knowledge the model lacks | **No — use RAG.** Fine-tuning teaches behaviour, not facts. |
| Making a model smarter in general | **No.** It narrows the model; it does not raise its ceiling. |

---

## 2. Distillation, disambiguated

The word carries at least three distinct meanings, and they get conflated constantly.

### 2a. Classical knowledge distillation (Hinton-style)

A large **teacher** and a small **student** both process the same input. The student is trained to match the teacher's *full output probability distribution* over the vocabulary at each token position — not just its final answer.

The insight: the teacher's wrong answers carry information. If the teacher assigns 70% to `cat`, 20% to `dog`, and 0.001% to `carburetor`, that relative structure encodes something a bare label `cat` does not.

Requires white-box access to teacher logits. Only possible with open-weight teachers.

### 2b. Sequence-level / synthetic-data distillation

Prompt a strong model, collect its **text outputs**, fine-tune a smaller model on those input→output pairs as though a human had written them.

No logits needed. Works through any API. **This is what "distillation" almost always means in a fine-tuning context**, and it's what this project uses. Strictly it is imitation learning rather than distillation, but the name stuck.

> Check the terms of service of whatever model you distil from. Some providers restrict using outputs to train competing models.

### 2c. Reasoning-trace distillation

Capture the teacher's full chain of thought, not just the final answer, and train on the traces. The DeepSeek-R1-Distill family (1.5B–8B, trained on R1-generated samples) is the canonical example.

### 2d. "Distillation" as marketing

Some model cards say "distilled" when what actually happened was pruning plus continued pretraining. When it matters, check the technical report rather than the card.

---

## 3. The ladder

Work down this list. Most tasks stop at step 2 or 3.

1. **Build an eval harness.** Non-negotiable, and covered below.
2. **Prompt properly.** Rigid schema, 5–10 few-shot examples, constrained decoding for structured output.
3. **RAG**, if the gap is missing knowledge rather than missing behaviour.
4. **LoRA / QLoRA supervised fine-tuning.** The subject of this project.
5. **Full-parameter fine-tuning.** Rarely worth it for narrow tasks.
6. **DPO or other preference optimisation.** Only after SFT, and only when correctness is a matter of *degree* rather than a single right answer.

### The rule that saves the most time

> Prototype with a frontier model first. If good prompt engineering with a state-of-the-art model cannot make the task work, fine-tuning a smaller model will not rescue it.

### When to skip to step 4 anyway

- Prompting reaches ~85% and you need ~95%.
- Prompting works but you need it 50× cheaper or 10× faster.
- Data cannot leave your network.

---

## 4. Where Ollama fits

**Ollama does not train.** It's an inference runtime — llama.cpp with a good wrapper. No optimiser, no backward pass, no training loop.

It is, however, a fine *destination*. The pipeline is:

```
Unsloth / Axolotl  →  adapter (safetensors) or merged GGUF  →  Ollama serves
```

Importing an adapter:

```dockerfile
# Modelfile
FROM qwen3.5:7b
ADAPTER ./my-adapter
```

```bash
ollama create my-extractor
ollama run my-extractor
```

### Three gotchas, in order of how much time they'll cost you

1. **Base model must match exactly.** The `FROM` base must be the same weights you trained against. An adapter trained on HuggingFace bf16 weights applied to a differently-quantised Ollama base produces output that is *subtly* wrong rather than obviously broken — the worst failure mode there is.

2. **Prefer non-quantised adapters.** Ollama's docs recommend against importing QLoRA adapters directly, because frameworks use different quantisation methods that don't compose cleanly. Train with QLoRA if you must for memory reasons, but merge into bf16 before converting.

3. **Verify architecture support.** Adapter import has historically covered Llama, Mistral, and Gemma families. Confirm your specific model is supported in the version you're running before committing to the adapter path.

### The fallback that always works

If adapter import isn't supported for your model, merge the adapter into the base weights yourself, convert to GGUF with llama.cpp's conversion script, and import the merged model as a standalone:

```dockerfile
FROM ./my-merged-model-q4_k_m.gguf
```

---

## 5. The project

**Task:** extract a fixed set of fields from unstructured text into strict JSON.

Pick one corpus:

| Corpus | Fields to extract | Notes |
|---|---|---|
| Job postings | title, seniority, remote_policy, salary_min, salary_max, currency, required_skills[] | Messy, plentiful, good field-type variety |
| Receipts / invoices | vendor, date, total, currency, line_items[] | Numeric fields expose hallucination clearly |
| Academic abstracts | venue, year, method_names[], dataset_names[], reports_code_release | Closest to the papers you've been reading |

Fix the schema **before** you generate any data and do not change it afterwards. Schema churn invalidates both your training set and your eval set.

### Why this task

- **Unambiguous correctness.** Field-by-field exact match gives a clean F1. No LLM-as-judge, no subjective calls.
- **Two independent metrics.** Parse rate (is it valid JSON with the right keys?) and field accuracy (are the values right?). Fine-tuning usually improves the first dramatically and the second modestly — seeing that split is the lesson.
- **It's real work.** Bounded, high-volume, single-turn extraction is the one category where fine-tuned small models have documented production wins.

### What you'll need

- Python 3.10+, a GPU with 12GB+ VRAM, or free Colab / a rented A10.
- Ollama installed locally.
- API access to one frontier model for data generation.
- Roughly two weeks of calendar time, of which about two hours is actual training.

---

## 6. Milestone walkthrough

### M0 — Freeze the schema

Write it as a JSON Schema file. Decide now:

- Which fields are required vs nullable?
- What is the exact representation for "not present"? (`null`, `""`, omitted key — pick one and enforce it everywhere)
- Are arrays ordered? Deduplicated? Case-normalised?

Ambiguity here becomes noise in your training targets, and noisy targets teach the model to be uncertain.

### M1 — Eval harness (do this first)

**200 examples with hand-verified ground truth.** Yes, by hand. This is the foundation everything else is measured against.

`eval.py` should take a model endpoint and print:

```
parse_rate      : 0.94    # fraction returning valid JSON matching the schema
field_f1        : 0.81    # macro-averaged across fields
per_field_f1    : {title: 0.95, salary_min: 0.62, ...}
latency_p50_ms  : 420
latency_p95_ms  : 890
```

Per-field breakdown matters. Aggregate F1 hides the fact that one field is dragging everything down, and that field usually has a schema problem rather than a model problem.

### M2 — Prompt baseline

Few-shot prompt the base `qwen3.5:7b` through Ollama. Use constrained/grammar-based decoding if available — it's the fair comparison, since it's cheap and it's what you'd do in production anyway.

**Write the number down.** This is what you have to beat.

It is entirely possible you'll find the baseline already hits 95% and the fine-tune buys three points. That is a real result, not a failed project — calibrating when fine-tuning is worth it is the actual skill.

### M3 — Generate training data

Target **2,000 examples**. Distil from a frontier model (sense 2b above).

Then:

- **Hand-check 100 of them.** You will find errors. Fix or drop.
- **Deduplicate against the eval set.** Near-duplicate detection, not just exact match. Leakage here invalidates every number that follows.
- **Normalise formatting ruthlessly.** If 10% of your targets have a trailing newline and 90% don't, the model learns that trailing newlines are a coin flip.

Training format — chat messages, loss masked to the assistant turn:

```json
{"messages": [
  {"role": "system", "content": "Extract fields into JSON matching the schema. Output JSON only."},
  {"role": "user", "content": "<raw document text>"},
  {"role": "assistant", "content": "{\"title\": \"Senior Backend Engineer\", \"salary_min\": 140000, ...}"}
]}
```

> **Check the chat template before formatting anything.** Pull the tokenizer config and inspect `chat_template`. Qwen3-series models shipped with a hybrid thinking mode; if the template expects `<think>` blocks and your data omits them, you get format drift that's hard to diagnose later.

### M4 — Train

QLoRA in Unsloth. Config in [section 7](#7-configuration-reference). Two to three epochs, watch eval loss, stop when it turns up.

Expect the run itself to take 30–120 minutes on a single consumer GPU.

### M5 — Evaluate

Run `eval.py` against the tuned model. Compare to M2.

**If the numbers didn't move, the problem is almost always data.** Resist the urge to sweep learning rates. Go look at 50 random training examples instead — you will find an inconsistency.

### M6 — Merge, convert, serve

Merge the adapter to bf16, convert to GGUF, import to Ollama, **run `eval.py` a third time against the served model**.

This third run is the one people skip, and it's where quantisation regressions and chat-template mismatches surface. A 4-point drop between M5 and M6 is common and entirely fixable — but only if you measure it.

### M7 — Ablate one variable

Retrain on 500 examples instead of 2,000. Compare.

That single experiment teaches more about the data-quantity/quality relationship than any amount of reading. Optional follow-ups: r=8 vs r=32, 2 epochs vs 5, with and without the system prompt.

---

## 7. Configuration reference

### Memory and cost for a 7B model

| Method | VRAM | Typical cost | Notes |
|---|---|---|---|
| Full fine-tune | ~60–80 GB | hundreds of $ | Rarely justified for narrow tasks |
| LoRA (bf16 base) | ~16–24 GB | $10–50 | One A100 or 4090 |
| QLoRA (4-bit base) | ~8–12 GB | < $10 | Consumer GPU / free Colab |

### Starting hyperparameters

```yaml
# Sensible defaults for narrow single-turn tasks
lora_r: 16                # 32 if task is complex; 8 if data is scarce
lora_alpha: 32            # conventionally 2 x rank
lora_dropout: 0.05
target_modules:
  - q_proj
  - k_proj
  - v_proj
  - o_proj
  - gate_proj
  - up_proj
  - down_proj

learning_rate: 2e-4       # 10-50x higher than full FT, which wants ~1e-5
num_epochs: 3
lr_scheduler: cosine
warmup_ratio: 0.03
max_seq_length: 2048      # set from your actual p99 example length
gradient_checkpointing: true

train_on_inputs: false    # CRITICAL - see note below
```

**`train_on_inputs: false` matters more than it looks.** Some trainers default to computing loss across the entire sequence including your prompt. You want loss masked to assistant tokens only, so the model learns to *produce* the output rather than to reproduce your prompts.

### Data quantity guidance

| Examples | Expectation |
|---|---|
| < 300 | Viable only for very narrow classification; high overfitting risk |
| 500–2,000 | Sweet spot for structured extraction |
| 2,000–10,000 | Sweet spot for tasks with real diversity |
| > 50,000 | Diminishing returns unless the task is genuinely broad |

800 clean, consistently-formatted examples beat 5,000 noisy ones. Reliably.

### Tooling

| Tool | Best for |
|---|---|
| **Unsloth** | Fastest single-GPU path, low memory, notebook-friendly. Good default for a first run. |
| **Axolotl** | YAML-driven, good multi-GPU and dataset handling. Better once you're iterating seriously. |
| **TRL + PEFT** | Most control, most boilerplate. `SFTTrainer` + `LoraConfig`. |
| **LLaMA-Factory** | Includes a UI if you want one. |

Don't write the training loop yourself. There's nothing to learn there that these don't teach you faster.

---

## 8. Failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| Eval loss drops, task metrics don't move | Loss computed over prompt tokens | Set `train_on_inputs: false` |
| Great train metrics, poor eval | Overfitting, or eval leakage | Fewer epochs; deduplicate train vs eval |
| Model memorises training answers | Too many epochs on small data | Stop at 2; lower rank |
| Output format drifts | Chat template mismatch | Inspect tokenizer `chat_template`, regenerate data |
| Works in training framework, broken in Ollama | Base model or quantisation mismatch | Verify `FROM` base; merge to bf16 before converting |
| Forces every input into the label set | Catastrophic forgetting / no negatives | Add out-of-scope examples with an "unknown" target |
| Numeric fields hallucinate plausibly | Model generating rather than extracting | Add explicit "only from source text" instruction; consider constrained decoding |

### The forgetting check

After training, throw the model **20 near-miss, out-of-scope inputs** and confirm it degrades sanely. A model tuned on 40 ticket categories will cheerfully classify a poem as `billing/refund_request` if you never taught it to abstain.

Abstention is a capability. Train for it explicitly.

---

## 9. Extending to tool-calling

Once extraction works, the natural next step is a small agent. Two constraints worth respecting:

**Keep it single-turn.** The benchmark evidence is consistent and brutal here: on the Berkeley Function Calling Leaderboard, multi-turn accuracy across a size ladder runs roughly 55% (3B) → 35% → 17% → 8% → 1.4% → 0% (1.1B). Sub-3B models collapse on multi-turn context retention. Starting there means fighting the hardest version of the problem while still learning the tooling.

**Prefer a single agent over multiple.** A 27-model study across three architectures found single-agent systems achieved the best effectiveness/cost balance, while multi-agent setups added coordination overhead with limited gains — completion rate fell from ~99.7% (base) to ~79.9% (single-agent) to ~72.0% (multi-agent), with token usage rising from ~2.4k to ~8k to ~14.6k per sample. Dominant multi-agent failure modes were delegation failures and context-length exhaustion.

### A reasonable tool-calling milestone

1. Define 3–4 fake tools with strict JSON schemas.
2. Generate traces where the model emits one correctly-formatted call.
3. Measure **call validity** (parses, tool exists, required args present, types correct) separately from **call correctness** (right tool, right arguments).
4. Only then consider adding a second turn.

---

## 10. Further reading

### Papers worth reading in this order

1. **Belcak et al., "Small Language Models are the Future of Agentic AI"** (arXiv 2506.02153) — the position argument, plus a six-step LLM-to-SLM conversion algorithm that generalises well. Read sections 3 and 6.
2. **Wang & Brorsson, "Rethinking Scale"** (arXiv 2604.19299) — the empirical counterweight. 27 models, three architectures, deployment metrics beyond accuracy. Read section 4.
3. **Haque et al., "TinyLLM"** (arXiv 2511.22138) — BFCL benchmarks establishing the sub-3B capability floor. *Note: the results tables have transcription errors; trust the ordering, not the exact per-subcategory figures.*
4. **Hu et al., "LoRA"** (arXiv 2106.09685) and **Dettmers et al., "QLoRA"** (arXiv 2305.14314) — the two methods you're actually using.

### Production case studies

- **Checkr** — background-check adjudication, 230 categories. GPT-4 at 80–82% on complex cases; fine-tuned Llama-2-7b at 85%; shipped llama-3-8b-instruct at 90% with 5× cost reduction and 0.15s latency. The most detailed public write-up of the pattern this project teaches.
- **ZenML LLMOps Database** — curated real-world implementations rather than vendor marketing. Filter by `classification` and `document_processing`.

### What to discount

Treat generic "SLMs in 2026" blog content as noise. Claims like "80% of production use cases run on models under 13B" circulate widely with no primary source. Vendor benchmarks from fine-tuning platforms are directionally plausible but not independent.

---

## Appendix: realistic time budget

| Phase | Time |
|---|---|
| Schema design | 0.5 day |
| Eval set + harness | 2 days |
| Training data generation and cleaning | 3–5 days |
| Actual training run | 2 hours |
| Iteration after finding a data bug | 2–3 days |
| Merge, convert, serve, re-verify | 1 day |
| Ablation | 0.5 day |

**Roughly two weeks.** The model training is the easy part, and almost none of the time goes there. If your plan allocates most of its effort to hyperparameters, the plan is wrong.
