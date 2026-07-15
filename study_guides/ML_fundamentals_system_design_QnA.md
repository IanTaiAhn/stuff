# Interview Prep Answer Key — ML/AI Engineer & Applied Data Scientist
*Compiled from practice session, based on Ian Tai Ahn's resume (RAG project, F-35 systems background)*

---

## ROUND 1: ML/AI FUNDAMENTALS

### Q1: What is an embedding, and why cosine similarity?
- **Chunking vs. tokenization are different steps.** Chunking = *you* deciding how to split a document into retrievable units (paragraph, sentence, fixed windows) — happens before the model touches it. Tokenization = the model's internal step of breaking text into subword pieces. Not the same thing, and not configured with regex.
- **An embedding is a dense vector of floats** (e.g., 384–1536 dimensions), produced by pooling token-level representations into one fixed-size vector per chunk. It is not "filled with tokens."
- **Bi-encoder** = encodes query and document *independently* into two vectors, compared after the fact (fast, scalable — this is what FAISS/vector search relies on).
- **Cross-encoder** = encodes query + document *together* as one input, outputs a relevance score directly (slow, accurate — this is what rerankers typically are).
- **Cosine similarity vs. Euclidean distance:** cosine measures the *angle* between vectors (ignores magnitude); Euclidean measures straight-line distance (sensitive to magnitude). Text embeddings care about *direction* (what the text is about), not magnitude (which can vary with length/emphasis) — so cosine aligns better with semantic similarity. Once vectors are L2-normalized, cosine and Euclidean produce the same *ranking*, which is why some libraries use dot product for speed after normalizing.

### Q2: Top-K similarity search vs. MMR
- **Top-K similarity search:** embed the query, compute similarity against every chunk vector, return the K highest-scoring chunks. No reranking involved — just nearest-neighbor lookup (this is the FAISS step).
- **The problem:** top-K optimizes purely for relevance to the query, with no regard for redundancy among the results. Can return several near-duplicate chunks that all restate the same fact, wasting context window.
- **MMR (Maximal Marginal Relevance)** fixes this by picking chunks one at a time, balancing *relevance to the query* against *dissimilarity to already-selected chunks* — trading a little top-1 relevance for better diversity of coverage.
- **Key distinction:** top-K vs. MMR = **relevance vs. diversity** trade-off. Bi-encoder vs. cross-encoder = **speed vs. accuracy** trade-off. Both can coexist in one pipeline.

### Q3: Cold start vs. async vs. warm-up hook
- **Cold start:** hosted platforms spin down idle servers to save cost. The next request has to wait for the container to boot and dependencies to load — that delay is the cold start.
- **Async request handling does NOT fix cold start.** Async lets a server start handling a second request while waiting on I/O (e.g., a network call to an external inference API) for the first, instead of blocking. It improves **throughput and concurrency**, not warm-up time.
- **The actual cold-start fix is the warm-up hook** — a scheduled ping (cron job / health-check hit) that keeps the server from going idle, or proactively triggers boot-up before a real user arrives.
- **Three separate problems, three separate fixes:** idle shutdown (cold start) → warm-up hook. Concurrency/throughput → async. They don't substitute for each other.

### Q4: Bias/variance and overfitting fixes
- **98% train / 65% validation accuracy = overfitting = low bias, high variance** (not "not enough variance" — that's backwards).
  - **Bias** = error from a model too simple to capture the pattern.
  - **Variance** = how much predictions swing based on the specific training data seen; high variance = latching onto training-set noise that doesn't generalize.
  - Memorize: **overfitting = low bias / high variance. Underfitting = high bias / low variance.**
- **Concrete fixes (not just "different model" or "data engineering"):**
  1. **Regularization** (L1/L2, dropout) — shrinks weights, discourages fitting noise. Usually the strongest default lever — cheap, tunable, works across linear models, trees, and neural nets.
  2. **Reduce model complexity** — fewer parameters/layers/depth directly lowers capacity to overfit.
  3. **Cross-validation** — a **diagnostic/tuning tool**, not a fix itself. It gives a reliable generalization estimate to tune regularization strength against; doesn't change the model on its own.
  4. **Early stopping** — halt training once validation loss starts climbing.
  5. **Ensembling/bagging** (e.g., random forests) — averages out individually overfit models to reduce variance.
  - Context-dependent picks: **regularization** as default first move; **bagging** for tree ensembles specifically; **dropout + early stopping** for deep nets.

### Q5: Diagnosing reranker regressions with objective metrics
- Eval dataset + manual chunk inspection is a legitimate *process*, but needs an actual **ranking metric**:
  - **MRR (Mean Reciprocal Rank):** for each query, take the reciprocal of the rank position of the first relevant chunk, average across queries. Answers "how fast does the relevant chunk show up?"
  - **NDCG (Normalized Discounted Cumulative Gain):** handles multiple relevant chunks with graded relevance, weights top positions more heavily. Better when relevance isn't strictly binary.
- **Workflow:** build a labeled eval set (query → relevant chunks), compute NDCG/MRR for bi-encoder ordering *and* reranker ordering on the same queries, isolate the queries where reranker NDCG *drops* below bi-encoder — that's your genuine regression set. Manually inspect only those to distinguish a bug (e.g., mishandling chunk length/format) from an inherent limitation (e.g., short/ambiguous queries).

### Q6: Why accuracy fails on imbalanced classes
- **98% accuracy on 2% defect rate is meaningless** — a model that always predicts "not defective" also scores 98%, while catching zero real defects. Accuracy is only meaningful when classes are roughly balanced.
- **Confusion matrix (memorize precisely):**
  - TP = predicted defective, is defective
  - FP = predicted defective, is fine
  - FN = predicted fine, is defective
  - TN = predicted fine, is fine
- **Recall** = TP / (TP + FN) — "of all real defects, how many did we catch?" Usually the priority in defect detection (a missed defect is costly).
- **Precision** = TP / (TP + FP) — "of everything flagged, how many were real?" Low precision = flooding QA with false alarms.
- **F1** = harmonic mean of the two, when you need one combined number. Threshold choice depends on which error costs more to the business — in defect detection, usually favor recall over precision.

### Q7: Guaranteeing schema-valid LLM output
- **Why it's nontrivial:** LLMs predict one token at a time from a probability distribution over the full vocabulary. Nothing inherently prevents a stray comma, unclosed brace, or wrong type — prompting for JSON is a *request*, not a *constraint*, and can be violated.
- **The real guarantee mechanism: constrained decoding (grammar-based / schema-constrained sampling).** Before each token is sampled, the decoder computes which tokens are grammatically valid at that position given the schema, and masks out (zero-probability) every invalid token. The model structurally *cannot* produce invalid output — not just "unlikely to." This is what libraries like `outlines`/`guidance` do, and what native tool-use/structured-output features (Claude, OpenAI function calling) do server-side.
- **Multi-pass / rules-engine approaches (generate → validate → re-prompt on error) are a fallback, not a guarantee** — they're probabilistic retry logic that reduces failure rate but doesn't eliminate it. Know the distinction explicitly: **constrained decoding = structural guarantee; retry loops = reduced failure rate.**

---

## ROUND 2: SYSTEM DESIGN

### Q1: Scaling RAG to 10K concurrent users, 50M chunks, <2s latency
Don't jump straight to naming tools — walk the request path stage by stage and name *why* each thing breaks:

1. **Vector index (FAISS in-memory):** 50M chunks at ~768 dims in float32 ≈ 150GB — doesn't fit on one machine, and FAISS as typically used has no built-in sharding/replication across machines. **This is a hard blocker**, not a degradation — nothing downstream matters until it's solved. Fix: managed/distributed vector DB (Pinecone, Weaviate, Qdrant) or a manually sharded FAISS setup — specifically for **horizontal sharding of the corpus** and **replication for concurrent read throughput**, not just "supports more stuff."
2. **API layer (FastAPI):** a single process saturates under 10K concurrent connections. Fix: multiple stateless instances behind a **load balancer**, with **auto-scaling** (ECS/Kubernetes/ASG) reacting to load. This is a **degradation problem** (system still works, just slow) — comparatively fast/cheap to fix.
3. **External embedding/reranker APIs (Jina, etc.):** third-party rate limits become a real bottleneck at this scale. Fix: caching (e.g., Redis for repeated/similar queries) and batching where feasible.
4. **LLM generation call:** usually the largest chunk of the latency budget. Fix: faster inference providers (Groq), streaming responses to reduce *perceived* latency.
5. **Explicit latency budgeting:** break the 2s target into a rough budget per stage (e.g., ~50-200ms vector search, ~50-100ms rerank, remainder for LLM generation) rather than just saying "we'll scale it."
6. **Cost/budget question comes last**, after bottlenecks are identified — not as a way to defer technical reasoning.

**Prioritization framework:** ask "hard blocker vs. degraded performance." Vector storage is a hard blocker (system literally can't function at scale) — fix first, since nothing else matters until it's solved. Load balancing is a degradation fix (system works, just slow) — fast, well-understood, can layer on after. Within "fix vector storage" for a single sprint, scope realistically: e.g., shard existing FAISS across a few machines, or start with a managed vector DB's starter tier and migrate incrementally — not a full production migration in one sprint.

### Q2: Detecting silent retrieval-quality degradation in production (no ground truth)
Core problem: no ground truth, so the whole design has to rely on **proxy signals**.

1. **Retrieval score distributions** — log top-k similarity scores per query, track average/distribution over time. A quiet drop in average top-1 score is a *leading* indicator of drift, often before bad answers are noticed.
2. **Embedding drift detection** — periodically compare the distribution of newly-ingested document embeddings against a baseline (e.g., population stability index, centroid/variance shifts). Detects when new documents land in a different region of embedding space than the historical corpus.
3. **Implicit user feedback** — query reformulation rate (user re-asking a rephrased question = likely failed first answer), session abandonment after a response, explicit thumbs up/down if available.
4. **LLM-as-judge sampling** — sample 1-5% of production queries, run through a separate judge LLM call scoring groundedness (does the answer reflect retrieved chunks, or hallucinate beyond them?) and relevance. Gives a quantified ongoing quality signal without full manual review.
5. **Basic ops signals** — latency, API timeouts, empty retrieval results, provider rate-limit errors.

**Turning signals into alerts:** don't use fixed thresholds blindly — use a rolling baseline with statistical bounds (e.g., moving average ± standard deviation, or "alert if today's average drops >X% below trailing 7-day average"). Catches gradual drift, avoids false alarms from normal noise.

**Where tracing/observability tools (query IDs, LangSmith, etc.) fit:** they're the "zoom in and debug one specific bad case *after* an alert fires" tool — not the "detect something's wrong across thousands of queries" tool. Aggregate monitoring detects *that* something broke; tracing helps you understand *why*, once you know where to look. Both matter, but they solve different halves of the problem.

---

## Overall Pattern to Address Before Interviews
Systems/engineering instincts are strong throughout (chunking, deployment, async, cost trade-offs, cloud infra). The recurring gap is **ML/AI theory vocabulary and precision**: bias/variance direction, bi-encoder vs. cross-encoder, what cross-validation actually does vs. what it doesn't, ranking metrics (NDCG/MRR), confusion-matrix-based metrics, and the mechanism behind guaranteed structured LLM output. Worth drilling these definitions until they come out precisely and fast, since interviewers will follow up exactly where the vocabulary is fuzzy.