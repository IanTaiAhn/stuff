### Week 7 — Prompt Engineering & Fine-Tuning

#### Goal: Know when not to fine-tune.

This week is about **control and restraint**. Strong GenAI practitioners know that fine-tuning is powerful—but often unnecessary, risky, or costly. Interviews favor candidates who can justify *not* fine-tuning and explain safer alternatives.

---

## Study

### Prompt Structures

#### Why structure matters
- LLMs respond strongly to format and clarity
- Well-structured prompts reduce variance and hallucinations

#### Common prompt components
- **Role**
  - Defines the model’s perspective
- **Task**
  - Clearly states what to do
- **Context**
  - Supplies necessary background
- **Constraints**
  - Specifies format, tone, or rules
- **Output format**
  - Reduces ambiguity

#### Practical takeaway
- Better prompts often outperform model changes

---

### Chain-of-Thought

#### What it is
- Encouraging the model to reason step-by-step

#### Why it helps
- Improves reasoning on multi-step tasks
- Makes logic more explicit

#### When to use it
- Math
- Logic
- Planning
- Complex decision-making

#### Caution
- Can increase latency
- Should not always be exposed to users

---

### Instruction Hierarchies

#### What they are
- Prioritized instruction layers that guide model behavior

#### Typical hierarchy
- System instructions
- Developer instructions
- User instructions

#### Why they matter
- Prevent prompt injection
- Enforce safety and consistency
- Separate policy from task logic

#### Best practice
- Put rules at higher levels
- Keep user prompts focused on intent

---

### Full Fine-Tuning vs LoRA vs QLoRA

#### Full fine-tuning
- Updates all model parameters

**Pros**
- Maximum control
- Deep behavioral changes

**Cons**
- Very expensive
- Risk of catastrophic forgetting
- Difficult to maintain

---

#### LoRA (Low-Rank Adaptation)
- Adds small trainable adapters
- Base model remains frozen

**Pros**
- Much cheaper than full fine-tuning
- Modular and reversible
- Lower risk of model drift

**Cons**
- Limited capacity for change
- Still requires training infrastructure

---

#### QLoRA
- LoRA applied to quantized models

**Pros**
- Extremely memory efficient
- Enables fine-tuning on limited hardware

**Cons**
- Added complexity
- Slight performance tradeoffs

---

### Tradeoffs (Cost, Drift, Latency)

#### Cost
- Training compute
- Storage and deployment
- Ongoing maintenance

#### Model drift
- Fine-tuned models can degrade over time
- Changes in data distribution amplify risk

#### Latency
- Larger models and complex prompts increase response time
- Fine-tuning does not eliminate inference costs

#### Decision principle
- Fine-tune only when prompting and retrieval fail

---

## Hands-On

- Complete a **prompt optimization task**
  - Improve output quality using structure and constraints
  - Compare naive vs optimized prompts
- LoRA fine-tune a small model
  - Observe learning behavior
  - Evaluate tradeoffs vs prompting alone

---

## Interview-Ready When You Can Say:

- *“We improved performance through prompt structure before changing the model.”*
- *“Chain-of-thought was used selectively for reasoning-heavy tasks.”*
- *“Instruction hierarchies protected against prompt injection.”*
- *“We evaluated LoRA before considering full fine-tuning.”*
- *“We avoided fine-tuning because RAG provided fresher knowledge with lower risk.”*
