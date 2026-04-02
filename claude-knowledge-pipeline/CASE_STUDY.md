# Claude Knowledge Pipeline

**Built:** April 2026
**Time to build:** ~2 sessions
**Status:** Live and running

---

## The Problem

Every day I scroll through Instagram reels, YouTube Shorts, and carousel posts about Claude AI and emerging dev tools. Some of it is genuinely useful — specific techniques, new API features, tool discoveries. Most of it disappears from memory within hours.

The manual workflow was: watch a reel → maybe mentally note something → forget it. No retention, no searchability, no way to connect ideas across content.

**I needed a system that turns passive scrolling into a searchable knowledge base — with zero friction.**

---

## What I Built

A fully automated local pipeline that:
1. Accepts a URL (shared from iPhone with one tap)
2. Downloads the media — video, reel, or carousel post
3. Transcribes audio (GPU-accelerated) or runs OCR on images
4. Triages the content with a local LLM to score relevance and assign category
5. Synthesises structured insights using Claude — with fact-checking
6. Indexes everything into a local vector database for semantic search
7. Pushes to GitHub and clears the queue

The whole thing runs on my local machine. No cloud costs, no subscriptions, GPU-accelerated, fully private.

---

## Architecture

```
iPhone Share Sheet (Scriptable)
        │
        ▼
Tavren Pad (self-hosted notepad API)   ← URL | optional note
        │
        ▼
run_pipeline.sh  ← triggered by desktop icon click
        │
        ├── yt-dlp  → audio (.mp3)
        │       └── faster-whisper large-v3 (RTX 3070 Ti, ~11s/reel)
        │
        ├── yt-dlp / instaloader  → images (.jpg)
        │       └── tesseract OCR + instaloader caption
        │
        ├── Ollama llama3.1:8b  → triage score + category
        │       (VRAM managed: unloaded before Whisper, reloaded after)
        │
        ├── Claude Code CLI (-p)  → structured markdown insight files
        │       (--dangerously-skip-permissions, --add-dir KB)
        │
        ├── nomic-embed-text (Ollama)  → ChromaDB vector index
        │
        └── git push  → GitHub (claude-powers / ahmed-ideas)
```

---

## Knowledge Base Structure

Two separate private/public repos:

**`claude-powers`** (public) — Technical AI knowledge
- `claude-agents/` — multi-agent patterns
- `claude-skills/` — skill building, SKILL.md format
- `claude-superpowers/` — extended thinking, hooks, computer use
- `api-features/` — Claude API patterns
- `prompt-engineering/` — prompting techniques
- `ai-tools/` — MCP servers, RAG, dev tooling
- `updates/` — general AI news

**`ahmed-ideas`** (private) — Personal project seeds
- `ideas/` — concepts sparked by content, with raw note preserved + next steps

---

## Key Technical Decisions

**Why local LLM for triage, not Claude?**
Triage runs on every item and needs to be fast and cheap. llama3.1:8b via Ollama scores content 0-10 and assigns category in ~3 seconds. Claude is reserved for the expensive synthesis step where quality matters.

**Why unload Ollama before Whisper?**
RTX 3070 Ti has 8GB VRAM. llama3.1:8b occupies ~5GB. faster-whisper large-v3 needs ~1.5GB but fails with 2.5GB available due to overhead. Solution: call `keep_alive: 0` on Ollama before transcription, freeing 5GB. Reload happens naturally on next triage call.

**Why instaloader as a fallback?**
Some Instagram accounts block yt-dlp's download path entirely (returns 0 items even with authenticated cookies). instaloader uses Instagram's internal API and handles these restricted accounts. yt-dlp runs first; instaloader only activates if yt-dlp returns nothing.

**Why `env -u CLAUDECODE` before `claude -p`?**
Running claude CLI inside the Cowork/Claude Code session sets a `CLAUDECODE` env var. Calling `claude -p` as a subprocess detects this and refuses to run ("cannot launch inside another Claude session"). Unsetting it before the call bypasses the check.

**Why Tavren Pad as the queue?**
Simple text API, self-hosted on Vercel, accessible from iPhone and Linux. No auth complexity, no database, no polling daemon. The pipeline reads it, processes everything, removes processed entries. It's a queue that happens to be a notepad.

---

## Challenges and Fixes

| Problem | Root Cause | Fix |
|---------|-----------|-----|
| `CLAUDECODE` nested session error | Claude CLI blocks subprocess calls from within Claude sessions | `env -u CLAUDECODE claude -p ...` |
| VRAM OOM on second run | Ollama keeps model loaded between calls (5GB held) | `keep_alive: 0` API call before Whisper |
| Claude can't write to `~/claude-powers/` | Claude Code sandboxes writes to current dir | `--dangerously-skip-permissions --add-dir "$KB"` |
| Invalid triage category strings | Ollama returned freeform strings like "Cloud Code/AutoDream" | Keyword-based category snapping in `triage.py` |
| Carousel post downloads 0 items | Instagram account had download restrictions | instaloader fallback using Instagram's internal API |
| iOS `.shortcut` file blocked | Apple blocks unsigned shortcut files from non-Apple devices | Switched to Scriptable JS script — no signing required |

---

## Stack

| Component | Tool | Why |
|-----------|------|-----|
| Media download | yt-dlp + instaloader | Handles video, audio, images, carousels |
| Audio transcription | faster-whisper large-v3 | GPU-accelerated, ~11s per reel, runs local |
| Image OCR | tesseract + pytesseract | Fast, free, good on styled text posts |
| LLM triage | Ollama llama3.1:8b | Local, fast, cheap for scoring |
| LLM synthesis | Claude Code CLI (`claude -p`) | Best quality for structured insight writing |
| Vector DB | ChromaDB (persistent) | Local, zero-config, good Python API |
| Embeddings | nomic-embed-text (Ollama) | Local embeddings, no API cost |
| Queue | Tavren Pad (self-hosted) | Simple text API, iPhone-accessible |
| iOS capture | Scriptable JS script | No signing required, works in share sheet |
| Remote access | Tailscale + x11vnc | Secure remote desktop from iPhone |
| Version control | GitHub (2 repos) | claude-powers (public), ahmed-ideas (private) |

---

## Results

- **Full pipeline runtime:** ~45 seconds per video reel (download + transcribe + triage + synthesise + index + push)
- **Image post runtime:** ~15 seconds (download + OCR + triage + synthesise + index + push)
- **Zero cloud cost** beyond existing Claude subscription
- **3 content types handled:** video reels, single image posts, carousel posts (up to N slides)
- **3-bucket routing:** Claude knowledge → `claude-powers`, general AI → `claude-powers/updates`, personal ideas → `ahmed-ideas`
- **One-tap capture** from iPhone share sheet with optional inline note

---

## What I'd Do Differently

- Set up a proper queue with retry logic instead of a notepad — currently a failed item just stays in the pad
- Add a daily scheduled run so the pipeline fires automatically at a set time rather than requiring a desktop icon click
- Explore fine-tuning a smaller triage model on my specific category taxonomy to reduce hallucinated category names

---

## Files

```
~/projects/claude-pipeline/
├── run_pipeline.sh          # Main orchestrator
├── scraper.py               # Reads/parses Tavren Pad entries
├── transcribe.py            # faster-whisper wrapper
├── describe_image.py        # OCR for image posts
├── insta_fetch.py           # instaloader fallback for carousels
├── triage.py                # Ollama relevance scoring
├── embed_and_index.py       # ChromaDB indexing
├── retrieve.py              # Semantic search
├── reindex.py               # Full reindex
├── prompts/
│   ├── synthesis_prompt.txt # Video synthesis template
│   ├── image_prompt.txt     # Image post synthesis template
│   └── ideas_prompt.txt     # Personal ideas capture template
└── .env                     # Config (gitignored)

~/claude-powers/             # Public knowledge base repo
~/ahmed-ideas/               # Private ideas vault repo
~/Downloads/ClaudePipeline.js  # Scriptable iOS share script
```
