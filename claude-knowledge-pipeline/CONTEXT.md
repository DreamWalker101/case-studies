# CONTEXT: Claude Knowledge Pipeline
# Read this at the start of any session touching this project.

## What This Is
Automated pipeline: Instagram/YouTube URL → transcribe/OCR → triage → Claude synthesis → ChromaDB → GitHub. Triggered by desktop icon or manually. iPhone capture via Scriptable share sheet extension.

## Repo Locations
- Pipeline code: `/home/ahmed/projects/claude-pipeline/` → github.com/DreamWalker101/claude-pipeline
- Knowledge base: `/home/ahmed/claude-powers/` → github.com/DreamWalker101/claude-powers (public)
- Ideas vault: `/home/ahmed/ahmed-ideas/` → github.com/DreamWalker101/ahmed-ideas (private)
- iOS script: `/home/ahmed/Downloads/ClaudePipeline.js` (paste into Scriptable app)

## Config
All config in `/home/ahmed/projects/claude-pipeline/.env` (gitignored):
- Tavren Pad: https://tavren-pad.vercel.app, padID=reels
- Whisper: large-v3, cuda, float16 (RTX 3070 Ti)
- Ollama triage: llama3.1:8b, embeddings: nomic-embed-text
- ChromaDB: ~/.claude-pipeline/chroma_db, collection=claude-powers
- KB path: ~/claude-powers, IDEAS path: ~/ahmed-ideas

## Pipeline Flow
```
scraper.py → {url, note} JSON per line
  → yt-dlp audio.mp3 → transcribe.py (Whisper GPU)
  → OR: yt-dlp images / insta_fetch.py (instaloader fallback) → describe_image.py (tesseract OCR)
  → triage.py (Ollama llama3.1:8b) → {score, category, reason}
  → if score >= 3: claude -p synthesis (ideas_prompt / image_prompt / synthesis_prompt)
  → embed_and_index.py (ChromaDB)
  → git push (claude-powers or ahmed-ideas depending on category)
  → scraper.py --remove (clears processed URLs from pad)
```

## Categories
- `claude-agents`, `claude-skills`, `claude-superpowers`, `api-features`, `prompt-engineering` → claude-powers
- `ai-tools`, `updates` → claude-powers
- `ideas` → ahmed-ideas (triggered when user adds a note, or Ollama classifies as idea)

## Known Gotchas
- MUST use `env -u CLAUDECODE claude -p` — nested session error otherwise
- MUST call `ollama keep_alive:0` before Whisper — 8GB VRAM, llama3.1:8b=5GB, Whisper=1.5GB
- MUST use `--dangerously-skip-permissions --add-dir "$KB"` for Claude to write to KB
- Instagram requires `--cookies-from-browser firefox` for yt-dlp; some accounts need instaloader fallback
- Display is `:1` not `:0` — VNC service configured for `:1` with auth `/run/user/1000/gdm/Xauthority`
- Tailscale IP: Linux=100.79.0.120, iPhone=100.85.23.54

## SSH Keys
- GitHub pipeline key: `~/.ssh/id_ed25519_claude_pipeline`
- ahmed-ideas uses `GIT_SSH_COMMAND="ssh -i ~/.ssh/id_ed25519_claude_pipeline"`

## URL|Note Format
Pad entries can be `URL` or `URL | note text`. Notes feed into triage (influences category) and synthesis (hints at what Ahmed found interesting).

## Active Services
- `tailscaled` (systemd) — Tailscale VPN
- `x11vnc` (systemd, root) — VNC on port 5900, display :1
- `ollama` — started by pipeline if not running
