# Curated References 📚

Acharya's hand-picked list — the *best* source per topic, in three flavors:
📄 official docs · 🎬 short video · 🎨 visual/interactive. Verify links if any have moved; the resource names are stable.

> We'll keep adding to this per phase. You never *have* to read these — they're for when you want to go deeper on your own.

## Foundations — how LLMs work
- 🎬 **3Blue1Brown — "But what is a neural network?" + Transformer series** (YouTube). The gold standard for *seeing* the math. Perfect for you.
- 🎨 **The Illustrated Transformer** — Jay Alammar (`jalammar.github.io/illustrated-transformer`). Visual, gentle, famous.
- 🎨 **Tokenizer playground** — paste text, watch it split into tokens (`tiktokenizer.vercel.app` or OpenAI's tokenizer). Makes "tokens" concrete.
- 🎬 **Andrej Karpathy — "Intro to Large Language Models" (1hr)** and his "Zero to Hero" series (YouTube). Save the "build GPT from scratch" one for Phase 8.

## The brain — Claude API (Phase 1)
- 📄 **Anthropic API docs** (`docs.anthropic.com`) — messages, streaming, system prompts, tokens.
- 📄 **Anthropic Console** (`console.anthropic.com`) — your keys, usage, and a Workbench to try prompts with no code.
- 📄 **Anthropic Python SDK** (`github.com/anthropics/anthropic-sdk-python`).

## Memory & RAG — embeddings (Phase 2)
- 🎨 **The Illustrated Word2Vec** — Jay Alammar. How words become vectors, visually.
- 📄 **sentence-transformers docs** (`sbert.net`) — the framework we'll likely use to make embeddings.

## Ears — Speech-to-Text (Phase 3)
- 📄 **OpenAI Whisper** (`github.com/openai/whisper`) — the open STT model.
- 📄 **faster-whisper** — the efficient version we'll run locally for cheap.

## Mouth — Text-to-Speech (Phase 4)
- 📄 **Piper TTS** (`github.com/rhasspy/piper`) — fast, open, free TTS for the product.

## Frameworks you'll learn along the way (you know basic Python)
- 📄 **FastAPI** (`fastapi.tiangolo.com`) — Python web backend (feels like Express, but Python). For serving AI.
- 📄 **Hugging Face course** (`huggingface.co/learn`) — free, hands-on intro to using open models.

## Deep dive — build it from scratch (Phase 8)
- 🎬 **Karpathy — "Let's build GPT from scratch, in code, spelled out"** (YouTube). We'll follow this to truly understand the brain.
