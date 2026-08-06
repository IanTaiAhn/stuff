# FAANG AI/ML Engineering Study Guide
*Built from current (mid-2026) job postings and interview-report patterns at Meta, Amazon, Google, Apple, and Netflix*

---

## 1. Read this first: pick your track

The single biggest mistake in self-study right now is treating "Machine Learning Engineer," "AI Software Engineer," and "Applied Scientist" as the same prep target. Current postings show they've split into genuinely different jobs with different day-to-day work and different interview emphasis. Figure out which one you're actually targeting before you build a study plan — it changes almost everything below.

| Track | What you actually ship | Core skill | Where it shows up at FAANG |
|---|---|---|---|
| **ML Engineer (MLE)** | A trained/deployed model (ranker, classifier, forecaster) | Training pipelines, feature engineering, MLOps, production serving | Meta "Software Engineer, ML," Amazon MLE, Netflix MLE, Apple ML org, Google SWE/ML |
| **AI / Applied AI Engineer** | A product feature built on *existing* foundation models (chatbots, agents, copilots) | RAG, prompt/agent design, evals, orchestration, latency & cost management | Newer titles: "AI Research Engineer," "GenAI Engineer," LLM-focused postings inside product orgs |
| **Applied Scientist / Research Scientist** | Novel modeling approaches, experiments, sometimes publications | Stats, experimental design, ML theory depth, research communication | Amazon "Applied Scientist," Netflix "Research Scientist/ML Scientist," Google PhD SWE tracks, Apple "Machine Learning Researcher" |

A useful rule of thumb from current market data: ML Engineer and AI Engineer postings share roughly two-thirds of their top skills (Python, cloud, LLMs generally show up in both) — but the remaining third is where they fork. MLE pulls toward scikit-learn, Spark, MLflow, and classical ML/statistics. AI Engineer pulls toward LangChain-style orchestration, vector databases, embeddings, and API-based model integration. If you're not sure which you're prepping for, look at whether the postings you're drawn to say "train/fine-tune models" (MLE track) or "integrate/orchestrate models" (AI Engineer track) — that's the fork.

**If you're targeting multiple tracks at once** (reasonable early in a search), prioritize the shared third (Python, coding fundamentals, one strong ML/LLM specialty) and treat the divergent skills as track-specific electives once you know which postings you're actually interviewing for.

---

## 2. What each company's postings are actually signaling

Patterns pulled across current listings — useful for tailoring prep once you know your target company, and for choosing which company to prioritize applying to given your existing strengths.

**Meta** — Postings are dominated by ranking and classification problems tied to specific product surfaces: feed/ads ranking, integrity/spam classification, recommendation, search. Distributed systems and "modern parallel environments" (GPU clusters, multicore) come up constantly. Increasingly, postings explicitly reference RAG-based search/retrieval and hallucination-reduction work layered on top of the classic ranking stack. Takeaway: study classic large-scale ranking/recsys deeply, then add a GenAI/RAG layer on top rather than starting from GenAI alone.

**Amazon** — The widest title sprawl of any FAANG company: "MLE," "Applied Scientist," "SDE-ML," and "AI/ML Specialist" all describe overlapping work, so read the responsibilities section, not the title. Two things are consistently emphasized that other companies mention less: (1) the Leadership Principles are woven into technical interviews, not just a separate behavioral round, and (2) production ownership — on-call for ML services, monitoring, and debugging live serving issues — is treated as core to the job, not a side responsibility. AWS-side postings (SageMaker, Bedrock) skew toward ML platform/infra work; retail-side postings skew toward ranking, forecasting, and fraud.

**Google** — Heavier on advanced-degree signaling than the others; many SWE/ML postings explicitly list PhD as a qualification (or prefer it), especially for research-adjacent roles. Requirements consistently emphasize large-scale distributed systems experience and depth in a specific deep learning framework (TensorFlow/JAX/PyTorch). Full-stack versatility is explicitly called out — Google wants engineers comfortable from low-level infrastructure and compilers up through model architecture.

**Apple** — A recurring surprise in candidate reports: people prep like it's a research role and get caught off guard by how production-engineering-heavy the actual loop is. Postings center on recommendation/personalization for App Store, Apple Music, and Siri, with a strong and growing GenAI layer (RAG, transformers, agentic workflows, fine-tuning, LLM evaluation) layered on top of a traditional MLOps stack (Kubernetes, Airflow, Docker, Ray). Privacy-by-design shows up as a recurring non-technical theme worth being ready to discuss.

**Netflix** — Distinct in two ways: heavy emphasis on experimentation and causal inference (not just point-in-time model accuracy — Netflix cares a lot about how you validate impact), and a real research track (Research Scientist / ML Scientist titles) alongside the engineering track. Personalization, member/title understanding, and pricing science are recurring domains. LLM post-training and multimodal (text/image/video/audio) work is now showing up in senior postings.

---

## 3. What the interview loop actually tests (this is where postings fall short)

Job postings tell you *what the team works on*; they tell you almost nothing about *how you'll be evaluated*. Across current candidate reports, the FAANG ML/AI loop is fairly consistent in shape:

1. **Recruiter screen + 1–2 phone screens** — often one coding-focused, sometimes one ML-breadth focused.
2. **Coding / DS&A round(s)** — standard LeetCode-style algorithmic coding. Not ML-specific. This round doesn't disappear just because the role is "ML" — arrays/strings, hash maps, trees/graphs, and complexity analysis are still tested directly.
3. **ML system design round** — the highest-leverage round to prepare for and the one people most underrate. Expect to scope a vague product problem (e.g., "design a feed ranking system" or, increasingly, "design a RAG-based support agent") end to end: data pipeline, feature/embedding strategy, model choice, training approach, serving/latency constraints, monitoring, and failure modes. As of 2026, a growing share of these rounds specifically test GenAI system patterns (RAG vs. fine-tuning vs. hybrid, agent tool-use design, hallucination mitigation under latency constraints) alongside the classic recsys/ranking design pattern.
4. **ML theory / breadth round** — shorter, conversational: explain a concept, defend a modeling choice, reason about metrics and failure modes. Tests communication as much as depth.
5. **Behavioral round(s)** — do not underweight this. Current guidance puts behavioral at 30–40% of the evaluation weight in the 2026 loop, and it's a common place strong technical candidates lose offers. Amazon in particular evaluates Leadership Principles directly inside technical rounds, not just a standalone round.
6. **Domain-specific / team-match conversation** — often with the hiring manager, digging into your past projects and how you handled ambiguity, offline/online metric tradeoffs, and stakeholder alignment.

System design becomes a required, heavily weighted round from roughly mid-level (L4/E4/SDE-2, Amazon L5) upward; junior/entry loops lean more on coding + ML fundamentals.

---

## 4. Weighted study topics

Ranked roughly by how consistently they appear across current postings + interview reports. Treat "Core" as non-negotiable regardless of company or track; "Track-specific" as high-value only for one track; "Nice-to-have" as differentiators, not requirements.

**Core (all three tracks, every FAANG company)**
- Data structures & algorithms — arrays/strings, hash maps, trees/graphs, sliding window/two pointers, complexity analysis. This is tested even in "ML" loops.
- Python fluency, written production-quality (readability, edge cases, not just correctness)
- ML fundamentals: supervised/unsupervised learning, evaluation metrics, bias-variance, overfitting, regularization
- ML/ GenAI system design as a *practiced skill* — not just knowledge, but the ability to narrate a design out loud under interviewer pushback
- Behavioral prep — STAR-formatted stories covering conflict, ambiguity, ownership, failure/learning. For Amazon specifically, map stories directly onto the Leadership Principles.

**High-priority, track-specific**

*ML Engineer track:*
- Feature engineering and pipelines (batch + streaming)
- Deep learning architecture fundamentals (transformers, CNNs where relevant to the team's domain)
- Distributed training and large-scale serving constraints (latency, throughput, cost)
- MLOps: experiment tracking, CI/CD for models, monitoring/drift detection, one cloud stack (AWS/GCP) in depth rather than all three shallowly
- Recommendation systems / ranking specifically if targeting Meta, Netflix, or Apple

*AI / Applied AI Engineer track:*
- RAG architecture end to end (chunking, embeddings, retrieval, re-ranking)
- Agent/tool-use design patterns and orchestration frameworks
- LLM evaluation methodology (hallucination detection, offline/online eval design)
- Prompt engineering as a rigorous discipline, not trial-and-error
- Latency and token-cost tradeoffs in production LLM systems
- Vector database fundamentals

*Applied Scientist track:*
- Experimental design and causal inference (especially for Amazon, Netflix)
- Statistical rigor: hypothesis testing, confidence intervals, common pitfalls in online experimentation
- Research communication — explaining technical tradeoffs to non-technical stakeholders
- Depth in one specialty (NLP, CV, RL, or recsys) rather than breadth — current data shows a majority of ML-adjacent postings now prefer domain depth over generalist breadth

**Lower priority / commonly over-studied**
- Advanced/niche algorithms — GANs, GNNs, Bayesian methods appear in a small minority of postings; don't let textbook curricula convince you these are core.
- Deep theoretical proofs of classical ML algorithms — useful for research-heavy roles, rarely tested directly in engineering loops.

---

## 5. Suggested prep sequence

1. **Lock your track and 2–3 target companies** before building flashcards or a curriculum — this guide's weighting shifts meaningfully by track.
2. **Coding fundamentals first**, even if the role is ML — it's tested in nearly every loop and is the fastest way to get eliminated if weak.
3. **Pick one ML system design framework** (problem scoping → data → modeling → serving → monitoring) and drill it against both a classic problem (ranking/recsys) and a GenAI problem (RAG-based agent) — current loops test both.
4. **Build 6–8 behavioral stories** early, not last. Map them to Amazon's Leadership Principles even if Amazon isn't your top choice — the exercise transfers.
5. **Go deep, not broad, in your specialty** — the data is consistent that domain depth is now weighted over generalist breadth across nearly all these postings.
6. **Layer in company-specific homework** in the final 1–2 weeks: read the specific team's postings closely, check Glassdoor/Blind for that team's recent interview reports, and understand the product surface you'd actually work on.

---

## 6. What this guide can't tell you (be honest with yourself about this)

- Postings mix "must-have" and "wish-list" requirements without labeling which is which — don't assume you need every listed tool.
- The exact interview format for a *specific team* varies more than company-wide guides suggest — always ask your recruiter what the loop emphasizes once you're scheduled.
- Compensation, leveling, and team-specific culture notes above are directional, not guaranteed — they'll shift with the market and with the specific team.
- This guide is a snapshot of current listings; refresh the topic weighting every few months, especially the GenAI/LLM sections, which are moving fastest.
