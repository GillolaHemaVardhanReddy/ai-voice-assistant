# Progress Tracker ✅

Tick each atom as you finish (`[ ]` → `[x]`). Acharya resumes from here each session.

**New rules (26 Jul 2026):** every phase ends with a **ship-it atom** (README + demo GIF + write-up → portfolio card on hemavardhanreddy.vercel.app). Classical ML/MLOps/vision/n8n live in **future projects P2–P4** — see `docs/project-roadmap.md`.

**Currently at:** 🧩 **Phase 2, Atom 2.3 — embeddings** · ⚠️ but FIRST: student asked for a **revision** at next session start (softmax · temperature · vectors/normalizing)

## Phase 0 — Setup & foundations plan
- [x] Repo + git + Acharya (teacher) built
- [x] Build-while-learn syllabus, all 10 phases atomized
- [x] Foundations coverage map (`foundations-map.md`)
- [x] API key in `.env` — **decision: OpenRouter** ($5 credit) instead of direct Anthropic; we call Claude models through OpenRouter using the `openai` SDK with `base_url="https://openrouter.ai/api/v1"`. One key → many models, easy model switching later.
- [x] Python confirmed installed (3.12.8)

## Phase 1 — The BRAIN
- [x] 1.0 venv + SDKs (`anthropic`, `openai`, `python-dotenv`) + `.env` (OpenRouter key)
- [x] 1.1 First API call (`learn/phase1/first_call.py`)
- [x] 1.2 Tokens & usage (cost verified by hand: $0.000068/call)
- [x] 1.3 🔧 Softmax by hand (`learn/phase1/softmax.py`, incl. negative-score experiment)
- [x] 1.4 Temperature (`learn/phase1/temperature.py`, Starbucks vs invented-name experiment)
- [x] 1.5 System prompt (`learn/phase1/system_prompt.py`, pirate → product voice)
- [x] 1.6 Conversation memory (`learn/phase1/memory.py`, amnesia → history replay; snowball cost + caching understood)
- [x] 1.7 Streaming (`learn/phase1/streaming.py`, SSE chunks, delta + flush)
- [x] 1.8 Chat loop ← **working chatbot** ✅ (`learn/phase1/chatbot.py` — streaming, memory, error-recovery, product voice)
- [x] 1.9 🚢 Ship-it: READMEs written, pushed to GitHub. Recall quiz done ✅ (5.5/6). Pending: demo GIF · portfolio card deferred by choice

## Phase 2 — MEMORY & RAG
- [x] 2.0a Python class skeleton (`learn/phase2/memory_class.py` — `class` / `__init__` / `self`, mapped from JS)
- [x] 2.0b Methods on a class (`add()`, self auto-passed, per-instance state proved)
- [x] 2.0c Imports + `if __name__ == "__main__":` guard (`learn/phase2/try_import.py`)
- [x] 2.0d Constructor arguments + defaults (`Memory(system_prompt="...")`, seeds history)
- [x] 2.0e Refactor: `Memory` drives the chat loop (`learn/phase2/chat_bot_v2.py`) — student added `pop()` unprompted ✅ **ATOM 2.0 DONE**
- [x] 2.1 Felt the failure — bot knows nothing about the student. Surprise: it did NOT hallucinate (Haiku 4.5 refuses on unknown private people); real failure = **confidently useless + deflects recruiters off-site**. Model's own words named the fix: *"not in my context."*
- [x] 2.1c Leading-question probe (yrs of React / hardest project) — refused both. **Haiku 4.5 = strong honesty baseline, good default for P1.5.** Still build the guardrail (cheaper models later may fabricate).
- [x] 2.2 🔧 Vectors + dot product in NumPy (`learn/phase2/vectors.py`; `a·b=32`, `a·a=14` by hand ✅)
- [x] 2.2a 🔧 Magnitude / norm (`√(a·a)` = `np.linalg.norm` ≈ 3.742; saw dot-product's length bug)
- [x] 2.2b 🔧 Normalizing → unit vectors (student proved it himself: `[1,2,3]` and `[4,8,12]` → same unit vector)
- [ ] 2.3–2.9 ← **answers from your data**

## Phase 3 — The EARS
- [ ] 3.0–3.6 ← **speak → text**

## Phase 4 — The MOUTH
- [ ] 4.0–4.6 ← **text → voice**

## Phase 5 — The LOOP
- [ ] 5.0–5.6 ← **hands-free talking assistant**

## Phase 6 — TOOLS & AGENTS
- [ ] 6.0–6.8 ← **an assistant that acts**

## Phase 7 — UNDER THE HOOD ★
- [ ] 7.0–7.4 Run A: neural nets from scratch (backprop!)
- [ ] 7.5–7.6 Run B: PyTorch
- [ ] 7.7–7.14 Run C: transformers → **train a mini-LLM**

## Phase 8 — FINE-TUNING (Hugging Face)
- [ ] 8.0–8.8 ← **your own trained model**

## Phase 9 — The WEB PRODUCT
- [ ] 9.0–9.8 ← **browser voice assistant**

## Phase 10 — CHEAP & SELLABLE
- [ ] 10.0–10.9 ← **deployed, measured, sellable** 🏁
