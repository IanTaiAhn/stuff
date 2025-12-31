### Week 2 — Classic ML & Evaluation

#### Goal: Sound confident discussing traditional ML choices.

This week focuses on *why* you choose certain models and *how* you evaluate them. Interviewers care less about exotic algorithms and more about your ability to reason through tradeoffs, metrics, and failure modes.

---

## Study

### Linear / Logistic Regression

#### What they are
- **Linear regression**
  - Predicts a continuous value
  - Assumes a linear relationship between features and the target
- **Logistic regression**
  - Predicts probabilities for classification
  - Uses sigmoid or softmax to map outputs to probabilities

#### When to use them
- As strong baseline models
- When interpretability matters
- When data is small or noisy
- When relationships are approximately linear

#### Strengths
- Fast to train
- Easy to debug
- Coefficients are interpretable
- Less prone to overfitting with regularization

#### Weaknesses
- Cannot model complex non-linear relationships
- Sensitive to feature scaling
- Assumes linearity and independence

---

### Decision Trees

#### What they are
- Models that split data based on feature thresholds
- Create a tree of decision rules

#### When to use them
- When relationships are non-linear
- When interpretability is important
- When features interact

#### Strengths
- Easy to visualize and explain
- Handles mixed feature types
- No feature scaling required

#### Weaknesses
- High variance
- Easily overfit without constraints
- Sensitive to small data changes

---

### Random Forests

#### What they are
- An ensemble of decision trees
- Each tree is trained on a bootstrapped dataset with random feature subsets

#### Why they work
- Reduce variance by averaging many uncorrelated trees
- Individual tree errors cancel out

#### Strengths
- Strong out-of-the-box performance
- Handles non-linearity and feature interactions
- Robust to noise

#### Weaknesses
- Less interpretable than a single tree
- Higher memory usage
- Slower inference than linear models

---

### Gradient Boosting (GBM, XGBoost, LightGBM)

#### What they are
- Sequentially trained trees
- Each new tree focuses on correcting previous errors

#### When to use them
- Structured or tabular datasets
- When performance matters more than interpretability
- Production ML systems and competitions

#### Strengths
- Very high predictive power
- Captures complex relationships
- Built-in regularization options

#### Weaknesses
- Sensitive to hyperparameters
- Can overfit if not tuned properly
- Harder to explain intuitively

---

### Support Vector Machines (Intuition Only)

#### Core idea
- Find a decision boundary that maximizes the margin between classes
- Kernels allow modeling non-linear boundaries

#### When they work well
- Small to medium datasets
- Clear class separation

#### Limitations
- Poor scalability to large datasets
- Difficult to interpret
- Kernel choice is critical

---

### Collaborative Filtering

#### What it is
- A recommender system approach
- Learns from user–item interaction patterns

#### Main types
- **User-based**
  - Similar users → similar preferences
- **Item-based**
  - Similar items → similar users

#### Strengths
- No need for explicit features
- Learns directly from behavior

#### Weaknesses
- Cold start problem
- Sparse interaction matrices
- Limited explainability

---

### Ranking Problems

#### What they are
- Predict an ordered list rather than a single label
- Common in search engines, recommendations, and ads

#### How they differ from classification
- Order matters more than exact values
- Performance focuses on top-ranked items

#### Common approaches
- Pointwise: predict relevance scores
- Pairwise: predict which item is better
- Listwise: optimize ranking directly

---

## Evaluation

### Classification Metrics

#### Precision
- Of predicted positives, how many are correct
- Important when false positives are costly

#### Recall
- Of actual positives, how many were identified
- Important when false negatives are costly

#### F1 Score
- Harmonic mean of precision and recall
- Useful for imbalanced datasets

#### AUC (ROC-AUC)
- Measures ranking quality of predictions
- Threshold-independent
- Interpreted as the probability a random positive ranks above a random negative

---

### Regression Metrics

#### MAE (Mean Absolute Error)
- Average absolute prediction error
- Robust to outliers
- Easy to interpret

#### RMSE (Root Mean Squared Error)
- Penalizes large errors more heavily
- Sensitive to outliers
- Useful when large mistakes are especially costly

---

### Feature Importance

#### Why it matters
- Helps explain model behavior
- Identifies data leakage
- Guides feature engineering

#### Common techniques
- Tree-based importance
- Permutation importance
- SHAP values (conceptual understanding)

---

### Error Analysis

#### What it is
- Systematic inspection of model mistakes

#### How to do it
- Review worst predictions
- Segment errors by:
  - Feature values
  - Classes
  - Time
  - Sub-populations

#### Why it matters
- Reveals blind spots
- Improves model robustness
- Often more impactful than hyperparameter tuning

---

## Hands-On

- Train at least **two different models** on the same dataset
  - Examples:
    - Logistic Regression vs Random Forest
    - Linear Regression vs Gradient Boosting
- Compare:
  - Training vs validation performance
  - Precision/recall tradeoffs
  - Error distributions
- Explain:
  - Why one model performs better
  - What kinds of errors each model makes

---

## Interview-Ready When You Can:

- Justify metric choice based on business goals
- Explain why accuracy alone can be misleading
- Describe when a simple model outperforms a complex one
- Explain overfitting vs underfitting with concrete examples
- Identify failure modes and propose improvements
