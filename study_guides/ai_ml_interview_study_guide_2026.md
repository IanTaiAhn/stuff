# AI / ML Engineer Interview Study Guide — 2026

> Based on current interview patterns across FAANG, AI-native startups, and enterprise teams.
> Updated to reflect the 2026 shift away from whiteboard theory toward production, LLMs, and MLOps.

---

## How to use this guide

Each section is tagged with one of three AI-use labels:

| Label | Meaning |
|---|---|
| 🚫 No AI | You'll be tested without AI tools. Drill these cold. |
| ✅ AI OK | Many interviewers now allow or even require AI here. Practice *with* AI. |
| ⚠️ Depends | Policy varies by company and round. Ask up front. Always own the output. |

---

## Part 1 — Interview structure overview

### The typical loop

| Stage | Duration | What's tested | AI tools? |
|---|---|---|---|
| Recruiter screen | 30 min | Fit, background, leveling | 🚫 No AI |
| Technical phone screen | 45–60 min | ML concepts, 1 easy/medium coding Q | 🚫 No AI |
| ML system design | 45–60 min | End-to-end pipeline thinking | ⚠️ Depends |
| MLOps / production round | 45 min | Deployment, drift, monitoring | ⚠️ Depends |
| Coding round | 45–60 min | Python, DSA, ML-flavored problems | ⚠️ Depends (Meta/Google now allow AI) |
| Behavioral | 30 min | Ownership, safety mindset, ambiguity | 🚫 No AI |

**Time budget:** 4–5 hrs of technical content, usually across 2–3 days.

### AI tool policy by company (as of mid-2026)

| Company | Live coding | Take-home |
|---|---|---|
| **Meta** | ✅ AI allowed — GPT, Claude, Gemini, Llama available in CoderPad | ✅ |
| **Google** | ✅ Piloting Gemini-assisted coding round (some teams) | ✅ |
| **Canva** | ✅ Expects you to use Copilot, Cursor, or Claude | ✅ |
| **Amazon** | 🚫 Standard live rounds still AI-off | ✅ |
| **Startups (YC-stage)** | ✅ Usually fine — they care about results and reasoning | ✅ |
| **Most others** | 🚫 Assume AI is off unless told otherwise | ✅ |

**Rule of thumb:** always ask "Should I treat this as AI-allowed or AI-off?" at the start of any coding round. It signals you're current, not unsure.

**Even when AI is allowed:** you're being evaluated on whether you own the output — prompting granularity, catching hallucinations, validating edge cases, and explaining every line. Never accept AI output without reading it.

---

## Part 2 — What's no longer the focus

These were core interview topics in 2019–2022. In 2026, they've mostly moved to quick conceptual checks, not full drill sessions.

🚫 **Deprioritize (but don't skip entirely):**
- Implementing backpropagation from scratch
- Writing gradient descent by hand
- Reciting definitions ("what is overfitting?", "what is regularization?")
- Pure LeetCode grind (it still exists but isn't the centerpiece)
- Memorizing CNN architectures

You should still be able to *explain* these clearly. You won't be asked to code them in isolation.

---

## Part 3 — Core study areas

---

### 3.1 ML fundamentals  
**🚫 No AI — these are tested cold in phone screens**

You need to explain these fluently, justify tradeoffs, and apply them to scenarios. No lookup allowed.

**Topics:**

- Bias-variance tradeoff — what it means in practice, how to diagnose it
- Overfitting vs underfitting — regularization (L1/L2, dropout, early stopping)
- Classification metrics — precision, recall, F1, AUC-ROC; when to use each
- Class imbalance — SMOTE, class weights, threshold tuning, resampling
- Feature engineering — scaling, encoding, feature selection, leakage
- Tree-based models — XGBoost, LightGBM, random forest; when to use over deep learning
- Loss functions — cross-entropy, MSE, focal loss; what problem each solves
- Evaluation strategy — train/val/test splits, cross-validation, holdout sets
- Hyperparameter tuning — grid search, random search, Bayesian optimization
- Data leakage — how it happens, how to detect it

**Practice format:** Explain any concept in 2 minutes as if to a product manager who asks "so why does that matter in production?"

---

### 3.2 Classical ML algorithms  
**🚫 No AI — still appear in phone screens and system design setups**

You don't need to implement these from scratch, but you need solid working knowledge.

**Topics:**

- Linear/logistic regression — assumptions, limitations, when they still win
- SVMs — kernel trick, margin intuition (high-level is fine)
- Decision trees — splitting criteria (Gini, entropy), pruning
- Ensemble methods — bagging vs boosting, stacking
- Clustering — K-means, DBSCAN, choosing K
- Dimensionality reduction — PCA, t-SNE/UMAP (for visualization)
- Recommender systems — collaborative filtering, matrix factorization, cold start problem

---

### 3.3 Deep learning fundamentals  
**🚫 No AI for conceptual questions / ✅ AI OK for coding implementation**

**Topics:**

- Backpropagation — understand the chain rule conceptually; you won't be asked to implement it
- Activation functions — ReLU, GELU, sigmoid, softmax; why ReLU beat sigmoid
- Batch normalization, layer normalization — what they do, when to use each
- Optimizers — SGD, Adam, AdamW; intuition for momentum and adaptive rates
- Learning rate schedules — warmup, cosine decay, cyclical
- Regularization — dropout, weight decay, data augmentation
- CNNs — convolution, pooling, receptive field (useful for CV roles)
- RNNs / LSTMs — vanishing gradients, when transformers replaced them

**PyTorch is the standard.** Know how to write a training loop, custom dataset, and DataLoader from memory.

---

### 3.4 Transformers and LLMs  
**🚫 No AI for conceptual questions — this is now core**

This is the biggest shift from prior years. Expect deep questions here.

**Topics:**

- Attention mechanism — query, key, value; scaled dot-product attention; why it works
- Multi-head attention — intuition for what different heads learn
- Positional encoding — why it's needed, absolute vs rotary (RoPE)
- Transformer architecture — encoder-only (BERT), decoder-only (GPT), encoder-decoder (T5)
- Tokenization — BPE, WordPiece; how vocabulary size affects performance
- Context window — cost vs capability tradeoff; long-context approaches
- Hallucination — root causes; mitigation layers (RAG, guardrails, confidence scoring)
- Fine-tuning vs RAG — when each is preferred; cost, latency, updatability tradeoffs
- LoRA / QLoRA — parameter-efficient fine-tuning; why it matters at scale
- Quantization — INT8, INT4; inference cost reduction
- Inference optimization — KV cache, speculative decoding, batching strategies

---

### 3.5 RAG architecture  
**🚫 No AI for design questions — this is tested heavily**

RAG is now a must-know topic for any AI/applied ML role.

**Topics:**

- Chunking strategy — fixed-size, semantic, hierarchical; impact on retrieval quality
- Embedding models — dense retrieval, how to choose, domain fine-tuning
- Vector databases — Pinecone, Weaviate, pgvector; indexing methods (HNSW, IVF)
- Hybrid search — dense + sparse (BM25); when hybrid beats pure dense
- Reranking — cross-encoders, Cohere Rerank; latency vs quality tradeoff
- Retrieval evaluation — recall@k, MRR, NDCG; how to run offline evals
- Hallucination in RAG — faithfulness, context relevance, answer relevance
- Production pitfalls — retrieval drift, stale embeddings, context stuffing

**Common system design prompt:** "Design an end-to-end RAG service: data ingestion, indexing, retrieval, generation, evals, tracing, and guardrails."

---

### 3.6 ML system design  
**🚫 No AI — this is the biggest and most important round**

This is where the best candidates show their ceiling. You'll be asked to design a full ML system end-to-end, usually in 45–60 minutes. Expect follow-up on every decision.

**Framework to use for any ML design question:**

1. **Problem framing** — what are we optimizing? What's the business metric?
2. **Data** — sources, volume, freshness, labeling strategy, class imbalance
3. **Feature engineering** — what features, how to compute them, online vs offline
4. **Model selection** — start with a simple baseline, justify escalation to complexity
5. **Training & evaluation** — offline metrics, online metrics, A/B test design
6. **Deployment** — batch vs real-time, shadow mode, canary releases
7. **Monitoring** — data drift, concept drift, prediction distribution, latency, cost
8. **Retraining** — trigger strategy, automated vs manual, rollback plan

**Common design questions:**
- Design a recommendation system for a streaming platform
- Design a fraud detection system serving 10K TPS
- Design a document Q&A chatbot for enterprise use
- Design a content moderation pipeline for a social network
- Design a multi-step agentic workflow (e.g., email triage, code review)
- Design a real-time personalization system

**Key tradeoffs to always address:** latency vs accuracy, online vs batch, cost vs performance, explainability vs model complexity.

---

### 3.7 MLOps and production  
**⚠️ Depends — often tested with AI tools off; some companies allow docs/IDE**

This is the "bottleneck skill" in 2026. Companies want engineers who can ship models, not just train them.

**Topics:**

- Experiment tracking — MLflow, Weights & Biases; what to log and why
- Model registry — staging vs production versioning, rollback
- Containerization — Docker basics; why it matters for reproducibility
- Orchestration — Kubernetes fundamentals; pod scaling, resource limits
- CI/CD for ML — automated testing, model validation gates, promotion logic
- Feature stores — Feast, Tecton; training-serving skew, point-in-time correctness
- Data pipelines — Airflow, Prefect; DAG design, failure handling
- Monitoring — Prometheus, Grafana; what metrics to track
- Data drift detection — statistical tests (KS, PSI); when to alert vs retrain
- Concept drift — how to detect it; proxy metrics when labels are delayed
- Inference optimization — TensorRT, ONNX, TorchServe; latency budgeting
- Cloud platforms — SageMaker, Vertex AI, Azure ML; know at least one deeply

**Stack to be fluent in:** Docker · Kubernetes · MLflow · GitHub Actions · Airflow · FastAPI

---

### 3.8 Agentic AI systems  
**🚫 No AI for design — this is now a standard advanced topic**

**Topics:**

- Tool calling / function calling — how LLMs invoke tools, schema design
- Memory systems — short-term (context window), long-term (vector store), episodic
- Agent frameworks — LangChain, LlamaIndex, AutoGen (know one well)
- Multi-agent architectures — orchestrator/worker patterns, parallelism
- Guardrails — prompt injection defense, output validation, rate limiting
- Evaluation — how to eval an agent; trajectory-based metrics, success rate
- Failure modes — unbounded tool calls, retrieval drift, context overflows
- Human-in-the-loop — when to interrupt, confidence thresholds, escalation

---

### 3.9 Coding  
**⚠️ Depends — Meta/Google now allow AI; most others don't. Practice both ways.**

**Topics to drill without AI:**
- Arrays, hash maps, trees, graphs, dynamic programming
- Sorting and searching
- String manipulation
- BFS/DFS traversal
- Two-pointer and sliding window

**ML-flavored coding problems (still common):**
- Implement k-means from scratch
- Write a simple neural network layer in NumPy
- Implement a precision-recall curve
- Build a simple feature pipeline with pandas
- Write a tokenizer

**When AI is allowed (Meta, Google, Canva):**
- Use AI for well-defined subtasks (boilerplate, shell commands, helper functions)
- Keep architectural decisions in your head, not in the prompt
- Always read, validate, and run AI-generated code before moving on
- Narrate what you're doing and why — that's what's being evaluated
- Test edge cases the AI may have missed

---

### 3.10 Ethical AI and explainability  
**🚫 No AI — now a hard engineering requirement, not a soft skill**

**Topics:**

- Fairness metrics — demographic parity, equalized odds, calibration
- Bias sources — training data, label noise, proxy features
- Explainability tools — SHAP, LIME; when to use each
- Audit frameworks — how to run a bias audit, what to document
- Adversarial robustness — prompt injection, jailbreaks, adversarial examples
- Privacy — differential privacy basics, federated learning concepts
- Responsible deployment — staged rollouts, monitoring for disparate impact

---

### 3.11 Behavioral round  
**🚫 No AI — this is a pure conversation**

Behavioral rounds for AI roles are different from standard SWE. They probe for:

- Ownership of AI systems in production
- Comfort with ambiguity and rapid change
- Safety-first mindset
- How you collaborate with non-technical stakeholders

**Very common questions in 2026:**
- Walk me through an AI project you built end-to-end
- Describe a time you reduced hallucinations or cost in production
- Describe a project where your AI solution failed. What did you do?
- How do you stay current with AI moving so fast?
- Tell me about a time you had to make a safety-first decision
- How do you collaborate with product managers or business stakeholders on AI features?
- Give an example of when you addressed ethical concerns in an ML project

**Use the STAR format:** Situation, Task, Action, Result. Include the technical specifics — what architecture, what the failure mode was, what you changed, what the measurable outcome was.

Prepare 5–6 strong stories. They should cover: a production failure, a cross-functional challenge, a tradeoff decision, an ethical consideration, and something you're proud of.

---

## Part 4 — Study schedule (6-week plan)

| Week | Focus |
|---|---|
| 1 | ML fundamentals + classical algorithms (cold recall, no notes) |
| 2 | Transformers + LLMs + RAG architecture |
| 3 | ML system design — practice 2–3 designs per day using the framework |
| 4 | MLOps + production — build or revisit a real deployment pipeline |
| 5 | Coding (no-AI drills) + AI-assisted coding practice (prompt strategy) |
| 6 | Behavioral prep + mock interviews + company-specific research |

---

## Part 5 — Resources

**System design:**
- Eugene Yan's ML system design writing (evidentlyai.com blog)
- Chip Huyen's *Designing Machine Learning Systems* (O'Reilly)
- ML System Design Interview guide (hellointerview.com)

**LLMs and RAG:**
- Lilian Weng's blog (lilianweng.github.io)
- Anthropic and OpenAI prompting guides
- LlamaIndex and LangChain documentation

**MLOps:**
- Made With ML (madewithml.com)
- Full Stack Deep Learning course

**Coding:**
- LeetCode (focus: medium, ML-flavored problems)
- Kaggle (for applied problem-solving)

**Behavioral:**
- *Cracking the PM Interview* behavioral frameworks adapt well here
- Keep a running doc of your 5–6 best stories, updated after every project

---

## Part 6 — Quick reference: AI tool rules

| Situation | What to do |
|---|---|
| Live coding round, no mention of AI | Assume AI is off. Don't use it. |
| Live coding round, company told you AI is allowed | Use it, but narrate your process to the interviewer |
| Take-home assignment | AI is almost always fine. Include a note on how you used it. |
| System design round | AI tools are rarely provided. Think out loud, no lookup. |
| Behavioral round | No AI. Speak from real experience. |
| Unsure about the policy | Ask: "Should I treat this as AI-allowed or AI-off?" — this is a smart question, not an unsure one. |

**When AI is allowed, you're evaluated on:**
1. How intelligently you prompt
2. How quickly you catch hallucinations and bugs
3. Whether you own the solution or outsource the thinking
4. How well you narrate your reasoning to the interviewer

The companies that allow AI specifically designed problems that can't be solved with a single prompt. They require iterative thinking, requirement clarification, and genuine engineering judgment.

---

*Good luck. The market rewards engineers who think in systems, ship to production, and communicate tradeoffs clearly.*
