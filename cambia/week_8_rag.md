### Week 8 — Retrieval-Augmented Generation (RAG)

#### Goal: Build trustworthy GenAI systems.

This week focuses on **grounding generation in real data**. RAG is the backbone of safe, up-to-date GenAI systems—especially in high-stakes domains like healthcare, where hallucinations are unacceptable.

---

## Study

### Embeddings

#### What embeddings are
- Dense vector representations of text, images, or documents
- Capture semantic meaning in geometry

#### Why embeddings enable retrieval
- Similar meanings → nearby vectors
- Enables nearest-neighbor search instead of keyword matching

#### Practical considerations
- Embedding dimensionality
- Domain-specific vs general embeddings
- Update frequency

---

### Vector Databases

#### What they do
- Store and index embeddings
- Support fast similarity search at scale

#### Common features
- Approximate nearest neighbor (ANN) search
- Metadata filtering
- Persistence and versioning

#### Why they matter
- Enable low-latency retrieval
- Scale to millions of documents

---

### Chunking Strategies

#### Why chunking is critical
- LLMs have context limits
- Retrieval operates on chunks, not full documents

#### Common chunking approaches
- Fixed-size chunks
- Sentence or paragraph-based chunks
- Overlapping windows

#### Tradeoffs
- Small chunks improve recall
- Large chunks improve coherence
- Overlap increases recall but adds cost

---

### Retrieval vs Generation Failures

#### Retrieval failures
- Relevant information not retrieved
- Caused by:
  - Poor chunking
  - Weak embeddings
  - Missing metadata filters

#### Generation failures
- Retrieved info is correct but misused
- Caused by:
  - Prompt ambiguity
  - Context overload
  - Model limitations

#### Debugging principle
- Always inspect retrieval before blaming the model

---

### Latency vs Accuracy Tradeoffs

#### Sources of latency
- Embedding computation
- Vector search
- Context construction
- Generation time

#### Accuracy considerations
- More chunks improve recall
- Larger context improves grounding
- Re-ranking improves relevance

#### Balancing strategy
- Retrieve fewer, higher-quality chunks
- Cache embeddings and results
- Use hybrid retrieval when needed

---

## Hands-On

- Build a **full RAG pipeline**
  - Document ingestion
  - Chunking and embedding
  - Vector storage
  - Retrieval
  - Prompted generation
- Test hallucination reduction
  - Compare with and without retrieval
  - Evaluate factual accuracy
  - Inspect failure cases

---

## Interview-Ready When You Can:

- Explain how embeddings power retrieval
- Describe chunking tradeoffs clearly
- Debug retrieval vs generation errors
- Justify latency decisions
- **Explain why RAG is essential in healthcare**
  - Medical knowledge changes frequently
  - Hallucinations are dangerous
  - RAG grounds responses in vetted sources
  - Enables auditability and traceability
