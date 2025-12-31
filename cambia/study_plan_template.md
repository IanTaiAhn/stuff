
## 📘 AI Scientist Study Plan (Cambia-Aligned)
### PHASE 1 — Foundations Refresh (Weeks 1–3)
### Week 1 — Math & ML Core Foundations

#### Goal: Be able to reason about models, not just run them.

Study

- Linear Algebra: vectors, matrices, dot products, eigen intuition
- Probability: distributions, expectation, variance, Bayes’ rule
- Statistics: hypothesis testing, confidence intervals
- Calculus: gradients, partial derivatives (intuition)

ML Concepts

- Objective functions
- Regularization (L1 vs L2)
- Bias–variance tradeoff
- Overfitting vs underfitting

Deliverables

- Explain why regularization reduces overfitting
- Explain how gradient descent works without equations

Interview-ready when you can say:

“This loss function aligns with the business objective and regularization controls variance.”

### Week 2 — Classic ML & Evaluation

#### Goal: Sound confident discussing traditional ML choices.

Study

- Linear / logistic regression
- Decision trees, random forests, gradient boosting
- SVMs (intuition only)
- Collaborative filtering
- Ranking problems
- Evaluation
- AUC, precision, recall, F1
- RMSE vs MAE
- Feature importance
- Error analysis

Hands-On

- Train at least two different models on the same dataset
- Compare metrics and explain differences

Interview-ready when you can:

- Justify metric choice
- Explain model failure modes

### Week 3 — ML Pipelines & Experimentation

#### Goal: Demonstrate professional ML workflow.

Study

- Train / validation / test splits
- Data leakage (critical for healthcare)
- Hyperparameter tuning
- Grid search vs random search
- Reproducibility

Hands-On

- Build an end-to-end ML pipeline
- Track experiments
- Document assumptions

Interview-ready when you can say:

“We ensured no leakage by splitting on time or entity rather than randomly.”

### PHASE 2 — Deep Learning & Data (Weeks 4–5)
### Week 4 — Deep Learning Fundamentals

#### Goal: Explain deep learning intuitively.

Study

- Activation functions
- Gradient descent issues (vanishing gradients)
- CNNs (why convolution works)
- RNNs / LSTMs (sequence modeling)
- GANs (generator vs discriminator)
- Embeddings (semantic similarity)

Hands-On

- Train a simple neural network
- Generate embeddings and measure similarity

Interview-ready when you can:
Explain why embeddings power RAG and retrieval systems.

### Week 5 — Data & Experimental Design

#### Goal: Think like a scientist, not a model jockey.

Study

- Research questions vs metrics
- Confounding variables
- Correlation vs causation
- Visualization best practices

Hands-On

- Design an experiment
- Visualize results
- Write conclusions

Interview-ready when you can say:

“This result is statistically significant, but not practically meaningful.”

### PHASE 3 — Generative AI Core (Weeks 6–9)
### Week 6 — Transformers & LLM Fundamentals

#### Goal: Deep conceptual understanding of LLMs.

Study

- Transformer architecture
- Self-attention
- Encoder vs decoder
- Scaling laws
- In-context learning

Hands-On

- Load a pretrained LLM
- Run zero-shot and few-shot prompts

Interview-ready when you can:
Explain why few-shot works without training.

### Week 7 — Prompt Engineering & Fine-Tuning

#### Goal: Know when not to fine-tune.

Study

- Prompt structures
- Chain-of-thought
- Instruction hierarchies
- Full fine-tuning vs LoRA vs QLoRA
- Tradeoffs (cost, drift, latency)

Hands-On

- Prompt optimization task
- LoRA fine-tune a small model

Interview-ready when you can say:

“We avoided fine-tuning because RAG provided fresher knowledge with lower risk.”

### Week 8 — Retrieval-Augmented Generation (RAG)

#### Goal: Build trustworthy GenAI systems.

Study

- Embeddings
- Vector databases
- Chunking strategies
- Retrieval vs generation failures
- Latency vs accuracy tradeoffs

Hands-On

- Build a full RAG pipeline
- Test hallucination reduction

Interview-ready when you can:
Explain why RAG is essential in healthcare.

### Week 9 — Evaluation, Alignment & Responsible AI

#### Goal: Show maturity and safety awareness.

Study

- Perplexity, BLEU, ROUGE (and limitations)
- Human evaluation
- RLHF
- Constitutional AI
- Red-teaming
- Bias & hallucination mitigation

Hands-On

- Create an evaluation rubric
- Perform error analysis on LLM outputs

Interview-ready when you can say:

“Automated metrics alone were insufficient, so we added human review.”

### PHASE 4 — Healthcare + Engineering Context (Weeks 10–12)
### Week 10 — Healthcare Domain Knowledge

#### Goal: Speak healthcare fluently without being clinical.

Study

- Claims vs clinical data
- Delayed and biased data
- Importance of interpretability
- Regulatory mindset (HIPAA)
- Why healthcare AI fails in practice

Interview-ready when you can:

Tie AI decisions to patient safety and trust.

### Week 11 — Engineering & Production Mindset

#### Goal: Show you can ship responsibly.

Study

- Model monitoring
- Drift detection
- Offline vs online metrics
- Feature importance in production
- Experiment reproducibility

Hands-On

- Simulate model drift
- Design monitoring metrics

### Week 12 — Integration & Storytelling

#### Goal: Convert knowledge into interviews.

Tasks

Prepare:

- 1 classic ML story
- 1 GenAI system story
- 1 failure story
- 1 healthcare-specific story

Practice explaining:

- Tradeoffs
- Metrics
- Limitations

Final Interview Signal:
You sound calm, thoughtful, and responsible — not hype-driven.