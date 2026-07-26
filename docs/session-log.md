# Session Log 📓

One short entry per session, newest on top. Acharya appends this at session end (or on "wrap up"). Keep entries under ~8 lines — this file is read at every session start, so brevity = cheap tokens.

---

## 2026-07-26 — Session 3 (evening): Phase 2 opened 🧮
- **Did:** Atom 2.0a–e (Python OOP via JS mapping: `class`/`__init__`/`self` → methods → imports + `__main__` guard → constructor args → refactored chatbot to `Memory`; student added `pop()` unprompted). 2.1 + 2.1c: felt the failure. 2.2 vectors + dot product, 2.2a norm, 2.2b normalizing.
- **Surprise:** the bot did **not** hallucinate about the student (Haiku 4.5 refuses on unknown private people, even to leading questions). Real failure = *confidently useless, deflects recruiters off-site*. Model's own words named the fix: "not in my context."
- **Decisions:** **P1.5 Recruiter Bot** added to `project-roadmap.md` — v1 after Phase 2, v2 after Phase 6 (email = agent+tools), v3 after Phase 10. New **`docs/math-map.md`**: 3 deep blocks (A vectors=now, B matrices pre-7.0, C calculus at 7.2–7.3); PCA/stats/regression deferred to P2.
- **⚠️ Pending / open next session with:** (1) **a REVISION — student explicitly asked** (softmax, temperature, vectors/normalizing/**unit vector**). (2) Then **Atom 2.3 embeddings**. (3) Phase 1 demo GIF still owed.
- **Vocabulary confusion to watch:** he had "unit vector" filed as something like a **bias vector**. Cleared: unit vector = direction only (÷ its own length); bias = a number added after a weighted sum inside a neuron (meets it properly at 7.0). Expect more half-remembered ML terms like this — surface and re-teach them from zero.
- **Student state:** pushed back hard — *"are you really going to teach me in-depth, or am I going to keep guessing?"* Root gap: never knew softmax's probabilities were **over the vocabulary** (logits per token); patched with a worked `mat/floor/roof` example. Also corrected: temperature divides **logits**, not probabilities. **He will call out hand-waving — always name black boxes up front and say which atom opens them** (told him: 2.3 uses a trained embedder as a black box, opened at 7.7/7.13).

---

## 2026-07-26 — Session 2 (morning): Phase 1 recall quiz ✅
- **Did:** 6-question Phase 1 quiz from memory — scored 5.5/6. Gaps patched: input cheap = parallel prefill (not cache), snowball cost of history replay, time-to-first-token.
- **Decisions:** Atom 2.0 re-split into smaller sub-atoms (2.0a, 2.0b…) because Python OOP is fuzzy — teach class/`__init__`/`self` via JS class mapping, tiny bites.
- **Pending:** Phase 2 NOT started — begin at **Atom 2.0a** (Python class skeleton, JS mapping already given in chat; student hasn't typed it yet). Demo GIF for Phase 1 chatbot still pending.
- **Student state:** sharp recall, but Phase 1 fatigue — asked to park and resume evening/night. Keep atoms extra small next session.

---

## 2026-07-26 — Session 1: Phase 1 complete, shipped 🚢
- **Did:** Atoms 1.0 → 1.9 all done. venv + OpenRouter key, first call, tokens/cost math, softmax by hand, temperature (Starbucks experiment!), system prompts, memory/statelessness, streaming, full chatbot, shipped to GitHub (commit credited after git identity fix).
- **Decisions:** OpenRouter instead of direct Anthropic ($5 credit, `openai` SDK + base_url). Classical ML/MLOps/vision/n8n = separate future projects (P2–P4, see `project-roadmap.md` — parking lot, discussion-gated). Ship-it atom every phase. Portfolio site cards deferred.
- **Pending:** ⚠️ Open next session with the 6-question Phase 1 recall quiz (no peeking at lesson 01). Demo GIF for chatbot. 
- **Student state:** flowing, fast learner, energized by "skills not everyone has" framing; tired of writing docs by day's end (Acharya wrote the README).
