# AHMED'S MASTER CONTEXT FILE
# Read this at the start of any new session.
# Last updated: 2026-04-03

---

## Who I Am
Ahmed — developer building an AI-augmented personal OS. Not just using AI tools, but assembling a layered agent infrastructure where Claude acts as the reasoning brain and a stack of local agents, tools, and models do the heavy lifting. The goal is compounding efficiency: each session improves the system, each agent learns from the last run, and the whole stack gets smarter over time with minimal token burn.

Email: contact@tavren.io
GitHub: DreamWalker101

---

## Philosophy & Approach

- **Brain/body separation**: Claude = reasoning, synthesis, decisions. Local agents = execution, browser, file ops, bulk tasks.
- **CLI-first, MCP-sparingly**: CLI tools have far lower token overhead than MCP tool calls. Prefer bash/python CLIs for agent wiring. Only use MCP when there's no clean CLI alternative.
- **Local-first**: prefer local models (llama3.1:8b, qwen2.5-coder:7b via Ollama) for tasks where quality is comparable. Save Claude for tasks that actually need reasoning.
- **Compound learning**: every agent run should leave the system smarter than before — via OpenSpace skill evolution, ChromaDB memory, or Mem0 cross-session persistence.
- **Specialist-over-generalist**: build a registry of agents that are best at specific task types. Test, log, keep the winners. GSD for planning, Agency-Agents templates for specialist roles, Hermes for autonomous long-running work.
- **Progressive rollout**: get each layer working and proven before stacking the next one on top.
- **No over-engineering**: the strongest infrastructure is one that's running and being used, not the most complete one on paper.

---

## Machine
- OS: Ubuntu 22 (GNOME), display :1
- GPU: RTX 3070 Ti (8GB VRAM, CUDA 12.2)
- RAM: 30GB
- Shell: bash, Python 3.12
- Key tools: yt-dlp, faster-whisper, Ollama, Claude Code CLI, gh CLI, git, bun
- Remote access: Tailscale (IP: 100.79.0.120) + x11vnc on port 5900 (password: claudevnc)

### Local Models (Ollama)
- `llama3.1:8b` — primary local reasoning model (4.9GB, fully GPU)
- `qwen2.5-coder:7b` — code tasks (4.7GB, fully GPU)
- `nomic-embed-text` — embeddings for ChromaDB
- Note: 8GB VRAM = max ~8B models run fully on GPU. Larger models (30B+) need CPU offload and run slow. Wait for Nemotron-Cascade-2-30B on Ollama but don't build around it yet.

---

## Agent Infrastructure (Target Stack)

### Status Key: ✅ Live | 🔧 To Install | 📋 Planned

```
Ahmed
  ↓
Claude (Cowork / CLI)                      ✅ Live — reasoning brain
  ├── GStack 33 skills                      ✅ Live — ~/.claude/skills/
  ├── GSD + GSD 2 agent                     ✅ Live — planning & task decomposition
  │
  └── delegates via CLI to:
        │
        OpenClaw (orchestrator)             🔧 To Install
          ├── Claw-Code + llama3.1:8b       🔧 To Install — bulk/cheap tasks, zero API cost
          ├── Claw-Code + qwen2.5-coder     🔧 To Install — code-specific tasks
          ├── Hermes Agent                  🔧 To Install — autonomous long-running tasks
          └── Agency-Agents templates       📋 Planned — specialist roles per task type
                    ↓
              OpenSpace (background)        🔧 To Install — observes executions, evolves skills
                    ↓
              Mem0 → ChromaDB              🔧 To Install — cross-session persistent memory
                    ↓
              browser-use / CUA            🔧 To Install — web + desktop automation
```

### Layer Details

**OpenClaw** — orchestration hub. Routes tasks to local models or Claw-Code agents. Also the messaging bridge: Claude can receive commands via WhatsApp (unofficial web.js/Baileys bridge, free, QR scan) or Discord (free API, no country restrictions — backup option since Telegram is banned). OpenClaw must be wired to invoke Claude CLI with CONTEXT.md so it "knows" who Ahmed is and what's been built.

**Claw-Code** (149k stars) — clean-room reimplementation of Claude Code harness. Runs on local models + Codex. Key for the efficiency goal: fire a Claw-Code agent with llama3.1:8b for mechanical tasks instead of burning Claude API tokens.

**Hermes Agent** (22.6k stars) — self-improving autonomous executor. 40+ tools, parallel subagents, cron scheduling, learns from experience. Best for complex multi-step tasks that need to run unsupervised.

**OpenSpace** (3.5k stars, updated daily) — skill evolution engine. Three modes: FIX (repairs broken skills), DERIVED (specialises), CAPTURED (extracts new patterns). 46% token reduction after first run of any task type. 4.2× income on GDPVal benchmark. Run as background service, wrap in CLI for calls.

**Agency-Agents** (68.9k stars) — 68+ specialist agent templates. Not infrastructure — personality/workflow layer. Grab the right template (UI agent, debugger agent, researcher) and drop it into Claw-Code or Hermes runtime. Build registry over time: best agent per task type.

**GSD 2 agent** — planning and task distribution. Decomposes high-level goals into discrete tasks, hands each to the right specialist agent.

**Mem0 → ChromaDB** — Mem0 sits on top of existing ChromaDB instance (`ahmed-context` collection). Handles "what's worth remembering" extraction. Any agent reads/writes through Mem0; ChromaDB persists it. Two collections: `ahmed-context` (project/session memory) + `claude-powers` (knowledge pipeline output).

**browser-use** (85.7k stars) — best-in-class web automation. 89.1% WebVoyager benchmark. Python CLI.

**CUA** — full desktop/GUI automation. Complements browser-use (browser-use = web, CUA = desktop apps).

### Agent Testing Registry
Keep a log here of what each agent does best. Update as we test.

| Agent | Best at | Verdict | Tested |
|-------|---------|---------|--------|
| GSD 2 | Planning, task decomposition | ✅ Strong | Yes |
| llama3.1:8b | Local reasoning, triage, classification | ✅ Good | Yes |
| qwen2.5-coder:7b | Code generation, code review | ✅ Strong | Yes |
| *(add as we test)* | | | |

---

## Projects Built

| Project | Context File | Status |
|---------|-------------|--------|
| Claude Knowledge Pipeline | [./claude-knowledge-pipeline/CONTEXT.md](./claude-knowledge-pipeline/CONTEXT.md) | ✅ Live |

### Research Done
| Topic | File | Summary |
|-------|------|---------|
| Agent Infrastructure | [./agent-infrastructure/RESEARCH.md](./agent-infrastructure/RESEARCH.md) | Full comparison: OpenClaw, CUA, browser-use, Mem0, OpenViking, Hermes, GStack, OpenSpace, Claw-Code, Agency-Agents |

---

## Key Paths
```
~/projects/                          # All project code
~/projects/claude-pipeline/          # Main knowledge pipeline
~/claude-powers/                     # Public AI knowledge base (git repo)
~/ahmed-ideas/                       # Private ideas vault (git repo, private)
~/case-studies/                      # This folder — project records + AI context
~/logs/                              # Pipeline and system logs
~/.claude/skills/                    # GStack 33 skills (installed)
~/.ssh/id_ed25519_claude_pipeline    # GitHub SSH key for pipeline repos
```

## GitHub
- Account: DreamWalker101
- Pipeline: github.com/DreamWalker101/claude-pipeline
- Knowledge base: github.com/DreamWalker101/claude-powers (public)
- Ideas: github.com/DreamWalker101/ahmed-ideas (private)
- Case studies: github.com/DreamWalker101/case-studies (public)
- gh CLI: authenticated system-wide

---

## Knowledge Pipeline (Live)

Captures content from Instagram, YouTube, TikTok via iOS Scriptable share sheet → Tavren Pad → Linux scraper → Whisper transcription → Ollama triage → Claude Code synthesis → GitHub push.

Three-bucket routing:
- `claude-powers` repo — technical AI knowledge (public)
- `ahmed-ideas` repo — personal ideas/notes (private)
- `updates/ai-tools` — general updates

Supports: video (reels), image posts, carousels. URL|note format: `https://... | my note` parsed into separate note field. Notes trigger `ideas` category routing.

---

## Active Services
- tailscaled (systemd)
- x11vnc (systemd, port 5900, display :1)
- Ollama (started on demand by pipeline)
- ChromaDB (ahmed-context collection, nomic-embed-text embeddings)

## iPhone Setup
- Tailscale installed — on same network as Linux (100.85.23.54)
- VNC Viewer app — connects to 100.79.0.120:5900
- Scriptable app — ClaudePipeline.js for sharing reels/posts to pipeline

---

## How to Wire Claude into Any Agent/CLI Context

Any agent (OpenClaw, Hermes, Claw-Code, etc.) that needs to invoke Claude with full context should:

```bash
claude --context ~/case-studies/CONTEXT.md "<task description>"
# or
cat ~/case-studies/CONTEXT.md | claude -p "<task description>"
```

This gives Claude the full picture: who Ahmed is, what's been built, the philosophy, the agent stack, all paths. OpenClaw's Claude invocations must always inject this file.

---

## Session Notes

### Founding Session — 2026-04-03 (Cowork)
First session where the full agent infrastructure was designed end-to-end. Key decisions made:
- Brain/body architecture decided: Claude reasons, local agents execute
- CLI-first wiring preference established (not MCP)
- Nemotron-Cascade-2 noted but deferred (8GB VRAM constraint)
- Full agent stack researched: OpenClaw + Claw-Code + Hermes + OpenSpace + Agency-Agents + browser-use + CUA + Mem0
- GStack installed: 33 skills in ~/.claude/skills/
- Agent testing registry concept established: test every agent, log what it's best at
- WhatsApp as primary command channel for OpenClaw (unofficial bridge, free)
- Discord as backup (Telegram banned in country)
