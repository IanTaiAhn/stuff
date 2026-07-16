# Interview Prep Guide: ML Engineer / AI Software Engineer / Applied Data Scientist

**How to use this:** Cover the answer under each question with your hand or a piece of paper, say your answer out loud (or write it), then check yourself. Anything you fumble, flag it and revisit in 2-3 days — that's the active recall + spaced repetition loop. Don't just re-read; force the retrieval.

---

## Part 1: Machine Learning Engineer

### A. ML Fundamentals

**Q1. What's the bias-variance tradeoff, in your own words?**
> Bias = error from overly simplistic assumptions (underfitting). Variance = error from sensitivity to the training data's noise (overfitting). Total error ≈ bias² + variance + irreducible noise. More model complexity typically lowers bias but raises variance.

**Q2. How do you decide between precision and recall for a given problem?**
> Optimize precision when false positives are costly (spam filter flagging real email). Optimize recall when false negatives are costly (cancer screening missing a case). F1 balances both when neither dominates.

**Q3. Why use k-fold cross-validation instead of a single train/test split?**
> Reduces variance in the performance estimate from an unlucky single split; every data point gets used for both training and validation across folds, giving a more reliable estimate of generalization error.

**Q4. What is regularization and name two common types.**
> A penalty added to the loss function to discourage overly complex models and reduce overfitting. L1 (Lasso) drives some weights to exactly zero (feature selection); L2 (Ridge) shrinks weights smoothly toward zero.

**Q5. Explain the difference between bagging and boosting.**
> Bagging trains models in parallel on bootstrapped samples and averages/votes (reduces variance, e.g. Random Forest). Boosting trains models sequentially, each correcting the previous one's errors (reduces bias, e.g. XGBoost, AdaBoost).

**Q6. What's the curse of dimensionality?**
> As feature count grows, data becomes sparse in the feature space, distance metrics become less meaningful, and models need exponentially more data to generalize well.

**Q7. When would you choose a tree-based model over a linear model?**
> When relationships are nonlinear or involve complex feature interactions, when you don't want to hand-engineer interaction terms, or when feature scaling/normalization is inconvenient. Linear models win when you need interpretability, extrapolation, or have limited data.

**Q8. What is data leakage and give an example.**
> When information from outside the training set (often from the future or the target itself) leaks into features, inflating performance metrics artificially. Example: including a "days since cancellation" feature when predicting churn.

**Q9. How do you handle class imbalance?**
> Resampling (oversample minority/undersample majority, SMOTE), class-weighted loss functions, choosing appropriate metrics (PR-AUC over accuracy), or anomaly-detection framing for extreme imbalance.

**Q10. What's the difference between parametric and non-parametric models?**
> Parametric models assume a fixed functional form with a finite set of parameters (linear regression, logistic regression). Non-parametric models grow in complexity with data and make fewer assumptions about the underlying function (KNN, decision trees, kernel methods).

### B. Deep Learning

**Q1. Walk through what happens in backpropagation.**
> Forward pass computes predictions and loss. Backward pass applies the chain rule to compute the gradient of the loss with respect to each weight, propagating error signal from output layer back to input layer. Weights are then updated via gradient descent.

**Q2. What causes vanishing/exploding gradients and how is it mitigated?**
> Repeated multiplication of small (or large) derivatives across many layers shrinks (or blows up) gradients. Mitigations: better initialization (Xavier/He), normalization layers (batch norm, layer norm), residual/skip connections, gradient clipping, using ReLU-family activations instead of sigmoid/tanh.

**Q3. Compare SGD, Momentum, and Adam.**
> SGD updates using the raw gradient each step (noisy but simple). Momentum adds a velocity term that accumulates past gradients, smoothing updates and speeding convergence. Adam adapts the learning rate per-parameter using estimates of both the first and second moments of the gradients — generally fast to converge, less tuning needed, though sometimes generalizes slightly worse than well-tuned SGD.

**Q4. What does batch normalization actually do?**
> Normalizes layer inputs (per batch) to zero mean/unit variance, then applies a learnable scale and shift. Stabilizes and speeds up training by reducing internal covariate shift and allowing higher learning rates.

**Q5. Why do CNNs work well for images?**
> Convolutional filters exploit spatial locality and translation invariance — a pattern (edge, texture) can be detected anywhere in the image with shared weights, drastically reducing parameters vs. a fully connected layer.

**Q6. At a high level, how does self-attention work in a Transformer?**
> Each token produces a query, key, and value vector. Attention scores are computed as the scaled dot product of a token's query with every other token's key, softmaxed into weights, then used to compute a weighted sum of value vectors — letting every token dynamically attend to relevant context regardless of distance.

**Q7. What's the difference between fine-tuning and training from scratch?**
> Fine-tuning starts from pretrained weights that already encode general patterns, and adapts them to a new task/domain with a smaller dataset and fewer training steps — much more data- and compute-efficient than training from random initialization.

**Q8. What is dropout and why does it help?**
> Randomly zeroes out a fraction of neurons during training, forcing the network not to rely too heavily on any single neuron/path — acts as an implicit ensemble and reduces overfitting.

### C. Coding Prompts Likely to Appear
Practice these live, with a time limit, out loud explaining your approach first:
- Implement k-means clustering from scratch
- Implement logistic regression gradient descent from scratch (no sklearn)
- Write a function for the forward pass of a single-layer neural net
- Standard DS&A: two-pointer array problems, BFS/DFS on a graph, tree traversal, sliding window, top-k with a heap
- Given a stream of data, compute a running mean/variance (Welford's algorithm)
- Matrix multiplication / batch matrix operations without a library

### D. ML System Design Prompts
For these, practice the *structure* of your answer, not just the content: clarify requirements → define the metric/objective → data → features → model choice + tradeoffs → serving/latency constraints → monitoring & retraining → failure modes.
- Design a recommendation system for a video platform
- Design a fraud detection system for transactions
- Design a search ranking system
- Design a system to detect duplicate/near-duplicate content
- How would you detect and handle training/serving skew?
- How would you design an A/B testing framework for model rollouts?

---

## Part 2: AI Software Engineer (GenAI / LLM-flavored)

### A. Core Software Engineering
**Q1. What's the difference between a process and a thread?**
> A process has its own memory space and is an independently executing program; threads share memory within a process and are lighter-weight, enabling concurrency within one process.

**Q2. What is idempotency and why does it matter for APIs?**
> An idempotent operation produces the same result no matter how many times it's applied. Matters for retries — a client can safely re-send a request after a timeout without risking duplicate side effects (e.g., double charging).

**Q3. Explain caching strategies (write-through vs. write-back) briefly.**
> Write-through writes to cache and the backing store simultaneously (safer, slightly slower). Write-back writes to cache first and flushes to storage later (faster, risk of data loss on crash).

**Q4. How would you design a rate limiter?**
> Common approaches: token bucket (allows bursts up to bucket size, refills at fixed rate), sliding window log/counter (more precise, more memory), fixed window counter (simplest, has boundary burst issues).

### B. LLM / GenAI Specific
**Q1. What is RAG (Retrieval-Augmented Generation) and why use it?**
> Combines a retrieval step (fetching relevant documents/chunks from a knowledge base, typically via vector similarity search) with generation, so the model answers grounded in retrieved context rather than only its parametric memory — reduces hallucination and allows up-to-date/private knowledge without retraining.

**Q2. How do embeddings and vector databases work together?**
> Text is converted into dense vectors that capture semantic meaning; a vector database indexes these (often via approximate nearest neighbor methods like HNSW) so a query embedding can retrieve semantically similar items efficiently at scale.

**Q3. Prompting vs. fine-tuning vs. RAG — when do you use each?**
> Prompting/few-shot: quick iteration, no training data needed, works for many tasks out of the box. Fine-tuning: when you need consistent behavior, a specific format/style, or domain adaptation that prompting can't reliably achieve, and you have labeled examples. RAG: when the need is fresh or proprietary *knowledge* rather than a new *skill* or *style*.

**Q4. How do you evaluate the quality of an LLM's output?**
> Combination of automated metrics (BLEU/ROUGE for overlap, embedding similarity), task-specific metrics (exact match, F1 for QA), LLM-as-judge scoring against a rubric, and human evaluation — often triangulating multiple methods since no single automated metric fully captures quality.

**Q5. What causes hallucination and how do you mitigate it?**
> The model generates fluent but factually ungrounded text because it's optimized to predict plausible next tokens, not verified truth. Mitigations: RAG grounding, lowering temperature, prompting for citations/uncertainty, output verification/fact-checking layers, fine-tuning on high-quality factual data.

**Q6. What is an agent/tool-use pattern in an LLM system?**
> The model is given access to external tools (search, calculator, code execution, APIs) and can decide when to invoke them, incorporate results into its reasoning, and iterate — extending it beyond static text generation into taking actions.

**Q7. What's the difference between context window limits and why do they matter for system design?**
> Limits the amount of text (prompt + retrieved context + history) a model can process at once; drives design decisions like chunking strategy for RAG, conversation summarization/truncation, and cost (longer context = more compute/$$ per call).

### C. AI Product System Design Prompts
- Design a customer support chatbot backed by a company's knowledge base
- Design a code-completion feature (like Copilot) for an IDE
- Design a content moderation pipeline using an LLM
- How would you reduce latency and cost for an LLM-powered feature at scale?

---

## Part 3: Applied Data Scientist

### A. SQL
Practice writing these without an IDE — on paper or a whiteboard:
- Second-highest value per group (window functions: `RANK()`, `DENSE_RANK()`)
- Running totals / moving averages (`SUM() OVER (ORDER BY ... ROWS BETWEEN ...)`)
- Self-joins for comparing rows within the same table (e.g., consecutive days)
- Cohort retention query (users active in month N who were also active in month N+1)
- Deduplication using `ROW_NUMBER()` partitioned by a key

**Q: What's the difference between `WHERE` and `HAVING`?**
> `WHERE` filters rows before aggregation; `HAVING` filters groups after aggregation (`GROUP BY`).

**Q: Difference between `RANK()`, `DENSE_RANK()`, and `ROW_NUMBER()`?**
> `ROW_NUMBER()` gives unique sequential numbers even for ties. `RANK()` gives ties the same rank but skips subsequent ranks (1,1,3). `DENSE_RANK()` gives ties the same rank without skipping (1,1,2).

### B. Statistics & Experimentation
**Q1. Explain a p-value in plain language.**
> The probability of observing data at least as extreme as what you saw, assuming the null hypothesis is true. It is NOT the probability the null hypothesis is true.

**Q2. What's a Type I vs. Type II error?**
> Type I: rejecting a true null hypothesis (false positive). Type II: failing to reject a false null hypothesis (false negative). There's a tradeoff between them controlled by your significance threshold.

**Q3. How do you determine sample size / how long to run an A/B test?**
> Power analysis: based on the minimum detectable effect size you care about, baseline conversion rate, desired statistical power (commonly 80%), and significance level (commonly 5%) — solve for the required sample size, then convert to run-time given daily traffic.

**Q4. What is the "peeking problem" in A/B testing?**
> Repeatedly checking significance before the pre-planned sample size is reached inflates the false positive rate, because each peek is an additional chance to hit a spurious significant result. Mitigate with sequential testing methods or committing to a fixed sample size/duration in advance.

**Q5. What's Simpson's Paradox and why does it matter for experiment analysis?**
> A trend that appears in aggregated data can reverse or disappear when the data is split into subgroups (often due to a confounding variable like traffic mix differing between test and control). Matters because overall experiment results can mislead if segment composition shifted.

**Q6. How would you check if your A/B test groups are actually comparable (a sample ratio mismatch or bad randomization)?**
> Run a sample ratio mismatch (SRM) check — a chi-squared test comparing actual vs. expected group sizes; also compare pre-experiment/baseline metrics between groups to confirm they're balanced before treatment.

### C. Product Sense / Case Questions
- "How would you measure the success of [feature X]?" — practice picking a primary metric, 1-2 guardrail metrics, and explaining why.
- "Engagement is down 10% this week — how do you investigate?" — practice a structured funnel: is it real (data issue?) → segment by platform/geo/cohort → check for seasonality/external events → correlate with recent changes/releases.
- "We want to add feature X — what tradeoffs would you flag?" — practice weighing user value vs. engineering cost vs. metric risk vs. unintended consequences.

---

## Part 4: Behavioral (All Three Roles)

Prep 5-6 stories in STAR format (Situation, Task, Action, Result) that you can flex across these prompts:
1. Tell me about a project you're proud of.
2. Tell me about a time a model/project failed or underperformed — what did you do?
3. Tell me about a disagreement with a teammate or manager.
4. Tell me about a time you had to simplify a technical result for a non-technical audience.
5. Tell me about a time you had ambiguous requirements.
6. Tell me about a time you made a mistake — how did you handle it?

For each story, be ready to answer the natural follow-ups: "What would you do differently?" and "What was the actual measurable impact?"

---

## Part 5: Quick-Reference Cheat Sheet

| Concept | One-liner |
|---|---|
| Precision | TP / (TP + FP) |
| Recall | TP / (TP + FN) |
| F1 | Harmonic mean of precision & recall |
| ROC-AUC | Ability to rank positives above negatives across thresholds |
| Adam | Adaptive per-parameter learning rate using 1st & 2nd moment estimates |
| Batch norm | Normalize activations per batch, then learnable scale/shift |
| RAG | Retrieve relevant context, then generate grounded in it |
| SRM | Sample Ratio Mismatch — sign of broken randomization in an A/B test |
| p-value | P(data this extreme \| null true) — not P(null true) |
| L1 vs L2 | L1 → sparsity (feature selection); L2 → smooth shrinkage |

---

## Suggested Weekly Rhythm
- **2-3 sessions/week**: coding practice (timed, out loud)
- **2-3 sessions/week**: quiz yourself on this doc, cold — no peeking until you answer
- **1 session/week**: mock system design (explain out loud or to a friend, 30-45 min)
- **Ongoing**: skim 5-10 target job postings, note recurring tools/keywords, and fold any gaps back into your quiz sessions above
