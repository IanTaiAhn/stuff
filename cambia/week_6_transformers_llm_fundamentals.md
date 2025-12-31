### PHASE 3 — Generative AI Core (Weeks 6–9)

### Week 6 — Transformers & LLM Fundamentals

#### Goal: Deep conceptual understanding of LLMs.

This week builds a **mental model of large language models**. The focus is not on equations, but on understanding how transformers process information, why scale matters, and how LLMs can learn *at inference time*.

---

## Study

### Transformer Architecture

#### What a transformer is
- A neural network architecture designed for sequence modeling
- Processes entire sequences in parallel
- Replaced recurrence with attention

#### Core components
- Token embeddings
- Positional encoding
- Self-attention layers
- Feed-forward networks
- Residual connections and normalization

#### Why transformers replaced RNNs
- Parallelizable training
- Better long-range dependency handling
- More stable gradients

---

### Self-Attention

#### Core idea
- Each token looks at every other token
- Learns which tokens matter most for context

#### What attention computes
- Query, key, and value vectors
- Similarity determines attention weights

#### Intuition
- Words dynamically choose what to pay attention to
- Context is built by weighted averaging of relevant tokens

#### Why it scales
- Same mechanism works for short or long contexts
- Captures syntax and semantics jointly

---

### Encoder vs Decoder

#### Encoder
- Reads and understands input
- Produces contextualized representations
- Used in:
  - BERT-style models
  - Classification
  - Embeddings

#### Decoder
- Generates output token by token
- Uses masked self-attention
- Used in:
  - GPT-style models
  - Text generation

#### Encoder–Decoder
- Encoder processes input
- Decoder generates output conditioned on encoder states
- Used in translation and summarization

---

### Scaling Laws

#### What scaling laws describe
- Model performance improves predictably with:
  - More parameters
  - More data
  - More compute

#### Key intuition
- Bigger models learn more general patterns
- Undertraining large models wastes capacity
- Overtraining small models saturates quickly

#### Practical takeaway
- Scale often beats architecture tweaks
- Data quality still matters

---

### In-Context Learning

#### What it is
- Learning from examples provided in the prompt
- No weight updates occur

#### Why this is surprising
- Traditional ML requires training
- LLMs adapt behavior at inference time

#### What enables it
- Attention over prompt examples
- Pattern recognition across sequences
- Implicit meta-learning during pretraining

---

## Hands-On

- Load a **pretrained LLM**
  - Run inference locally or via API
  - Inspect tokenization and outputs
- Run zero-shot prompts
  - Provide task instruction only
- Run few-shot prompts
  - Provide input–output examples
  - Observe performance improvement

---

## Interview-Ready When You Can:

- Explain how self-attention builds context
- Contrast encoders and decoders
- Explain why transformers scale well
- Describe in-context learning intuitively
- **Explain why few-shot works without training**
  - The model recognizes patterns in the prompt
  - Attention binds examples to new inputs
  - Pretraining teaches the model *how to learn from context*
