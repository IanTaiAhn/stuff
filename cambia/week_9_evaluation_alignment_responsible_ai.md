### Week 9 — Evaluation, Alignment & Responsible AI

#### Goal: Show maturity and safety awareness.

This week focuses on **how GenAI systems are evaluated, aligned, and made safe**. Senior practitioners understand that raw model capability is not enough—trust, reliability, and human oversight are essential, especially in high-impact domains.

---

## Study

### Perplexity, BLEU, ROUGE (and Limitations)

#### Perplexity
- Measures how well a language model predicts the next token
- Lower perplexity indicates better fluency

**Limitations**
- Does not measure factual correctness
- Poor proxy for task usefulness

---

#### BLEU
- Measures n-gram overlap between generated text and references
- Commonly used in translation

**Limitations**
- Penalizes valid paraphrases
- Encourages generic outputs
- Requires high-quality reference texts

---

#### ROUGE
- Measures recall-based overlap
- Often used in summarization

**Limitations**
- Rewards verbosity
- Ignores coherence and factual accuracy

---

### Human Evaluation

#### Why human evaluation is necessary
- Captures usefulness, clarity, and correctness
- Detects hallucinations and subtle errors
- Evaluates alignment with user intent

#### Common evaluation criteria
- Factual accuracy
- Completeness
- Clarity
- Safety and tone
- Helpfulness

#### Tradeoffs
- Expensive and time-consuming
- Requires clear rubrics to reduce subjectivity

---

### RLHF (Reinforcement Learning from Human Feedback)

#### What RLHF is
- Aligns model behavior with human preferences
- Uses human-ranked outputs to train reward models

#### Why it matters
- Improves helpfulness and safety
- Reduces harmful or unhelpful outputs

#### Limitations
- Expensive to collect feedback
- Encodes annotator biases
- Can reduce model creativity

---

### Constitutional AI

#### Core idea
- Align models using a written set of principles
- Model critiques and revises its own outputs

#### Why it’s useful
- Reduces reliance on large-scale human labeling
- Makes alignment goals explicit and auditable

#### Limitations
- Quality depends on constitution design
- Still requires validation

---

### Red-Teaming

#### What red-teaming is
- Systematic stress testing of models
- Adversarial probing for failures

#### What it uncovers
- Hallucinations
- Biases
- Prompt injection vulnerabilities
- Unsafe completions

#### Best practices
- Diverse testers
- Documented failure patterns
- Iterative mitigation

---

### Bias & Hallucination Mitigation

#### Sources of bias
- Training data
- Evaluation datasets
- Prompt framing

#### Mitigation strategies
- Balanced and diverse data
- Prompt constraints
- Post-generation checks
- Retrieval grounding
- Human review for high-risk outputs

#### Hallucination reduction
- RAG
- Confidence calibration
- Refusal policies when unsure

---

## Hands-On

- Create an **evaluation rubric**
  - Define qualitative and quantitative criteria
  - Include safety and factuality
- Perform error analysis on LLM outputs
  - Categorize failure types
  - Identify root causes
  - Propose mitigations

---

## Interview-Ready When You Can:

- Explain why perplexity is insufficient
- Describe when automated metrics fail
- Justify human-in-the-loop evaluation
- Explain RLHF and Constitutional AI at a high level
- Discuss red-teaming results concretely
- *“Automated metrics alone were insufficient, so we added human review.”*
