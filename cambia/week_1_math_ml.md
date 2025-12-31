### Week 1 — Math & ML Core Foundations

#### Goal
Be able to reason about models, not just run them.

---

## 1. Linear Algebra (Mental Models, Not Proofs)

### 1.1 Vectors

**What they are**
- A vector is an ordered list of numbers
- In ML: a single data point or feature representation

**How to reason about them**
- Think of a vector as a point in space
- Each dimension = one feature
- Distance between vectors ≈ similarity

**ML intuition**
- Models try to learn directions in vector space
- Classification = separating regions in space
- Regression = fitting a surface through points

---

### 1.2 Matrices

**What they are**
- A collection of vectors stacked together

**In ML**
- Dataset = matrix
  - Rows = samples
  - Columns = features
- Weight matrix = how features are combined

**Mental model**
- A matrix is a transformation that stretches, rotates, or compresses space

---

### 1.3 Dot Product

**Definition (intuition only)**
- Measures how aligned two vectors are

**Why it matters**
- Core of:
  - Linear regression
  - Logistic regression
  - Neural networks
  - Attention mechanisms

**Mental shortcut**
- Large dot product → strong alignment
- Zero → orthogonal (unrelated)
- Negative → opposing directions

---

### 1.4 Eigen Intuition (No Math)

**What eigenvectors represent**
- Directions that don’t change direction when transformed
- Only scaled, not rotated

**Why ML cares**
- PCA finds eigenvectors of the covariance matrix
- These are principal directions of variance
- Helps reduce dimensionality while preserving signal

**Interview framing**
> “Eigenvectors capture the dominant patterns in the data.”

---

## 2. Probability (How Models Handle Uncertainty)

### 2.1 Distributions

**What they represent**
- How often values occur

**Common ML distributions**
- Normal: noise, errors
- Bernoulli: binary outcomes
- Categorical: class probabilities

**ML connection**
- Model outputs are often probabilities
- Loss functions assume specific distributions

---

### 2.2 Expectation

**What it means**
- Long-run average outcome

**ML intuition**
- Training minimizes expected loss
- Not optimizing one data point, but average behavior

---

### 2.3 Variance

**What it measures**
- How spread out values are

**Why it matters**
- High variance models:
  - Sensitive to noise
  - Overfit training data
- Low variance models:
  - Stable
  - May underfit

---

### 2.4 Bayes’ Rule

**Core idea**
- Update beliefs when new evidence arrives

**ML intuition**
- Prior: what we believe before seeing data
- Likelihood: how data supports hypotheses
- Posterior: updated belief

**Interview-ready explanation**
> “Bayes’ rule formalizes how models update uncertainty when observing data.”

---

## 3. Statistics (Making Claims with Data)

### 3.1 Hypothesis Testing

**Purpose**
- Decide if an observed effect is likely real or due to chance

**Key components**
- Null hypothesis: no effect
- Alternative hypothesis: effect exists
- p-value: probability of observing results under null

**ML relevance**
- Feature selection
- A/B testing models
- Evaluating improvements

---

### 3.2 Confidence Intervals

**What they are**
- Range where the true value likely lies

**Why they matter**
- Model metrics have uncertainty
- Business decisions shouldn’t rely on point estimates only

**Interview framing**
> “Confidence intervals communicate model reliability, not just accuracy.”

---

## 4. Calculus (Optimization Intuition Only)

### 4.1 Gradients

**What a gradient represents**
- Direction of steepest increase

**In ML**
- We move against the gradient to reduce loss

**Mental model**
- Standing on a hill blindfolded, feeling the slope with your feet

---

### 4.2 Partial Derivatives

**Why they matter**
- Models have many parameters
- Each parameter affects loss differently

**Intuition**
- Ask: *If I change this weight slightly, what happens to the loss?*

---

## 5. Core ML Concepts (Where Math Becomes Modeling)

### 5.1 Objective (Loss) Functions

**What they do**
- Translate “bad predictions” into numbers

**Examples**
- MSE → regression
- Cross-entropy → classification

**Key insight**
- Choosing a loss function is a business decision, not just technical

**Interview line**
> “The loss function defines what the model is optimizing for.”

---

### 5.2 Regularization (L1 vs L2)

**Why regularization exists**
- Models can memorize noise
- Regularization penalizes complexity

**L1 (Lasso)**
- Encourages sparsity
- Feature selection
- Some weights go to zero

**L2 (Ridge)**
- Shrinks weights smoothly
- Reduces sensitivity
- Keeps all features but weakens them

**Mental model**
- L1: “Use fewer knobs”
- L2: “Turn knobs gently”

---

### 5.3 Bias–Variance Tradeoff

**Bias**
- Error from overly simple assumptions

**Variance**
- Error from sensitivity to noise

**Key insight**
- You can’t minimize both perfectly
- Regularization shifts this balance

**Interview framing**
> “Regularization increases bias slightly to reduce variance significantly.”

---

### 5.4 Overfitting vs Underfitting

| Problem        | Symptoms                          | Fix                              |
|---------------|-----------------------------------|----------------------------------|
| Underfitting  | Poor train & test performance     | More features, complex model     |
| Overfitting   | Great train, poor test performance| Regularization, more data        |

**Mental shortcut**
- Underfitting = model too dumb
- Overfitting = model too confident

---

## 6. Deliverables (You Should Be Able to Explain)

### Explain: Why Regularization Reduces Overfitting

**Strong answer**
> “Regularization penalizes large or unnecessary weights, which limits model complexity. This prevents the model from fitting noise in the training data, reducing variance and improving generalization.”

---

### Explain: Gradient Descent Without Equations

**Strong answer**
> “Gradient descent iteratively adjusts model parameters by moving in the direction that most reduces error. At each step, the model checks which direction lowers the loss the fastest and takes a small step that way until improvements level off.”
