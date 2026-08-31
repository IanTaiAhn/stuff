# Multi-Model Coding Agent Comparison Plan

## Goal

Recreate the core functionality of a small, well-known app using four different
model/harness combinations in parallel, then grade each build against a fixed
checklist. The point isn't just to see which model "wins" — it's to practice
being the reviewer/architect: judging output against a standard instead of
reading code line by line.

**Models to compare:**
- Claude (via Claude Code)
- Kimi K3 (via OpenCode / OpenCode Go)
- GLM-5.2 (via OpenCode / OpenCode Go)
- DeepSeek V4 (via OpenCode / OpenCode Go)

---

## Step 1 — Define the reference app's behavior as a checklist

Pick a small, well-scoped app you already understand the behavior of — not the
whole platform, just its core feature loop. Write a checklist of **observable
behaviors**, not implementation details. This checklist is your grading rubric
later, so keep every item concrete and testable.

Example (kanban board clone):
- [ ] Create / rename / delete a board
- [ ] Drag a card between columns
- [ ] State persists on page reload
- [ ] Keyboard shortcut adds a new card

**Good candidate apps** (small, well-known, bounded scope):
- Pomodoro timer with session history
- URL shortener with click analytics
- Single-board kanban tool (Trello-style, no auth complexity)
- Read-it-later list with tags (Pocket-style)

**Note on recreating apps:** build the *functionality* from your own
understanding of how it behaves — don't hand an agent the real app's source
code, logos, or marketing copy to copy. This is both the safer approach and
the better exercise, since you're specifying behavior the way a PM would.

---

## Step 2 — Same spec, four separate runs

Give the identical checklist, verbatim, to all four model/harness combos.
Same prompt every time — any wording differences between runs contaminate the
comparison, since you won't know whether you're grading the model or your own
inconsistency.

---

## Step 3 — Run all four in parallel worktrees

Use Orca to spin up four isolated **git worktrees**, one per model, so they
build in parallel without touching each other's files. Let each one run to
completion or a fixed time box before looking at any of them.

### What is a git worktree?

Normally a git repo has one working directory checked out to one branch at a
time — switching branches means your files change under you. A **worktree**
lets you check out multiple branches from the *same* repository into
**separate folders at the same time**, all sharing the same underlying `.git`
history. So you can have `~/project-claude/`, `~/project-kimi/`,
`~/project-glm/`, and `~/project-deepseek/` on disk simultaneously, each on
its own branch, each independently buildable and runnable — without cloning
the repo four times or one agent's changes interfering with another's. This
is the mechanism Orca (and similar orchestrators like Conductor) use to let
multiple coding agents work on the same codebase in parallel without
colliding.

---

## Step 4 — Grade each build against the checklist blind

Go through your checklist against each running app *before* comparing them to
each other. Click every item, note pass/fail. Avoid looking at which model
produced which build until you've graded all four — this keeps you grading
against your own standard instead of against "best of the four so far."

---

## Step 5 — Compare notes across models

Reveal which build is which and compare:
- Which model nailed edge cases the others missed?
- Which one made a good architecture call you didn't specify?
- Which one needed the most follow-up prompting to get right?

This is where you actually build intuition for each model's "personality."

---

## Caveats to keep in mind

- **Harness confound:** Claude Code and OpenCode are different harnesses
  (different system prompts, tool permissions, checkpoint systems) wrapped
  around the models. A comparison isn't purely "which model is smarter" — it's
  "which model + harness combo performs better." Worth noting when you draw
  conclusions.
- **This is a private benchmark, not a formal eval** — small sample size, one
  app, your own judgment. Treat conclusions as directional, not definitive.
- **OpenCode Go usage caps** are dollar-denominated ($12/5hrs, $30/week,
  $60/month), and cheaper models (DeepSeek V4 Flash, MiMo) go much further per
  dollar than pricier ones (Kimi K3, GLM-5.2/5.3) — so budget your runs
  accordingly if you want to repeat this exercise across several apps.

---

## Reference: model quick-picks

| Model | Strength | Best for |
|---|---|---|
| Claude (Claude Code) | Frontier reasoning, deep agentic autonomy | Complex, multi-step architecture work |
| GLM-5.2 | Top-ranked open model overall, 1M context | General-purpose default comparison |
| DeepSeek V4 | Best price-performance, MIT license | Cost-efficiency, high-volume runs |
| Kimi K3 | Leads open models on frontend/UI coding | Frontend-heavy comparisons |
