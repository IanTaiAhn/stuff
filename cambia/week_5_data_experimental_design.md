### Week 5 — Data & Experimental Design

#### Goal: Think like a scientist, not a model jockey.

This week emphasizes **reasoning about data and evidence**, not just training models. Strong practitioners know how to ask the right questions, design clean experiments, and communicate what results *do and do not* mean.

---

## Study

### Research Questions vs Metrics

#### Research questions
- Define *what you want to learn*
- Are rooted in business, product, or clinical goals
- Example:
  - *Does this intervention improve patient outcomes?*

#### Metrics
- Define *how you measure progress*
- Are proxies, not the goal itself
- Example:
  - Accuracy, AUC, conversion rate, readmission rate

#### Common failure mode
- Optimizing metrics without answering the research question
- Improving numbers while missing real-world impact

#### Best practice
- Start with the question
- Choose metrics that directly reflect it
- Revisit metrics as understanding improves

---

### Confounding Variables

#### What a confounder is
- A variable that influences both:
  - The treatment or feature
  - The outcome

#### Why confounders matter
- Create misleading relationships
- Can make effects appear stronger or weaker than they are

#### Examples
- Health outcomes confounded by age or severity
- Model performance confounded by data source
- User behavior confounded by seasonality

#### Mitigation strategies
- Stratification
- Matching
- Including confounders as covariates
- Careful experimental design

---

### Correlation vs Causation

#### Correlation
- Two variables move together
- Does not imply one causes the other

#### Causation
- One variable directly influences another
- Requires stronger evidence

#### Why this matters in ML
- Models exploit correlations
- Correlations may break in new environments
- Spurious correlations reduce robustness

#### How causation is established
- Randomized experiments
- Natural experiments
- Strong domain reasoning

---

### Visualization Best Practices

#### Purpose of visualization
- Reveal patterns
- Communicate findings clearly
- Support reasoning, not decoration

#### Best practices
- Choose the right chart for the question
- Label axes clearly
- Use consistent scales
- Avoid misleading truncation
- Highlight uncertainty when possible

#### Common pitfalls
- Overloaded charts
- Cherry-picked ranges
- Decorative visuals that obscure insight

---

## Hands-On

- Design an **experiment**
  - Define hypothesis
  - Identify variables
  - Choose metrics
- Visualize results
  - Compare groups clearly
  - Show distributions, not just averages
  - Include uncertainty or variability
- Write conclusions
  - State what the data supports
  - Acknowledge limitations
  - Avoid overclaiming

---

## Interview-Ready When You Can Say:

- *“We defined the research question before selecting metrics.”*
- *“We controlled for confounding variables in the analysis.”*
- *“This relationship is correlational, not causal.”*
- *“The effect is statistically significant, but small in magnitude.”*
- *“This result is statistically significant, but not practically meaningful.”*
