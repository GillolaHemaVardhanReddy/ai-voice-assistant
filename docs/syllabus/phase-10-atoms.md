# Phase 10 — CHEAP & SELLABLE (ship it)  *(living draft)*

Goal: make it cost little per user, prove it's good, and deploy — the phase that turns a project into a business. Includes the last AI-engineer foundation: **evaluation & guardrails**. 🔧 = open-the-hood atom.

| Atom | Idea you'll learn | What you'll do | You'll end up with |
|------|-------------------|----------------|--------------------|
| **10.0 🔧** | Cost model per conversation | Sum STT + LLM + TTS $ per chat, in code | Your true unit cost |
| **10.1** | Swap paid → open where it saves | Local Whisper + Piper + open LLM (Ollama) | Big cost drop |
| **10.2** | Right-size the model | Cheaper tier (e.g. Haiku) where quality allows | Balanced cost/quality |
| **10.3** | Caching | Cache prompts/responses | Cheaper repeats |
| **10.4 🔧** | **Evals** — measuring if AI is *good* | Build a small eval set + score it | Quality you can prove |
| **10.5** | Catching regressions | Re-run evals after changes | A safety net |
| **10.6 🔧** | **Guardrails** — safety & failure handling | Add input/output guards | A trustworthy product |
| **10.7** | Deployment | Put it on a server, env/secrets done right | It's live |
| **10.8** | Scale & pricing | Cost at N users → price with margin | A viable business |
| **10.9** | Wrap it up | A deployed, measured, affordable assistant | **Something sellable** 🏁 |

> Far-phase draft: tactics depend on real costs measured in earlier phases.
