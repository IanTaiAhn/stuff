### Week 3 — ML Pipelines & Experimentation

#### Goal: Demonstrate professional ML workflow.

This week focuses on **how models are built in the real world**, not just trained once in a notebook. Interviewers want to see that you understand experimentation discipline, leakage risks (especially in healthcare), and how to make results trustworthy and reproducible.

---

## Study

### Train / Validation / Test Splits

#### What they are
- **Training set**
  - Used to fit model parameters
- **Validation set**
  - Used for model selection and hyperparameter tuning
- **Test set**
  - Held out until the very end
  - Used only for final performance estimation

#### Why proper splits matter
- Prevent overly optimistic results
- Simulate real-world deployment
- Ensure fair model comparison

#### Common splitting strategies
- **Random split**
  - Suitable for i.i.d. data
- **Time-based split**
  - Train on past, validate/test on future
  - Required for time series and many healthcare datasets
- **Entity-based split**
  - Split by patient, user, or device
  - Prevents learning individual-specific patterns

---

### Data Leakage (Critical for Healthcare)

#### What data leakage is
- Any information from the future or target that leaks into training
- Causes inflated performance that fails in production

#### Common leakage sources
- Aggregates computed over the full dataset
- Features derived from outcomes
- Using post-event data for prediction
- Random splits when entities repeat (patients, providers)

#### How to prevent leakage
- Perform splits **before** feature engineering
- Compute statistics using training data only
- Use time-based or entity-based splits
- Treat feature pipelines as part of the model

---

### Hyperparameter Tuning

#### What hyperparameters are
- Configuration values not learned during training
- Examples:
  - Learning rate
  - Tree depth
  - Regularization strength
  - Number of estimators

#### Why tuning matters
- Controls bias–variance tradeoff
- Improves generalization
- Prevents underfitting and overfitting

#### Best practices
- Tune using validation data only
- Keep test data untouched
- Start with coarse ranges, then refine

---

### Grid Search vs Random Search

#### Grid Search
- Exhaustively tests all parameter combinations
- Easy to understand and implement

**Pros**
- Deterministic
- Covers defined space completely

**Cons**
- Computationally expensive
- Inefficient in high-dimensional spaces

#### Random Search
- Samples parameter combinations randomly

**Pros**
- More efficient for large search spaces
- Finds good parameters faster
- Often outperforms grid search in practice

**Cons**
- Less predictable coverage
- Requires setting sensible parameter distributions

---

### Reproducibility

#### Why it matters
- Ensures results can be trusted
- Enables collaboration
- Required for regulated environments like healthcare

#### Key practices
- Set random seeds
- Version data and code
- Log hyperparameters and metrics
- Save model artifacts
- Record environment details

#### What breaks reproducibility
- Uncontrolled randomness
- Data changes without versioning
- Manual, undocumented steps

---

## Hands-On

- Build an **end-to-end ML pipeline**
  - Data loading
  - Cleaning and preprocessing
  - Feature engineering
  - Model training
  - Evaluation
- Track experiments
  - Hyperparameters
  - Metrics
  - Model versions
- Document assumptions
  - Data availability
  - Label definitions
  - Evaluation choices
  - Known limitations

---

## Interview-Ready When You Can Say:

- *“We split data by time or entity to reflect real-world deployment.”*
- *“All feature engineering was fit on training data only.”*
- *“Hyperparameters were tuned using validation data, not the test set.”*
- *“Experiments were tracked to ensure reproducibility and auditability.”*
- *“We ensured no leakage by splitting on time or entity rather than randomly.”*
