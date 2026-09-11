# Small-model agentic AI — paper abstracts

Four papers on small/tiny language models for agentic (tool/function-calling) tasks, gathered while researching what's out there beyond the `harness_your_hopes` repo's own bare-metal Project 1 loop.

> **Note on sourcing:** direct fetches to arxiv.org, ar5iv.org, Semantic Scholar, and research.nvidia.com were all blocked by this session's network egress policy, so the abstracts below were reconstructed from search-engine result summaries rather than pulled verbatim from each paper's own abstract page. They should be accurate in substance, but treat exact wording as paraphrase, not a guaranteed direct quote — worth a quick check against the source link if you're going to cite one formally.

---

## 1. TinyLLM: Evaluation and Optimization of Small Language Models for Agentic Tasks on Edge Devices

**Authors:** Mohd Ariful Haque, Fahad Rahman, Kishor Datta Gupta, Khalil Shujaee, Roy George (Clark Atlanta University / United International University) — author list may be incomplete, one search result referenced "5 other authors" beyond the lead
**Date:** November 27, 2025 · **arXiv:** [2511.22138](https://arxiv.org/abs/2511.22138) · **Status:** preprint (no conference/workshop acceptance found)

> This paper investigates the effectiveness of small language models (SLMs) for agentic tasks (function/tool/API calling) with a focus on running agents on edge devices without reliance on cloud infrastructure. The paper evaluates SLMs using the Berkeley Function Calling Leaderboard (BFCL) framework and describes parameter-driven optimization strategies that include supervised fine-tuning (SFT), parameter-efficient fine-tuning (PEFT), reinforcement learning (RL)-based optimization, preference alignment via Direct Preference Optimization (DPO), and hybrid methods. Results are reported for models including TinyAgent, TinyLlama, Qwen, and xLAM across BFCL categories (simple, multiple, parallel, parallel-multiple, and relevance detection), both in live and non-live settings, and in multi-turn evaluations. Ultra-compact models (~600M–1.1B) reach only 20–45% overall accuracy; 1–3B models achieve 55–66% upon hybrid optimization.

---

## 2. Rethinking Scale: Deployment Trade-offs of Small Language Models under Agent Paradigms

**Authors:** Xinlin Wang, Mats Brorsson
**Date:** April 2026 · **arXiv:** [2604.19299](https://arxiv.org/abs/2604.19299) · **Status:** peer-reviewed — accepted, ACL 2026 Industry Track

> Despite the impressive capabilities of large language models, their substantial computational costs, latency, and privacy risks hinder their widespread deployment in real-world applications. Small Language Models (SLMs) with fewer than 10 billion parameters present a promising alternative; however, their inherent limitations in knowledge and reasoning curtail their effectiveness. Existing research primarily focuses on enhancing SLMs through scaling laws or fine-tuning strategies while overlooking the potential of using agent paradigms, such as tool use and multi-agent collaboration, to systematically compensate for the inherent weaknesses of small models. To address this gap, this paper presents the first large-scale, comprehensive study of <10B open-source models under three paradigms: (1) the base model, (2) a single agent equipped with tools, and (3) a multi-agent system with collaborative capabilities. The results show that single-agent systems achieve the best balance between performance and cost, while multi-agent setups add overhead with limited gains. The findings highlight the importance of agent-centric design for efficient and trustworthy deployment in resource-constrained settings.

---

## 3. Small Language Models are the Future of Agentic AI

**Authors:** Peter Belcak, Greg Heinrich, Shizhe Diao, Yonggan Fu, Xin Dong, Saurav Muralidharan, Yingyan Celine Lin, Pavlo Molchanov (NVIDIA Research)
**Date:** June 2026 · **arXiv:** [2506.02153](https://arxiv.org/abs/2506.02153) · **Status:** preprint / position paper

> Large language models (LLMs) are often praised for exhibiting near-human performance on a wide range of tasks and valued for their ability to hold a general conversation. The rise of agentic AI systems is, however, ushering in a mass of applications in which language models perform a small number of specialized tasks repetitively and with little variation. The paper lays out the position that small language models (SLMs) are sufficiently powerful, inherently more suitable, and necessarily more economical for many invocations in agentic systems, and are therefore the future of agentic AI. The argumentation is grounded in the current level of capabilities exhibited by SLMs, the common architectures of agentic systems, and the economy of LM deployment. The authors further argue that in situations where general-purpose conversational abilities are essential, heterogeneous agentic systems (i.e., agents invoking multiple different models) are the natural choice.

---

## 4. Toward a Modular Architecture for Embedded AI Agent Systems at the Edge

**Authors:** not retrieved (blocked fetches prevented confirming the author list)
**Date:** June 2026 · **arXiv:** [2606.02862](https://arxiv.org/abs/2606.02862) · **Status:** preprint

> The paper proposes a modular reference architecture for Embedded Agent Systems that bridges the divide between deterministic real-time control and agentic intelligence. The rise of Large Language Models (LLMs) has enabled agentic AI capable of complex reasoning and tool use; however, deploying such autonomy in pervasive computing environments remains challenging due to the strict memory and energy constraints of embedded microcontrollers. Existing frameworks typically assume server-class resources or continuous connectivity, leaving a gap for deeply embedded systems. The paper introduces a tiered design that decouples On-Device Agents — executing highly compressed neural networks and rule-based logic for low-latency, privacy-critical tasks — from Cloud-Augmented Agents that leverage Small Language Models (SLMs) for higher-level reasoning and planning. A key contribution is the integration of a cross-cutting Governance Layer, ensuring observability, policy enforcement, and safety across distributed fleets of autonomous devices. Rather than presenting purely empirical benchmarks, the paper analyzes architectural design principles and trade-offs regarding latency, energy, and reliable execution in resource-constrained environments.
