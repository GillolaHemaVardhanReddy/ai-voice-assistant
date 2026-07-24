# AI Voice Assistant 🎤🤖🔊

Building a full AI voice chat assistant from scratch, end to end — while learning how modern AI actually works (including the math), with the goal of shipping it as an affordable product.

**Architecture:** `mic → Speech-to-Text → LLM brain → Text-to-Speech → speaker`

## Status
Phase 0 — setup & foundations. See [`docs/00-roadmap.md`](docs/00-roadmap.md) for the full journey.

## Stack
- **Product:** React + Node/Express
- **AI learning / training / math:** Python
- **Brain:** Claude API · **Ears:** Whisper (STT) · **Mouth:** TTS

## Getting started
1. Copy `.env.example` to `.env` and fill in your API key.
2. Follow the lessons in `docs/lessons/` in order.

Built with Claude Code as an in-project AI teacher (see `.claude/CLAUDE.md`).
