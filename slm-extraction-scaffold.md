# slm-extraction-finetune

> Scaffold doc — drop this in as `README.md` of a fresh repo and start filling in the checkboxes. Background and rationale for every decision below live in `slm-finetuning-project.md` (the companion doc this was generated from); keep that alongside it as `docs/PROJECT_GUIDE.md` for reference.

**Goal:** fine-tune a small language model (target: `qwen3.5:7b` via QLoRA) to extract a fixed schema of fields from messy text into strict JSON, and prove — with numbers, at three separate checkpoints — whether the fine-tune actually helped over a prompted baseline.

**Chosen corpus:** _(pick one and delete the other two rows before committing M0)_

| Corpus | Fields | Notes |
|---|---|---|
| Job postings | `title, seniority, remote_policy, salary_min, salary_max, currency, required_skills[]` | Messy, plentiful, good field-type variety |
| Receipts / invoices | `vendor, date, total, currency, line_items[]` | Numeric fields expose hallucination clearly |
| Academic abstracts | `venue, year, method_names[], dataset_names[], reports_code_release` | Closest to papers-reading domain |

---

## 0. Repo layout

```
.
├── README.md                      # this file
├── docs/
│   └── PROJECT_GUIDE.md            # the full narrative doc (background, ladder, distillation, failure modes...)
├── schema/
│   └── extraction_schema.json      # M0 — frozen JSON Schema, single source of truth
├── data/
│   ├── raw/                        # untouched source documents
│   ├── eval/
│   │   └── eval_set.jsonl          # M1 — 200 hand-verified {input, target} examples
│   ├── train/
│   │   ├── train_full.jsonl        # M3 — ~2000 distilled examples
│   │   └── train_ablation_500.jsonl# M7 — subsample for the ablation run
│   └── dedup_report.json           # M3 — near-dup check output (train vs eval)
├── src/
│   ├── generate_data.py            # M3 — calls frontier model, writes chat-format jsonl
│   ├── eval.py                     # M1 — the harness; takes an endpoint, prints metrics
│   ├── metrics.py                  # parse_rate, per-field F1, latency percentiles
│   └── dedup.py                    # near-duplicate detection between train/eval
├── training/
│   ├── config.yaml                 # M4 — hyperparameters (see §7 of PROJECT_GUIDE)
│   └── train.py                    # Unsloth QLoRA training script (or notebook)
├── serving/
│   ├── Modelfile                   # M6 — Ollama import definition
│   └── merge_and_convert.sh        # adapter → bf16 merge → GGUF conversion
├── results/
│   ├── m2_prompt_baseline.json      # every eval.py run's output lands here, timestamped
│   ├── m5_finetuned.json
│   ├── m6_served.json
│   └── m7_ablation_500.json
├── requirements.txt
└── .gitignore                      # exclude data/raw, *.gguf, *.safetensors, venv/
```

---

## 1. Setup checklist

- [ ] Python 3.10+ environment (`venv` or `conda`)
- [ ] `requirements.txt` — start with: `unsloth`, `transformers`, `peft`, `trl`, `datasets`, `pydantic` (schema validation), `jsonschema`
- [ ] GPU: 12GB+ VRAM, or Colab / rented A10
- [ ] Ollama installed locally (`ollama --version`)
- [ ] API key for one frontier model (for data generation) stored in env var, not committed
- [ ] `.gitignore` covers model weights, adapters, raw scraped data, and API keys

---

## 2. Milestones → deliverables

Each milestone below is "done" only when its listed artifact exists and is committed. Copy this table into GitHub issues or a project board if useful.

### M0 — Freeze the schema
- [ ] `schema/extraction_schema.json` written and validated (`jsonschema` loads it without error)
- [ ] Decided and documented in-repo: required vs. nullable fields, the exact "not present" representation (`null` vs `""` vs omitted key — pick one), array ordering/dedup/case rules
- [ ] Schema is **frozen** — any change after this point requires regenerating both eval and train sets

### M1 — Eval harness (before any modeling work)
- [ ] `data/eval/eval_set.jsonl` — 200 hand-verified examples
- [ ] `src/eval.py` runs against any endpoint (prompted base model, fine-tuned adapter, or served Ollama model) and prints:
  ```
  parse_rate      : 0.94
  field_f1        : 0.81
  per_field_f1    : {title: 0.95, salary_min: 0.62, ...}
  latency_p50_ms  : 420
  latency_p95_ms  : 890
  ```
- [ ] Output is also written as JSON to `results/`

### M2 — Prompt baseline
- [ ] Few-shot prompt against base model in Ollama (constrained/grammar decoding if available)
- [ ] `results/m2_prompt_baseline.json` committed
- [ ] Number written down somewhere visible (top of this README's Results section, §8 below)

### M3 — Generate training data
- [ ] `src/generate_data.py` distills ~2,000 examples from a frontier model into the chat-format below
- [ ] Hand-checked 100 examples for errors (log findings in `data/train/hand_check_notes.md`)
- [ ] `src/dedup.py` run against eval set → `data/dedup_report.json`, zero leakage confirmed
- [ ] Formatting normalized ruthlessly (trailing whitespace, key order, etc. — pick one convention)
- [ ] Chat template checked against the target model's tokenizer config (`chat_template` inspected — watch for Qwen3's `<think>` hybrid mode)

  Target format:
  ```json
  {"messages": [
    {"role": "system", "content": "Extract fields into JSON matching the schema. Output JSON only."},
    {"role": "user", "content": "<raw document text>"},
    {"role": "assistant", "content": "{\"title\": \"...\", ...}"}
  ]}
  ```

### M4 — Train
- [ ] `training/config.yaml` filled in (start from defaults in `docs/PROJECT_GUIDE.md` §7)
- [ ] QLoRA run via Unsloth, 2–3 epochs, eval loss monitored, stopped when it turns up
- [ ] Adapter checkpoint saved (not committed to git — path noted in `.gitignore` and README)

### M5 — Evaluate the fine-tune
- [ ] `eval.py` run against the tuned adapter → `results/m5_finetuned.json`
- [ ] Compared against M2 baseline in §8 below
- [ ] If numbers didn't move: inspected 50 random training examples before touching hyperparameters

### M6 — Merge, convert, serve
- [ ] Adapter merged to bf16
- [ ] Converted to GGUF (`serving/merge_and_convert.sh`)
- [ ] `serving/Modelfile` written, `ollama create` run
- [ ] `eval.py` run a **third** time against the served Ollama model → `results/m6_served.json`
- [ ] Any drop vs. M5 investigated (quantization or chat-template mismatch)

### M7 — Ablate one variable
- [ ] Retrained on `data/train/train_ablation_500.jsonl` (500 examples)
- [ ] `results/m7_ablation_500.json` committed and compared to M5
- [ ] (Optional follow-ups) r=8 vs r=32, epochs 2 vs 5, with/without system prompt — log each as its own `results/m7_*.json`

### Forgetting check (do this once, after M5 or M6)
- [ ] 20 near-miss / out-of-scope inputs thrown at the model
- [ ] Confirmed it abstains sanely rather than force-fitting the schema
- [ ] If it doesn't: add out-of-scope examples with an explicit "unknown"/null target and retrain

---

## 3. Config reference (starting point for `training/config.yaml`)

```yaml
lora_r: 16
lora_alpha: 32
lora_dropout: 0.05
target_modules: [q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj]

learning_rate: 2e-4
num_epochs: 3
lr_scheduler: cosine
warmup_ratio: 0.03
max_seq_length: 2048   # set from actual p99 example length once data exists
gradient_checkpointing: true

train_on_inputs: false  # loss masked to assistant turn only — do not skip this
```

Full rationale, VRAM/cost table, and tooling comparison (Unsloth vs Axolotl vs TRL+PEFT vs LLaMA-Factory) are in `docs/PROJECT_GUIDE.md` §7.

---

## 4. Failure modes to check against

Before debugging hyperparameters, run through this table (full version in `docs/PROJECT_GUIDE.md` §8):

| Symptom | Likely cause |
|---|---|
| Eval loss drops, task metrics don't move | `train_on_inputs` not set to `false` |
| Great train metrics, poor eval | Overfitting or eval leakage — re-run `src/dedup.py` |
| Output format drifts | Chat template mismatch — re-inspect tokenizer |
| Works in training framework, broken in Ollama | Base model or quantization mismatch |
| Numeric fields hallucinate plausibly | Add "only from source text" instruction; consider constrained decoding |

---

## 5. Non-goals (things this project deliberately skips)

- No RAG — this project assumes the gap is behavior, not knowledge.
- No multi-turn tool-calling until extraction is solid (see `docs/PROJECT_GUIDE.md` §9 if extending later).
- No full-parameter fine-tune — QLoRA only, unless M4 results explicitly justify escalating.

---

## 6. Time budget (for planning, not a commitment)

| Phase | Time |
|---|---|
| Schema design (M0) | 0.5 day |
| Eval set + harness (M1) | 2 days |
| Training data generation and cleaning (M3) | 3–5 days |
| Training run (M4) | ~2 hours actual compute |
| Iteration after finding a data bug | 2–3 days |
| Merge, convert, serve, re-verify (M6) | 1 day |
| Ablation (M7) | 0.5 day |

---

## 7. Open decisions before starting

- [ ] Which corpus (job postings / receipts / abstracts)?
- [ ] Which frontier model for data generation, and confirm its ToS allows training a model on its outputs
- [ ] Which base model exactly — confirm adapter-import support in the installed Ollama version before committing (historically: Llama, Mistral, Gemma families; verify Qwen3.5 support explicitly)
- [ ] Compute: local GPU, Colab, or rented instance?

---

## 8. Results log

_Fill in as each milestone completes. This table is the actual point of the project._

| Milestone | parse_rate | field_f1 | latency_p50_ms | Notes |
|---|---|---|---|---|
| M2 — prompt baseline | | | | |
| M5 — fine-tuned (pre-serve) | | | | |
| M6 — served via Ollama | | | | |
| M7 — ablation (500 examples) | | | | |
