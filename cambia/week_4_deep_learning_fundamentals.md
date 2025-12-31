### PHASE 2 — Deep Learning & Data (Weeks 4–5)

### Week 4 — Deep Learning Fundamentals

#### Goal: Explain deep learning intuitively.

This week is about building **mental models** for deep learning. Interviewers are not looking for tensor math derivations—they want clear intuition for *why* these models work and *when* to use them.

---

## Study

### Activation Functions

#### What they do
- Introduce non-linearity into neural networks
- Allow models to learn complex patterns
- Without them, deep networks collapse into linear models

#### Common activation functions
- **ReLU**
  - Outputs max(0, x)
  - Fast and effective
  - Most widely used in hidden layers
- **Sigmoid**
  - Outputs values between 0 and 1
  - Often used for probabilities
- **Tanh**
  - Outputs values between -1 and 1
  - Zero-centered but can saturate

#### Practical intuition
- Activation functions decide **when neurons fire**
- ReLU keeps gradients flowing better than older activations

---

### Gradient Descent Issues (Vanishing Gradients)

#### What gradient descent does
- Adjusts weights to minimize loss
- Uses gradients to know which direction to move

#### Vanishing gradients
- Gradients shrink as they move backward through layers
- Early layers learn very slowly

#### Why this happens
- Repeated multiplication by small numbers
- Saturating activations like sigmoid and tanh

#### How it’s mitigated
- ReLU and variants
- Better initialization
- Normalization layers
- Residual connections

---

### CNNs (Why Convolution Works)

#### Core idea
- Learn **local patterns** and reuse them across space
- Same filter applied everywhere

#### Why this is powerful
- Fewer parameters than fully connected layers
- Translation invariance
- Hierarchical feature learning

#### Intuition
- Early layers detect edges
- Middle layers detect shapes
- Deeper layers detect objects or concepts

#### Common use cases
- Image classification
- Medical imaging
- Signal processing

---

### RNNs / LSTMs (Sequence Modeling)

#### What problem they solve
- Model ordered, sequential data
- Output depends on previous inputs

#### Why vanilla RNNs struggle
- Vanishing and exploding gradients
- Difficulty remembering long-term dependencies

#### How LSTMs help
- Gating mechanisms control information flow
- Separate memory cell preserves long-term context

#### Common applications
- Time series prediction
- Text processing
- Speech recognition

---

### GANs (Generator vs Discriminator)

#### What GANs are
- Two models trained together in a competitive setup

#### Generator
- Creates fake data
- Tries to fool the discriminator

#### Discriminator
- Distinguishes real data from fake data
- Provides feedback to the generator

#### Why GANs work
- Adversarial training pushes generator toward realism
- No explicit likelihood required

#### Challenges
- Training instability
- Mode collapse
- Hard to evaluate objectively

---

### Embeddings (Semantic Similarity)

#### What embeddings are
- Dense vector representations of entities
- Capture semantic meaning in geometry

#### Why they matter
- Similar items are close in vector space
- Enable similarity search and clustering

#### Common types
- Word embeddings
- Sentence embeddings
- Image embeddings
- Multimodal embeddings

#### Measuring similarity
- Cosine similarity
- Euclidean distance

---

## Hands-On

- Train a **simple neural network**
  - Use a small dataset
  - Observe training vs validation loss
  - Experiment with activation functions
- Generate embeddings
  - Encode text, images, or items
  - Measure similarity between examples
  - Visualize nearest neighbors

---

## Interview-Ready When You Can:

- Explain why deep networks need non-linear activations
- Describe vanishing gradients in simple terms
- Explain why convolution reduces parameters
- Contrast RNNs and LSTMs intuitively
- Explain adversarial training in GANs
- **Explain why embeddings power RAG and retrieval systems**
  - They turn meaning into geometry
  - Retrieval becomes nearest-neighbor search
  - Generation is grounded in relevant context
