# Workflow Graphs for LLM Agents: A Production-Grounded Guide

A quick note before the taxonomy: there is no single agreed-upon naming scheme for these patterns. Anthropic, Google's Agent Development Kit, LangChain, AWS, and academic surveys have each published their own vocabulary, and a 2026 arXiv survey on agent design patterns calls this out explicitly — every major AI lab has shipped its own framework for describing the same handful of underlying graph shapes. So terms like "umbrella-shaped" aren't standardized industry vocabulary; they're descriptive shorthand for a graph topology that *does* have a standard name (orchestrator-worker / hierarchical / hub-and-spoke). This guide maps the common shapes to their canonical names and tells you, with sources, which ones are actually load-bearing in production versus which are mostly demo-ware.

---

## The foundational split: workflows vs. agents

Anthropic's engineering team, drawing on work with "dozens of teams building LLM agents across industries," draws one core architectural line:

- **Workflows** — LLMs and tools orchestrated through code paths a developer defines in advance. The graph's edges are fixed at design time.
- **Agents** — the LLM itself decides what happens next at each step. The graph's edges are chosen at runtime, and the graph can be cyclic and open-ended.

Their blunt finding, after that many production engagements: **the most successful implementations use simple, composable workflow patterns, not complex autonomous frameworks.** Full autonomy is the exception, reserved for tasks that genuinely can't be hardcoded. [(Anthropic, "Building Effective Agents," Dec 2024)](https://www.anthropic.com/engineering/building-effective-agents)

Keep that finding in mind — it's the thread running through everything below.

---

## Part 1 — The six workflow shapes (Anthropic's canonical taxonomy)

This is the most-cited practical taxonomy in the industry, and it's the one Spring AI, AWS's prescriptive guidance, and most framework docs build on top of. Each pattern is a distinct graph shape.

### 0. The augmented LLM (the atomic node)
A single LLM call with tools, retrieval, and memory attached. Not a graph by itself, but every pattern below is built from this unit.

### 1. Prompt chaining — linear pipeline / DAG
Task is decomposed into a fixed sequence of LLM calls, each consuming the previous step's output. You can insert programmatic "gate" checks between steps.
**Graph shape:** a straight line (a simple DAG). **Good for:** tasks that decompose cleanly into fixed stages — e.g., draft an outline → validate it against criteria → write the full document. Anthropic trades latency for accuracy here: each call gets an easier sub-task.

### 2. Routing — branching graph
A classifier step (LLM or traditional model) sends the input down one of several specialized downstream paths.
**Graph shape:** a switch/branch. **Good for:** distinct input categories that shouldn't share a prompt — e.g., sending easy queries to a cheap model and hard ones to a stronger model, or splitting billing vs. technical support tickets.

### 3. Parallelization — fan-out / fan-in
Two flavors: **sectioning** (split a task into independent subtasks run concurrently) and **voting** (run the same task N times for diverse outputs, then aggregate). Critically, the subtasks are *fixed in advance* by the developer.
**Graph shape:** fan-out to parallel branches, fan-in to an aggregator. **Good for:** guardrail checks running alongside the main response, or multiple independent reviewers voting on whether code has a vulnerability.

### 4. Orchestrator-workers — the "umbrella" shape
A central LLM dynamically decomposes the task and delegates pieces to worker LLMs, then synthesizes their results. This is topologically similar to parallelization — central hub, radiating branches, converging back — which is exactly the umbrella silhouette. **The difference that matters:** in parallelization the subtasks are pre-defined; here the orchestrator decides the number and nature of subtasks *at runtime*, based on what it sees. [(Anthropic)](https://www.anthropic.com/engineering/building-effective-agents)
**Good for:** tasks where you can't predict the shape of the work ahead of time — e.g., a coding agent that doesn't know how many files it'll need to touch until it looks at the codebase, or research tasks requiring an unknown number of independent searches.

### 5. Evaluator-optimizer — a loop
One LLM generates, a second LLM critiques against explicit criteria, and the loop repeats until the evaluator is satisfied.
**Graph shape:** a two-node cycle. **Good for:** literary translation, or any task where you can articulate what "better" looks like and an LLM can reliably judge against it.

---

## Part 2 — The free-flowing agent loop (ReAct-style)

This is what you're calling "free-flow." Formally, it traces back to **ReAct: Synergizing Reasoning and Acting in Language Models** (Yao, Zhao, Yu, Du, Shafran, Narasimhan, Cao — ICLR 2023). The idea: interleave explicit reasoning traces ("thoughts") with actions and environment observations in a single loop, rather than doing reasoning and acting as separate phases. <cite index="12-1">The reasoning traces help the model induce, track, and update action plans and handle exceptions, while actions let it interface with external sources like a knowledge base or environment to gather additional information.</cite>

The paper's actual numbers, for grounding: <cite index="13-1">on question answering (HotpotQA) and fact verification (Fever), ReAct overcomes issues of hallucination and error propagation prevalent in chain-of-thought reasoning by interacting with a Wikipedia API. On two interactive decision-making benchmarks (ALFWorld and WebShop), ReAct outperformed imitation and reinforcement learning methods by an absolute success rate of 34% and 10% respectively</cite>, using only one or two in-context examples.

**Graph shape:** technically a single node with a self-loop (think → act → observe → think again), unrolled until a stop condition — max iterations, task completion, or a human checkpoint. There's no fixed depth and no fixed set of next steps; the model picks the edge at every turn. This is what Anthropic calls simply "Agents" in their taxonomy above, and what most "autonomous agent" frameworks (AutoGPT-style loops, coding agents, computer-use agents) are built on under the hood.

**A close cousin worth knowing: plan-and-execute.** Rather than deciding one step at a time, the model produces an upfront plan, then executes each step (often with its own ReAct-style sub-loop), replanning if something breaks. This trades some flexibility for more predictability and cheaper planning overhead — useful when the task is complex but not fully unknowable upfront.

**Where this actually ships in production:** Anthropic's own SWE-bench coding agent and their "computer use" reference implementation are both this pattern — an LLM using tools in a loop based on environmental feedback, with the primary engineering effort spent on the tool interface (the "agent-computer interface") rather than the loop logic itself. <cite index="10-1">The autonomous nature of agents means higher costs and the potential for compounding errors, so Anthropic recommends extensive testing in sandboxed environments along with appropriate guardrails</cite> — this pattern is powerful but the least predictable of everything in this guide, and the one most likely to burn tokens on unproductive loops if the toolset is poorly specified.

---

## Part 3 — Multi-agent topologies

Once you have more than one *independently reasoning* LLM (not just parallel calls, but agents that can each make their own tool-use decisions), you get a second layer of graph shapes describing how the agents relate to each other.

### Hierarchical / supervisor / orchestrator-worker (the umbrella, multi-agent version)
A supervisor LLM receives all input, decides which specialized agent handles it, delegates, and translates the result back — sub-agents never talk to the user directly. This is the most heavily production-validated multi-agent shape, and it's worth walking through the best-documented real deployment in detail.

**Flagship production example: Anthropic's own multi-agent Research system.** A lead orchestrator agent (Claude Opus) analyzes a query, plans a strategy, and spins up 3–5+ specialized subagents (Claude Sonnet) in parallel, each with its own context window and search tools, before a separate synthesis pass compiles the findings. On Anthropic's internal evaluation, this beat a single-agent baseline by **90.2%** — but at roughly **15x the token cost** of a normal chat turn, which Anthropic is explicit about as the real tradeoff. Early versions of the system over-spawned subagents for simple questions and had subagents duplicate each other's work when task boundaries weren't explicit enough; fixing that required hard-coded effort-scaling rules in the orchestrator's prompt (roughly: 1 agent for simple fact-finding, 2–4 for direct comparisons, 10+ only for genuinely broad research). [(ZenML LLMOps case study, drawn from Anthropic's engineering writeup)](https://www.zenml.io/llmops-database/building-a-multi-agent-research-system-for-complex-information-tasks)

Anthropic followed this up with a pointed caveat that matters a lot for anyone about to build this pattern: <cite index="25-1">multi-agent systems are often applied in situations where a single agent would actually perform better, and domains that require all agents to share the same context or involve many dependencies between agents are not a good fit for multi-agent systems today — most coding and debugging workflows fail that test</cite>. [(Claude/Anthropic, "When to use multi-agent systems")](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them) In other words: the umbrella shape earns its keep specifically on *breadth-first, independently-parallelizable* work (research, comparison, gathering) — not on tightly coupled work where one agent's output determines what the next needs to do.

**Also in production:** LinkedIn built a hierarchical/supervisor agent system on LangGraph for their AI recruiting product, coordinating candidate sourcing, matching, and messaging under one supervisor. [(LangChain customer story)](https://www.langchain.com/built-with-langgraph)

### Network / mesh (peer-to-peer)
Every agent can call every other agent — no fixed hierarchy, no single entry point. Suited to problems with no natural ordering or clear chain of command, but the least predictable and hardest to debug of the multi-agent shapes since control flow isn't centrally legible.

### Swarm / handoff (decentralized)
Agents hand off control to each other directly via "handoff tools," and — critically — any agent can respond to the user, not just a central coordinator. LangChain ran a direct empirical comparison of supervisor vs. swarm architectures on the same tasks and found something specific: the supervisor pattern's main failure mode was a "telephone game" problem, where the supervisor has to translate between the user and sub-agents because only it is allowed to respond, and information gets lost or garbled in that translation layer. The swarm pattern avoided this because sub-agents could respond directly. [(LangChain, "Benchmarking Multi-Agent Architectures")](https://blog.langchain.com/benchmarking-multi-agent-architectures/) The tradeoff: swarms require every agent to know about every agent it might hand off to, which breaks down once you're integrating third-party or loosely-coupled agents.

### Sequential agent pipeline
The multi-agent analogue of prompt chaining — agent A finishes and hands off to agent B in a fixed order. Simplest to reason about, least flexible.

---

## Part 4 — What's actually deployed and validated, with sources

Framework adoption numbers circulating in 2026 industry blogs (GitHub star counts, "X% of enterprises," download counts) are noisy and often vendor-promoted — treat those skeptically unless they cite a company's own engineering blog. The deployments below are ones with a named company and a traceable primary or near-primary source.

| Deployment | Pattern | Framework | Reported outcome | Source |
|---|---|---|---|---|
| Anthropic Claude Research | Orchestrator-workers (umbrella) | Claude Agent SDK | 90.2% quality improvement vs. single agent; 15x token cost | [Anthropic via ZenML](https://www.zenml.io/llmops-database/building-a-multi-agent-research-system-for-complex-information-tasks) |
| Anthropic SWE-bench coding agent | ReAct-style autonomous loop | Custom | Solves real GitHub issues from PR description alone | [Anthropic](https://www.anthropic.com/engineering/building-effective-agents) |
| Klarna AI Assistant | Workflow + agent hybrid | LangGraph | 80% reduction in customer resolution time, 85M active users | [LangChain](https://www.langchain.com/built-with-langgraph) |
| LinkedIn AI recruiter | Hierarchical/supervisor | LangGraph | Automated candidate sourcing/matching, freed recruiter time for strategy | [LangChain](https://www.langchain.com/built-with-langgraph) |
| Uber Developer Platform | Multi-agent network | LangGraph | Automated unit-test generation for large-scale code migrations | [LangChain](https://www.langchain.com/built-with-langgraph) |
| AppFolio (Realm-X) | Workflow orchestration | LangGraph | 2x response accuracy, 10+ hours/week saved per property manager | [LangChain](https://www.langchain.com/built-with-langgraph) |
| Elastic | Orchestrated agents | LangGraph | Reduced manual SecOps threat-detection work | [LangChain](https://www.langchain.com/built-with-langgraph) |

The pattern across all of these: **every single one is either a plain workflow or a hierarchical/orchestrator shape.** None of the well-sourced production deployments are peer-to-peer mesh or fully autonomous open-ended agents — those show up far more in demos and research papers than in shipped systems with reported business metrics. That lines up exactly with Anthropic's own finding at the top of this guide.

---

## Part 5 — Decision cheat-sheet

| If your task looks like... | Use... |
|---|---|
| Fixed sequence of transformations | Prompt chaining |
| Distinct input categories needing different handling | Routing |
| Independent subtasks you can enumerate in advance | Parallelization (sectioning/voting) |
| Subtasks you *can't* enumerate until you see the input | Orchestrator-workers ("umbrella") |
| A generation task with clear, articulable quality criteria | Evaluator-optimizer |
| Open-ended, can't hardcode the number of steps, tools give ground truth | ReAct-style autonomous loop |
| Breadth-first research/comparison across independent sources, cost is secondary to quality | Multi-agent orchestrator-worker |
| Specialized agents where the user should talk to whichever is active | Swarm/handoff |
| Tightly coupled steps where each depends on full context of the last | **Don't multi-agent this** — use one agent or a tight sequential chain instead |

And the meta-rule, straight from the source with the most production mileage behind it: start with the simplest pattern that passes your evaluation — often a single well-tooled LLM call — and only add graph complexity when you can show it demonstrably improves outcomes.

---

## A note on how well this has aged (Dec 2024 → mid-2026)

The Anthropic post this guide leans on most is now about 20 months old, which is a long time in this field. Worth being precise about what has and hasn't changed:

**What's held up:** the six-pattern taxonomy itself. It hasn't been contradicted or replaced — Anthropic's own subsequent posts build on top of it rather than revising it, and it's still the most-cited reference framework across vendors (Google's ADK, LangChain's docs, AWS's prescriptive guidance all use it as a common reference point).

**What's actually new since then:**

- **Context engineering as its own discipline.** The original post didn't address what happens when an agent runs long enough that its context window fills with stale tool outputs — a failure mode Anthropic now names "context rot." Their Sept 2025 follow-up, ["Effective Context Engineering for AI Agents,"](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) lays out three fixes: **compaction** (summarize and reinitialize near the context limit), **structured note-taking** (persist state outside the context window entirely), and using **multi-agent architecture specifically for context isolation** — each subagent burns tens of thousands of tokens exploring but returns only a 1,000–2,000 token distilled summary. That's a new reason to reach for the orchestrator-worker shape beyond "I can't predict the subtasks upfront" — it's now also "I need to keep the lead agent's context clean."
- **Sharper multi-agent guidance.** The Jan 2026 "when to use multi-agent systems" post cited throughout this guide is itself evidence of refinement — it's much more pointed about failure modes (tightly-coupled domains like coding) and introduces sub-patterns like verification subagents that weren't in the original.
- **These patterns got productized.** The Claude Agent SDK and, as of April 2026, **Claude Managed Agents** — hosted infrastructure handling sandboxing, state persistence, and crash recovery that previously took engineering teams 3–6 months to build by hand.
- **Protocol standardization.** MCP matured from a Nov 2024 announcement into a versioned spec; Google's Agent2Agent (A2A) protocol emerged to standardize cross-vendor agent-to-agent communication, relevant to the network/swarm topologies above.
- **Enterprise usage is shifting toward genuinely complex deployments.** Anthropic's 2026 enterprise survey found 57% of organizations now run multi-stage agent workflows and 16% run cross-functional processes spanning teams — up substantially from the simpler single-task automations that dominated in 2024–2025. [(Anthropic, "How Enterprises Are Building AI Agents in 2026")](https://claude.com/blog/how-enterprises-are-building-ai-agents-in-2026)

**Net read:** the graph shapes in this guide are durable. What's moved is how you manage state *within* those shapes at production scale, and how much of the plumbing you now get for free versus having to build yourself.

---

## Sources

- Anthropic, ["Building Effective Agents"](https://www.anthropic.com/engineering/building-effective-agents) (Dec 2024) — primary source for the six-pattern taxonomy
- Anthropic / Claude, ["When to use multi-agent systems (and when not to)"](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them)
- Yao et al., ["ReAct: Synergizing Reasoning and Acting in Language Models"](https://arxiv.org/pdf/2210.03629), ICLR 2023
- ZenML LLMOps Database, ["Anthropic: Building a Multi-Agent Research System"](https://www.zenml.io/llmops-database/building-a-multi-agent-research-system-for-complex-information-tasks)
- LangChain, ["Built with LangGraph" customer stories](https://www.langchain.com/built-with-langgraph) (LinkedIn, Uber, Klarna, Elastic, AppFolio)
- LangChain, ["Benchmarking Multi-Agent Architectures"](https://blog.langchain.com/benchmarking-multi-agent-architectures/) — supervisor vs. swarm empirical comparison
- LangChain, [multi-agent supervisor library docs](https://reference.langchain.com/python/langgraph-supervisor) and [swarm library docs](https://github.com/langchain-ai/langgraph-swarm-py)
- AWS Prescriptive Guidance, ["Agentic AI patterns and workflows on AWS"](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html)
- arXiv, ["A Two-Dimensional Framework for AI Agent Design Patterns"](https://arxiv.org/pdf/2605.13850) — documents the fragmented state of agent-pattern taxonomies across vendors
- Anthropic, ["Effective Context Engineering for AI Agents"](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (Sept 2025)
- Anthropic, ["How Enterprises Are Building AI Agents in 2026"](https://claude.com/blog/how-enterprises-are-building-ai-agents-in-2026)