"""
minimal_react_agent.py

A stripped-down illustration of the four things that make a "harness" a
harness (per the constitutive definition floating around in 2026 harness-
engineering writeups):

    1. Agent loop        -> run_agent()
    2. Tool interface     -> TOOLS + TOOL_IMPL
    3. Context management -> ContextManager
    4. Control mechanisms -> approval_required() / verify()

This is NOT production code. There's no sandboxing, no fuzzy-match diffing,
no MCP, no retry/reflection logic. It's meant to show the *shape* of the
thing in ~150 lines, not to replace Aider/OpenCode/Claude Code. Every real
harness takes each of these four sections and makes it dramatically more
robust.
"""

import subprocess
from pathlib import Path


# ---------------------------------------------------------------------------
# 0. THE "BRAIN" — swap this for a real model call (Anthropic, OpenAI, a
#    local vLLM/Ollama endpoint, whatever). This stub just defines the
#    contract: given conversation history + available tools, return either
#    a tool call or a final answer.
# ---------------------------------------------------------------------------
def call_model(messages: list[dict], tools: list[dict]) -> dict:
    """
    Replace with something like:

        response = anthropic_client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1024,
            messages=messages,
            tools=tools,
        )
        # ... parse response into {"tool_call": {...}} or {"done": True, "text": ...}
        return parsed

    Expected return shape:
        {"tool_call": {"name": "read_file", "args": {"path": "foo.py"}}}
        or
        {"done": True, "text": "Final answer / summary for the user"}
    """
    raise NotImplementedError("Wire this up to your model provider of choice")


# ---------------------------------------------------------------------------
# 1. TOOL INTERFACE — the hands. Small, explicit, individually sandboxable.
#    Real harnesses expose these via function-calling schemas or MCP; here
#    it's just a plain registry so the shape is obvious.
# ---------------------------------------------------------------------------
TOOLS = [
    {"name": "read_file", "description": "Read a file's contents",
     "parameters": {"path": "str"}},
    {"name": "search_replace", "description": "Replace exact text in a file",
     "parameters": {"path": "str", "search": "str", "replace": "str"}},
    {"name": "run_shell", "description": "Run a shell command (e.g. tests)",
     "parameters": {"command": "str"}},
    {"name": "list_dir", "description": "List files in a directory",
     "parameters": {"path": "str"}},
]


def read_file(path: str) -> str:
    return Path(path).read_text()


def search_replace(path: str, search: str, replace: str) -> str:
    text = Path(path).read_text()
    if search not in text:
        # A real harness falls back here: fuzzy line matching, whitespace-
        # normalized matching, "reflect the error back to the model and let
        # it retry" (this is exactly what Aider does — see find_original_
        # update_blocks() + its cascade of matching strategies).
        return f"ERROR: search text not found verbatim in {path}"
    Path(path).write_text(text.replace(search, replace, 1))
    return f"OK: edited {path}"


def run_shell(command: str) -> str:
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, timeout=60
    )
    return f"exit={result.returncode}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"


def list_dir(path: str) -> str:
    return "\n".join(p.name for p in Path(path).iterdir())


TOOL_IMPL = {
    "read_file": read_file,
    "search_replace": search_replace,
    "run_shell": run_shell,
    "list_dir": list_dir,
}


# ---------------------------------------------------------------------------
# 2. CONTROL MECHANISMS — permissions + verification. This is the layer
#    that decides "should this action even happen" and "did it actually
#    work" — the difference between a toy and something you'd trust.
# ---------------------------------------------------------------------------
DESTRUCTIVE_TOOLS = {"search_replace", "run_shell"}


def approval_required(tool_name: str, auto_approve: bool) -> bool:
    """Permissive (fast, risky) vs restrictive (slow, safe) mode."""
    return tool_name in DESTRUCTIVE_TOOLS and not auto_approve


def ask_human(tool_name: str, args: dict) -> bool:
    resp = input(f"\nApprove {tool_name}({args})? [y/N] ")
    return resp.strip().lower() == "y"


def verify(test_command: str | None) -> bool:
    """
    Computational verification (run the tests) beats LLM-as-judge whenever
    you can get it — it's the deterministic ground truth the agent can
    actually trust and iterate against.
    """
    if not test_command:
        return True
    result = run_shell(test_command)
    return result.splitlines()[0] == "exit=0"


# ---------------------------------------------------------------------------
# 3. CONTEXT MANAGEMENT — keep the conversation from exploding. Production
#    harnesses do summarization, observation-masking, sub-agent delegation,
#    repo-maps, etc. This is the crudest possible version of that idea:
#    once history gets long, collapse the old stuff into one summary line.
# ---------------------------------------------------------------------------
class ContextManager:
    def __init__(self, max_messages: int = 20, keep_recent: int = 6):
        self.messages: list[dict] = []
        self.max_messages = max_messages
        self.keep_recent = keep_recent

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.max_messages:
            self._compact()

    def _compact(self):
        old, recent = self.messages[:-self.keep_recent], self.messages[-self.keep_recent:]
        summary = "SUMMARY of earlier steps: " + " | ".join(
            m["content"][:80] for m in old if m["role"] == "assistant"
        )
        self.messages = [{"role": "system", "content": summary}] + recent

    def get(self) -> list[dict]:
        return self.messages


# ---------------------------------------------------------------------------
# 4. AGENT LOOP — reason, act, observe, repeat. Everything above exists to
#    be called from inside this loop.
# ---------------------------------------------------------------------------
def run_agent(
    task: str,
    max_steps: int = 15,
    auto_approve: bool = False,
    test_command: str | None = None,
):
    ctx = ContextManager()
    ctx.add("user", task)

    for step in range(max_steps):
        # --- REASON ---
        response = call_model(ctx.get(), TOOLS)

        if response.get("done"):
            print(f"\n✅ Agent finished: {response['text']}")
            return response["text"]

        tool_name = response["tool_call"]["name"]
        args = response["tool_call"]["args"]

        # --- CONTROL: permission gate ---
        if approval_required(tool_name, auto_approve):
            if not ask_human(tool_name, args):
                ctx.add("user", f"Action {tool_name} denied by user.")
                continue

        # --- ACT ---
        observation = TOOL_IMPL[tool_name](**args)

        # --- CONTROL: verify after any edit ---
        if tool_name == "search_replace":
            ok = verify(test_command)
            observation += f"\n[verification {'passed' if ok else 'FAILED'}]"

        # --- OBSERVE ---
        ctx.add("assistant", f"Called {tool_name}({args})")
        ctx.add("tool", observation)

    print("⚠️  Hit max_steps without the model signaling completion.")
    return None


if __name__ == "__main__":
    run_agent(
        task="Fix the bug in calculator.py where subtract() adds instead of subtracting.",
        test_command="python -m pytest tests/",
    )
