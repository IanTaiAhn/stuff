SONNET 5 High Initial:
I built a local, Ollama-powered text-based dungeon crawler RPG to learn how agentic coding tools are called in a DAG type architecture.

**The project**

AI Dungeon Crawler pairs an LLM "Dungeon Master" for narration that is grounded via RAG from a markdown lore corpus (md file) with a deterministic rules engine for combat, inventory, and movement (langgraph). The design was meant to help me learn agentic looping and make it a little funner for me since rpgs are fun. Everything runs locally via Ollama so you can play it yourself, granted you follow the README in the repo. There are options to play it manually, or you can select another agent (slm) to play the game for you and watch how an agentic loop works itself out as it observes and acts based on state.

**Studying harness engineering directly**

In parallel I made a self-study repo structured as a "ladder" of progressively harder agent-harness projects, each targeting a specific failure mode against local Ollama models: a bare-metal tool loop, surviving a restart, a permission-gated file agent, a generator-evaluator loop, and a capstone coding agent with ablation runs.

This self-study repo along with my AI Dungeon Crawler app showed me something about agent/coding harnesses.

**Where OpenCode broke**

I took the same small local models running my AI Dungeon Crawler and agentic harness self-study repos (Qwen2.5-Instruct, 7B and 14B) and pointed OpenCode at them, expecting a mature framework to outperform my own harness by a wide margin. Instead, it couldn't reliably do things as simple as printing the current working directory or writing a .txt file into the repo. The models kept failing to produce output matching OpenCode's tool-calling JSON schema, so the agentic loop broke down before the model ever got a chance to reason.

My own harness handled these tasks and more when using the same models without issue.

**Takeaway**

This told me OpenCode is built assuming you're running a pretty strong model behind it. Swap in something smaller and it doesn't fail gracefully, it just breaks on basic tool calls. My own harness, scoped down to only the tools I actually needed, ran those same small models fine. Small models still do great for regular chat. But if you actually want them acting as agents, scoping your own harness to the task beats relying on a general framework built for bigger models.

---

AI Dungeon Crawler (text-based RPG): [link]
Agent harness ladder — the study repo behind the OpenCode comparison: [link]



OPUS 5 Medium Rewrite:
A 14B model couldn't print its own working directory through OpenCode. The same model, same machine, same Ollama setup, ran a coding agent I wrote myself without issue.

I'd been building two things to learn how agentic coding tools actually work under the hood. The first is a text-based dungeon crawler RPG — an LLM "Dungeon Master" narrating from a markdown lore corpus via RAG, paired with a deterministic rules engine for combat, inventory, and movement, wired together in LangGraph. You can play it manually or hand it to a small model and watch the agent loop observe and act on state. The second is a self-study repo structured as a ladder of progressively harder harness projects, each targeting one failure mode: a bare-metal tool loop, surviving a restart, a permission-gated file agent, a generator-evaluator loop, and a capstone coding agent with ablation runs.

Once both worked, I pointed OpenCode at the same models (Qwen2.5-Instruct, 7B and 14B) expecting a mature framework to beat my homegrown one by a mile. Instead it failed on printing a cwd and writing a .txt file. The models couldn't produce output matching OpenCode's tool-calling schema, so the loop died before the model ever reasoned about the task. [X/10 vs Y/10 over N trials.]

Worth being precise about the cause, because "framework bad" isn't it. OpenCode ships a large system prompt and a wide tool surface. My harness has [N] tools and a short prompt. Small models degrade fast as the schema they have to satisfy grows, and they don't degrade gracefully — they emit malformed JSON and the loop breaks. I set num_ctx to [value] and confirmed the prompt wasn't being truncated, so this isn't just Ollama's default context window eating the tool definitions. [Cut this sentence if you didn't verify it.]

So: general frameworks assume a strong model behind them, and that assumption is load-bearing. If you want small local models actually acting as agents rather than chatting, scoping a harness to the tools the task needs beats reaching for something built for bigger models.

AI Dungeon Crawler: [link]
Agent harness ladder — the repo behind the OpenCode comparison: [link]


Okay. So in order to actually test this I need to change the parameter num_ctx to something higher in Ollama and then this post actually more valid.