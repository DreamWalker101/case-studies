# Agent Infrastructure Research
# Last updated: 2026-04-03

## Goal
Build a brain/body architecture: Claude = brain (reasoning, synthesis, decisions), local agents = body (browser, computer use, memory, task execution). Claude delegates heavy lifting to avoid burning tokens on mechanical work.

---

## Layer-by-Layer Comparison

### Layer 1: Orchestration Hub (the routing backbone)

| Tool | Stars | What it does | Verdict |
|------|-------|-------------|---------|
| **OpenClaw** | ~5k | WebSocket gateway at `ws://127.0.0.1:18789`. Routes across 24+ messaging channels (WhatsApp, Telegram, Slack, Discord, etc). Pi agent runtime, skills registry (ClawHub), voice, Live Canvas for visual control. Multi-agent routing. | ✅ **Best pick** — local, persistent, multi-platform |
| Hermes Agent | 22.6k | Self-improving executor. Writes its own skills from experience. 40+ tools, 6 terminal backends (local/Docker/SSH/Modal). Multi-platform comms built in. Near-zero idle cost. | Good alternative if OpenClaw is overkill |

**Recommendation: OpenClaw** as the body's central nervous system. It receives commands from Claude, routes to the right agent, and maintains state across sessions.

---

### Layer 2: Computer Use / Desktop Control

| Tool | Stars | What it does | Verdict |
|------|-------|-------------|---------|
| **CUA (trycua)** | ~8k | Screenshot-based computer use. Explicitly integrates with OpenClaw. Full desktop control — not just browser. Runs as a node. | ✅ **Best for desktop** — full OS control |
| browser-use | 85.7k | Browser-only agent. 89.1% WebVoyager benchmark (best open-source). Works with Claude. Python API. Much simpler setup than CUA. | ✅ **Best for web** — higher accuracy, lighter weight |

**Recommendation: Both.** Use `browser-use` for all web tasks (forms, scraping, research). Use `CUA` for full desktop control (clicking apps, file management, GUI automation). They complement each other — browser-use is faster and more accurate for web; CUA handles what browser-use can't reach.

---

### Layer 3: Memory / Context Persistence

| Tool | Stars | What it does | Verdict |
|------|-------|-------------|---------|
| **Mem0** | 51.8k | Persistent memory layer. 91% faster retrieval than full-context, 90% lower token usage. `pip install mem0ai`. Works with Claude and Ollama. Three-tier: user/session/agent memories. | ✅ **Best pick** — simple, fast, proven |
| OpenViking | 20.6k | Filesystem-paradigm context DB. L0/L1/L2 tiered loading, visualised retrieval paths, session compression, automatic long-term memory. Docker deploy. Works with Ollama + Claude. | 🟡 More powerful but heavier — overkill for solo use |
| Letta (MemGPT) | ~35k | OS-style memory (RAM/disk model). Stateful agent identity across sessions. Complex to self-host. | ❌ Too heavy for this setup |
| ChromaDB (existing) | — | Already running for claude-powers and ahmed-context. Good for semantic search on specific corpora. | ✅ Keep for pipeline KB — not replacing |

**Recommendation: Mem0** for cross-session agent memory (what Claude and Hermes remember between runs). Keep ChromaDB for the knowledge pipeline — they serve different purposes. OpenViking is worth watching but adds ops complexity you don't need right now.

---

### Layer 4: Task Executor (does the actual work)

| Tool | Stars | What it does | Verdict |
|------|-------|-------------|---------|
| **Hermes Agent** | 22.6k | Self-improving, writes skills from experience. 40+ tools. Parallel subagents. Cron scheduling. 6 execution backends. Anthropic support. $5/month to run idle. | ✅ **Best pick** — grows with your use case |
| CrewAI | ~25k | Role-based agent teams. Good for structured multi-agent pipelines. Less flexible than Hermes for ad-hoc tasks. | 🟡 Better for defined pipelines |
| AutoGen | ~35k | Microsoft's conversational multi-agent. Heavy, enterprise-grade. | ❌ Overkill |

**Recommendation: Hermes Agent** as the primary executor for complex tasks that need to run autonomously (multi-step research, code tasks, scheduled jobs). It learns from each run, so it gets better at your specific workflows over time.

---

### Layer 5: Claude Code Skills (already installed)

**GStack** — 33 skills from Garry Tan. Installed at `~/.claude/skills/`.

Key skills available now:
- `/browse` — Playwright-based web browsing inside Claude sessions
- `/qa` — quality assurance workflow
- `/review` — code review
- `/ship` — full deploy workflow
- `/investigate` — deep research mode
- `/checkpoint` — save/restore Claude session state
- `/learn` — structured learning workflow
- `/health` — project health check
- `/autoplan` — automated planning

---

## Recommended Stack (Phased Rollout)

### Phase 1 — The Body (this week)
```
Claude (brain)
    │
    ├── OpenClaw gateway (ws://127.0.0.1:18789)
    │       └── CUA node (desktop control)
    │
    └── browser-use (pip install browser-use)
            └── Called directly when Claude needs web actions
```
Install: `pip install browser-use` + clone/run OpenClaw + connect CUA as node

### Phase 2 — Memory (next week)
```
Mem0 (persistent memory layer)
    ├── Claude reads/writes memories per session
    ├── Hermes reads/writes memories per task run
    └── ChromaDB (existing) — pipeline knowledge base (unchanged)
```
Install: `pip install mem0ai` + configure with Ollama (local, zero cost)

### Phase 3 — Smart Executor (when needed)
```
Hermes Agent
    ├── Receives delegated tasks from Claude via OpenClaw
    ├── Has 40+ tools natively
    ├── Spawns subagents for parallel work
    └── Learns your patterns → writes new skills automatically
```

---

## Communication Flow (Target State)

```
Ahmed
  │  (text/voice)
  ▼
Claude (Cowork or CLI)     ← brain: reasoning, decisions, synthesis
  │
  ├── /browse (GStack)     ← quick in-session web lookups
  │
  ├── OpenClaw gateway     ← delegates mechanical tasks
  │     ├── CUA node       ← desktop/GUI automation
  │     ├── Hermes         ← complex multi-step autonomous tasks
  │     └── Bash/tools     ← simple operations
  │
  ├── browser-use          ← web automation (forms, scraping)
  │
  └── Mem0                 ← what Claude remembers between sessions
        └── ChromaDB       ← searchable knowledge base (pipeline output)
```

---

## What to Skip (for now)

- **OpenViking**: Powerful but adds a Docker service + Rust CLI + complex config for benefits you already get from Mem0 + ChromaDB combined. Revisit if you run a team of agents.
- **Letta/MemGPT**: Enterprise memory OS. Way too heavy for solo setup.
- **LangGraph / CrewAI / AutoGen**: Framework lock-in. Hermes covers the same ground with less boilerplate.
- **SafeGuard NemoClaw**: NVIDIA's LLM guardrail layer — relevant for production deployments with untrusted users, not for personal use.

---

## Install Commands (when ready)

```bash
# Phase 1
pip install browser-use --break-system-packages
playwright install chromium  # for browser-use

# OpenClaw (check openclaw/openclaw for latest install)
git clone https://github.com/openclaw/openclaw ~/projects/openclaw
# follow their setup

# Phase 2
pip install mem0ai --break-system-packages
# configure with Ollama: set OPENAI_API_KEY equivalent for local

# Phase 3
git clone https://github.com/NousResearch/hermes-agent ~/projects/hermes-agent
# configure with Anthropic API key
```
