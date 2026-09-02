# OpenCode on Windows: The Seamless WSL2 Setup

A step-by-step guide to running OpenCode on a personal Windows laptop with near-native Linux performance — no dual boot, no Linux laptop, no Apple Silicon required.

---

## Why this approach

OpenCode runs best on Linux. On Windows, the closest you can get to that experience — without new hardware — is **WSL2 (Windows Subsystem for Linux, version 2)**, which runs a real Linux kernel in a lightweight VM. This guide sets up WSL2 + Ubuntu as your one true dev environment, with Windows-native tools (Terminal, VS Code, the OpenCode Desktop app) layered on top for a normal-feeling GUI experience.

---

## Step 1: Install WSL2 + Ubuntu

Open PowerShell as Administrator and run:

```powershell
wsl --install
```

This single command installs WSL2, sets it as the default version, and installs Ubuntu (the default distro). Restart when prompted.

> On a personal laptop this "just works" — modern consumer hardware almost always has virtualization available. (This is the step that can silently fail on locked-down corporate machines, which don't apply here.)

Verify you're on WSL2 (not the older WSL1):

```powershell
wsl -l -v
```

You should see `VERSION 2` next to your Ubuntu install.

---

## Step 2: Install OpenCode *inside* WSL2

Open your Ubuntu shell (search "Ubuntu" in the Start menu, or type `wsl` in a terminal), then run the installer **from inside WSL**, not from PowerShell:

```bash
curl -fsSL https://opencode.ai/install | bash
```

Verify it worked:

```bash
opencode --version
```

---

## Step 3: Keep your project files inside the Linux filesystem

This is the single most important habit for a smooth setup.

- ✅ **Do this:** `~/code/your-project/`
- ❌ **Not this:** `/mnt/c/Users/you/your-project/`

Reasons this matters:
- **Speed** — crossing the Windows↔Linux filesystem boundary (`/mnt/c/...`) is the one place WSL2 is genuinely slow. Keeping files natively in Linux gives near-bare-metal I/O.
- **Git worktree correctness** — if a project lives on a Windows-mounted drive, `git worktree` paths get stored in WSL-style (`/mnt/d/...`) inside `.git`, which Windows-native Git clients and editors can't resolve. Keeping everything inside `~/code/` avoids this entirely.

```bash
mkdir -p ~/code
cd ~/code
git clone <your-repo-url>
```

---

## Step 4: Terminal — Windows Terminal

[Windows Terminal](https://apps.microsoft.com/detail/9n0dx20hk701) is the natural front-end. It has first-class WSL2 profile support and renders TUI apps (like OpenCode's interface) well.

- Open a new tab and select your **Ubuntu (WSL)** profile.
- Use multiple tabs or split panes if you want several OpenCode sessions running side by side.

> **Known quirk:** image paste (`Ctrl+V`) into OpenCode's TUI can behave inconsistently depending on Windows Terminal's paste handling. Plain text paste is reliable; pasting screenshots sometimes isn't. Not a dealbreaker — just don't be surprised if an image paste silently fails.

---

## Step 5 (optional): VS Code + WSL Remote

If you want a full GUI editor alongside the terminal agent:

1. Install the **WSL** extension in VS Code.
2. From inside your WSL shell, in your project folder:
   ```bash
   code .
   ```

VS Code's UI runs on Windows, but the file system, extensions, and integrated terminal all execute inside WSL2 — so it feels like a normal Windows app while working against the same Linux-native files OpenCode uses, with zero cross-filesystem penalty.

---

## Step 6 (optional): OpenCode Desktop (Windows) + WSL-hosted server

If you'd rather use a native Windows GUI instead of living in a terminal:

1. Start the OpenCode backend inside WSL2:
   ```bash
   opencode serve
   ```
2. Install **OpenCode Desktop** on Windows (from [opencode.ai/download](https://opencode.ai/download)).
3. In Desktop's settings, connect to your WSL server and **set it as the default server**.

This gives you a native GUI app while the actual work — file edits, tool calls, git operations — happens against the Linux filesystem underneath.

> Set the WSL server as *default*, not just connected. Leaving it ambiguous is a known source of session/connection issues when the WSL server isn't running yet at Desktop startup.

---

## Step 7: Running multiple agents/worktrees in parallel

If you're comparing multiple models (or just want isolated workspaces), keep every worktree inside the WSL filesystem:

```bash
cd ~/code
git worktree add ~/code/project-claude claude-branch
git worktree add ~/code/project-kimi kimi-branch
git worktree add ~/code/project-glm glm-branch
git worktree add ~/code/project-deepseek deepseek-branch
```

Then either:
- Open one **Windows Terminal tab per worktree**, or
- Use `tmux` or `zellij` inside a single WSL shell for split panes without leaving one terminal window.

---

## Step 8: Performance tuning for heavy parallel use

WSL2's default memory/CPU allocation can be conservative. If things feel sluggish running several agents at once, create a config file **on the Windows side**:

**File:** `%UserProfile%\.wslconfig`

```ini
[wsl2]
memory=12GB
processors=6
```

Adjust the numbers to your actual RAM/core count (leave enough headroom for Windows itself). Apply the change by restarting WSL from PowerShell:

```powershell
wsl --shutdown
```

Then reopen your Ubuntu shell.

---

## Quick checklist

- [ ] `wsl --install` run, `wsl -l -v` confirms **VERSION 2**
- [ ] OpenCode installed from *inside* the Ubuntu shell
- [ ] Project repos live under `~/code/`, never `/mnt/c/...`
- [ ] Windows Terminal set up with an Ubuntu (WSL) profile
- [ ] *(optional)* VS Code WSL extension installed, opened via `code .`
- [ ] *(optional)* `opencode serve` + Desktop connected and set as default
- [ ] `.wslconfig` tuned if running multiple agents in parallel
