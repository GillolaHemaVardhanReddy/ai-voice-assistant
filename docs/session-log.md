# Session Log 📓

One short entry per session, newest on top. Acharya appends this at session end (or on "wrap up"). Keep entries under ~8 lines — this file is read at every session start, so brevity = cheap tokens.

---

## 2026-07-27 — Session 5: cosine landed, math teaching contract rewritten 🧮
- **Env:** new laptop — rebuilt from scratch. Python 3.10.12 system-wide, fresh `venv`, all packages reinstalled (numpy 2.2.6 / openai 2.48.0 / anthropic 0.120.0 / dotenv 1.2.2 / sentence-transformers 5.6.1 / torch 2.13.0). ⚠️ `.env` is gitignored — he must recreate it (OpenRouter key) on **every** new machine.
- **Did:** re-taught 2.4 geometrically → **2.4 ✅** (`cosine.py`), **2.5 ✅** (`similarity.py`: `cat/kitten 0.788` vs `cat/car 0.463` — meaning beats spelling), **2.6a mostly** (cone/anisotropy proven with 5 unrelated words, floor `0.186`, nothing near 0).
- **Rule earned:** absolute cosine lies, ranking tells the truth → **top-k, never a threshold.** Re-flag at 2.7; *measure* centering's value at 10.4 rather than arguing it.
- **⚠️ RESUME HERE:** the centering block in `similarity.py` (`vecs.mean(axis=0)` → `centered = vecs - mean_vec` → reprint 10 pairs). He predicted the new floor = **−1** (correct). Run it, compare, then → **2.6 vector store**.
- **BIG teaching change (his order):** *"don't throw LA resources at me — mine them and integrate into learn-by-doing; any math term becomes a clean sub-atom."* → new standing rule in `.claude/CLAUDE.md` (4 beats: 🖼️picture → 🔢numbers → ✏️formula → 💻code, then **back to text**), `math-map.md` rewritten with a take/skip table, 4 new 🧮 sub-atoms added (2.5a span/basis, 2.5b projection, 2.6a high-D, 2.7a search-as-matmul).
- **Two failures of mine, both logged:** (1) algebra proof before the picture; (2) a full triangle derivation never connected back to text — his words: *"no dots connected between geometry and our text."* Fix that landed: dot product = **AND-gate agreement score** = a JS `for` loop of `a[i]*b[i]`.
- **Student state:** frustrated mid-session, then flowing hard — asking foundation questions unprompted (*"why dot product?"*), correcting me, predicting well. Motivated by the countdown: **2 atoms to a vector store, 4 to working RAG.** Still owed: Phase 1 demo GIF.

## 2026-07-26 — Session 4 (night): first real embeddings 🧬
- **Did:** Atom 2.3a install `sentence-transformers` 5.6.1 → 2.3b `all-MiniLM-L6-v2`, `vec.shape == (384,)` for any text length → 2.3c `np.linalg.norm(vec) == 1.0` (model has a `Normalize` module ⇒ ships Atom 2.2b baked in). **Atom 2.3 DONE.**
- **Skipped:** the revision he'd asked for ("not even been 3hrs, let's start next") — softmax/temperature never re-checked, still un-quizzed.
- **Decision:** student chose **no naive text→vector detour** — building an embedder by hand is **deferred to Phase 7** (7.7/7.13). Do not re-offer it in Phase 2.
- **⚠️ STOPPED MID-EXPLANATION — resume here:** he understood *unit vector* and correctly guessed cosine collapses to `a·b`, then **got lost in my algebra proof** of it (`a·b/(|a||b|)` → `/1×1`, plus the "you choose *when* to divide" point). **Re-teach geometrically first:** draw arrows, angle → number, 1/0/−1 by picture; formula only after. Then start 2.4 (`learn/phase2/cosine.py`, predict-then-run on `[1,0]`/`[0,1]`/`[2,0]`).
- **Teaching note:** the loss came from a **dense multi-part block** (proof + worked example + "you cannot skip it" aside, all at once). Symbols-before-intuition is his failure mode — one idea per beat, picture before algebra.
- **Student state:** engaged and pushing back well (challenged "aren't we building text→vector ourselves?" — good instinct, answered honestly with the Phase 7 dependency chain). Tired at the end; asked to wrap and continue on another machine.
- **Still owed:** Phase 1 demo GIF.

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
