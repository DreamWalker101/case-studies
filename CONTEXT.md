# AHMED'S MASTER CONTEXT FILE
# Read this at the start of any new session.
# Last updated: 2026-04-02

## Who I Am
Ahmed — developer, building AI-augmented personal systems. Using Claude (Cowork + Claude Code CLI) as a persistent system-level assistant with full machine access.

## Machine
- OS: Ubuntu 22 (GNOME)
- GPU: RTX 3070 Ti (8GB VRAM, CUDA 12.2)
- Shell: bash, Python 3.12
- Key tools: yt-dlp, faster-whisper, Ollama (llama3.1:8b, nomic-embed-text), Claude Code CLI, gh CLI, git
- Remote access: Tailscale (IP: 100.79.0.120) + x11vnc on port 5900

## Projects Built
| Project | Context File | Status |
|---------|-------------|--------|
| Claude Knowledge Pipeline | [./claude-knowledge-pipeline/CONTEXT.md](./claude-knowledge-pipeline/CONTEXT.md) | ✅ Live |

## Key Paths
```
~/projects/                  # All project code
~/claude-powers/             # Public AI knowledge base (git repo)
~/ahmed-ideas/               # Private ideas vault (git repo)
~/case-studies/              # This folder — project records
~/logs/                      # Pipeline and system logs
~/.ssh/id_ed25519_claude_pipeline  # GitHub SSH key for pipeline repos
```

## GitHub
- Account: DreamWalker101
- Pipeline: github.com/DreamWalker101/claude-pipeline
- Knowledge base: github.com/DreamWalker101/claude-powers (public)
- Ideas: github.com/DreamWalker101/ahmed-ideas (private)
- gh CLI: authenticated system-wide

## Preferences & Patterns
- Full autonomous access — no need to ask permission for file/system operations
- Commits after every meaningful change with descriptive messages
- `.env` files are gitignored — never commit credentials
- Separate private repo for personal/speculative content vs public technical knowledge
- Local-first: prefer GPU/local models over API calls where quality is comparable
- Pipeline runs are triggered manually (desktop icon) — not on a cron yet

## Active Services
- tailscaled (systemd)
- x11vnc (systemd, port 5900, display :1)
- Ollama (started on demand by pipeline)

## iPhone Setup
- Tailscale installed — on same network as Linux (100.85.23.54)
- VNC Viewer app — connects to 100.79.0.120:5900, password: claudevnc
- Scriptable app — ClaudePipeline.js script for sharing reels/posts to pipeline
