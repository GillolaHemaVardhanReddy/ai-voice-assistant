# AI Voice Assistant 🎤🤖🔊

Building a full AI voice chat assistant from scratch, end to end — while learning how modern AI actually works (including the math), with the goal of shipping it as an affordable product.

**Architecture:** `mic → Speech-to-Text → LLM brain → Text-to-Speech → speaker`

## Status
**Phase 1 complete ✅ — the Brain.** A streaming terminal chatbot with conversation memory, personality, and error recovery — every line understood, from softmax to SSE. See [`learn/phase1/`](learn/phase1/) and the write-up in [`docs/lessons/01-the-brain.md`](docs/lessons/01-the-brain.md). Next: Phase 2 — Memory & RAG.

## Stack
- **Product:** React + Node/Express
- **AI learning / training / math:** Python
- **Brain:** Claude (Haiku 4.5) via OpenRouter · **Ears:** Whisper (STT) · **Mouth:** TTS

## Getting started
1. Copy `.env.example` to `.env` and fill in your API key.
2. Follow the lessons in `docs/lessons/` in order.

Built with Claude Code as an in-project AI teacher (see `.claude/CLAUDE.md`).
