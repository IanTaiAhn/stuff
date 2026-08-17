# Understanding MCP (Model Context Protocol)

Notes from a walkthrough covering the M×N problem, what MCP actually is, how to
architect a production setup, and a real example from LangChain's Open SWE
codebase.

---

## 1. The problem MCP solves

Before a shared protocol exists, connecting an AI application to an external
tool (Slack, GitHub, a database, an internal API) requires a **bespoke,
hand-built bridge** — custom auth handling, custom translation between the
tool's API and the model, maintained by whoever built it.

If you have **M** AI applications and **N** tools, and every pairing needs its
own bridge, you need **M × N** bridges. That number grows *quadratically*, and
none of the work is reusable — the Slack↔Claude bridge doesn't help the
Slack↔ChatGPT bridge get built, and both drift out of sync as Slack's API
changes.

| M (AI apps) | N (tools) | Bespoke integrations (M×N) |
|---|---|---|
| 2 | 3 | 6 |
| 3 | 4 | 12 |
| 10 | 50 | 500 |

A shared protocol turns this into **M + N**: each AI app implements the
protocol *once* (an MCP client), each tool implements the protocol *once* (an
MCP server), and any client can now talk to any server without either side
knowing anything specific about the other.

| M (AI apps) | N (tools) | With a shared protocol (M+N) |
|---|---|---|
| 2 | 3 | 5 |
| 3 | 4 | 7 |
| 10 | 50 | 60 |

**Why this is more than "less code":** it's about *whose* work is reusable.
Without MCP, a tool builder (say, Notion) has to build a separate integration
for every AI app that wants to use it. With MCP, Notion builds **one** server,
and it becomes usable by every MCP-compatible AI app that exists — including
ones that don't exist yet. It's the same shape of win as HTTP: one webpage
serves every browser instead of a browser-specific version of every site.

---

## 2. The key mental model: MCP is a rulebook, not infrastructure

This is the part that's easy to get backwards. **There is no server called
"MCP" that traffic passes through.** MCP doesn't run anywhere by itself.

What actually exists are two independent pieces of software that both agreed
to speak the same format:

- **MCP client** — code inside the AI application. Knows how to ask "what
  tools do you have?" and "run this tool" in a standard format.
- **MCP server** — code next to a tool. Knows how to answer those same two
  questions in that standard format.

When they connect, it's a **direct** connection (an HTTP request, or a local
subprocess pipe) straight from the client to the server. Nothing sits between
them. The reason it "just works" isn't a shared middleman — it's that both
ends independently chose the same rules.

```
   AI application                         Tool
  ┌────────────────┐                 ┌────────────────┐
  │   MCP client    │ ── direct ──►  │   MCP server    │
  │ (built into the │   connection   │ (wraps whatever │
  │  app/framework) │ ◄── direct ──  │  the tool does) │
  └────────────────┘                 └────────────────┘
```

Closest everyday analogy: **HTTP**. There's no company or server called
"HTTP" that the internet routes through — your browser and a website's server
both just implement the HTTP spec, so they can talk directly. "The web" is
millions of direct connections that all happen to use the same rules, not a
hub.

---

## 3. What the protocol actually standardizes

A small, fixed set of concepts, discovered dynamically at connection time
rather than hardcoded:

- **Tools** — functions the model can call (name, description, typed args).
- **Resources** — data the app can read (files, records, search results).
- **Prompts** — reusable prompt templates a server can expose.
- A standard handshake for **auth** and **capability discovery**.

A simplified example of what crosses the wire between a client and a server:

**Discovery** — the client asks what's available (it isn't told in advance):
```
Client → Server:  tools/list
Server → Client:  [
                     { name: "post_message", params: { channel, text } },
                     { name: "search_messages", params: { query } },
                     { name: "list_channels", params: {} }
                   ]
```

**Invocation** — the client calls a tool by name with arguments:
```
Client → Server:  tools/call  { name: "post_message",
                                args: { channel: "#eng", text: "Deploy done" } }
Server → Client:  { status: "ok", message_id: "1729..." }
```

**What's fixed vs. what varies:** the *format* of these messages never
changes, no matter which client or server is involved. What varies is purely
the *content* — which tools a given server happens to expose, because that's
dictated by what the underlying service actually does. Point the same client
at a different server (GitHub instead of Slack) and `tools/list` just returns
a different list — `create_issue`, `search_code` — and the client handles it
identically, because "ask what's available, then call something by name" is
the entire client-side logic.

---

## 4. Standing up your own production MCP setup

If you're building, say, 2–3 internal AI services and 4–5 custom internal
tools:

- **You're mostly writing MCP servers, not clients.** Whatever framework your
  AI services are built on (LangGraph, an agent SDK, etc.) typically ships a
  generic MCP client already — you *configure* it to point at servers, you
  don't build one per service.
- **"One server per tool" really means "one server per capability domain,"
  not per function.** Group tools the way you'd draw a microservice boundary:
  things sharing data/auth/deployment lifecycle live in one server (e.g. a
  CRM server exposing `get_customer`, `update_customer`, `list_orders`
  together); genuinely separate backend systems get separate servers.
- **The server is usually a thin wrapper**, not new logic — you likely
  already have the tool's real implementation; the server just exposes it via
  `tools/list` / `tools/call` instead of its current ad-hoc interface.
- **Transport matters in production.** Local stdio (client spawns the server
  as a subprocess) doesn't work when multiple services need to reach the same
  server concurrently — use the HTTP transport and run the server as a normal
  long-lived backend behind standard auth (API keys, mTLS, OAuth).
- **Keep credentials server-side and allow-list what you expose**, even from
  servers you trust — discovery being dynamic doesn't mean the AI app should
  get everything a server offers by default.
- **Honest caveat:** if you will only ever have exactly one AI service,
  forever, MCP is an abstraction layer you're paying for without collecting
  the multiplication benefit. The payoff comes from M and N both being > 1
  and growing over time.

---

## 5. A real production example (Open SWE + Corridor)

From `langchain-ai/open-swe`, the entire integration with a third-party tool
called Corridor is one file,
[`agent/integrations/corridor_mcp.py`](https://github.com/langchain-ai/open-swe/blob/main/agent/integrations/corridor_mcp.py):

```python
from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient({
    "corridor": {
        "transport": "http",
        "url": config.url,                          # https://app.corridor.dev/api/mcp
        "headers": {"Authorization": f"Bearer {config.token}"},
        "timeout": timedelta(seconds=30),
    }
})
tools = await client.get_tools()
```

What this demonstrates, line by line:

- **`MultiServerMCPClient` is an import, not custom code.** Open SWE didn't
  build an MCP client — they imported a generic, reusable one.
- **The entire "integration" is a URL and an auth header.** No Corridor-
  specific parsing or request-building code exists anywhere.
- **`client.get_tools()` is the discovery step.** Open SWE has zero hardcoded
  knowledge of what Corridor offers — it asks, at runtime.
- **Open SWE explicitly allow-lists which discovered tools it actually
  uses** (`_ALLOWED_TOOL_NAMES = frozenset({"analyzePlan"})`) — a real
  security practice: discover everything, wire up only what's reviewed.
- **The resulting tools merge in with zero special-casing** — from the
  agent's point of view, a tool sourced from Corridor's remote MCP server
  looks identical to a tool defined locally in Python.

Open SWE's team has never seen Corridor's server code and doesn't need to —
that's the actual point of the protocol boundary.

---

## 6. Quick reference

| Term | What it means |
|---|---|
| **MCP** | A specification/contract for how an AI app and a tool exchange capability info and calls. Not a running service. |
| **MCP client** | Code inside an AI app that speaks MCP to discover and call tools. Usually provided by your framework, not hand-built. |
| **MCP server** | Code next to a tool that speaks MCP to expose that tool's capabilities. This is usually what *you* build. |
| **Tool** | A callable function a server exposes (name, description, typed args). |
| **Resource** | Data a server exposes for the client to read. |
| **Discovery** (`tools/list`) | The client asking a server what it can do, at runtime rather than hardcoded. |
| **Invocation** (`tools/call`) | The client actually calling a named tool with arguments. |
| **M×N problem** | Without a shared protocol, every AI-app/tool pairing needs its own bespoke integration — growth is quadratic. |
| **M+N** | With a shared protocol, each side integrates once — growth is linear. |

---

## 7. The one-sentence version

MCP is a shared rulebook, not a hub — an AI app implements it once (as a
client), a tool implements it once (as a server), and any client can then
talk directly to any server, which is what turns "custom integration for
every pairing" into "one integration per side."
