# Progress Tracker ✅

Tick each atom as you finish (`[ ]` → `[x]`). Acharya resumes from here each session.

**New rules (26 Jul 2026):** every phase ends with a **ship-it atom** (README + demo GIF + write-up → portfolio card on hemavardhanreddy.vercel.app). Classical ML/MLOps/vision/n8n live in **future projects P2–P4** — see `docs/project-roadmap.md`.

**Currently at:** 🧩 **Phase 2 — RAG works end-to-end with source citations (through 2.9b ✅).**

### ▶️ START NEXT SESSION HERE — student must pick A, B, or C
He stopped before reading these. **Open the session with the recall warm-up, then re-offer this choice verbatim.**

- **A) Follow-up questions ⭐ (Acharya's recommendation, ≈1 atom).** Right now every question is a cold start — a recruiter can't ask *"and what about his notice period?"*. Fix = conversation-only history (keep the Q/A turns, retrieve **fresh** context every turn). This is the **owed memory-snowball fix** from Phase 1, finally applied. Small, and it makes the demo feel like a product.
- **B) Straight to P1.5 v1 — FastAPI service → React widget** on hemavardhanreddy.vercel.app. Taught by building the real thing, starting from his own `flask SELFLEARN/app.py` (it already has his Express→Flask comparison comments). Carries the proper hang fix: `await asyncio.wait_for(call(), timeout=20)`. **Before it goes public: CORS + rate limit + spend cap**, or his OpenRouter key funds strangers.
- **C) LLM-based semantic chunking.** Honest advice: **skip for now.** His notes are already clean and hand-sectioned; build this when the data actually needs it, not before.

**Unanswered thread he raised (answered in chat, worth re-stating):** *how can a model cite a file it was never given?* → because a filename is just predicted tokens. The realistic failure isn't an invented file, it's **mis-attribution among files it WAS given** — and the `issubset` check does not catch that. Risk rises with bigger `k` and with conversation memory (option A adds old filenames to the context).

**New rule (27 Jul 2026, student's call):** revision notes live in **`docs/notes/`**, one file per phase, and Acharya appends a card **after every atom** (option b — live, never a backlog). Card format: 💡 idea → 💻 the line that matters → ⚠️ gotcha → ❓ self-test in a `<details>` toggle. Phase 1 + Phase 2 backfilled.

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
- [x] 2.3a Installed `sentence-transformers` (5.6.1) — pulled `torch` (Phase 7) + `transformers` (Phase 8) into the venv for free
- [x] 2.3b First real embedding (`learn/phase2/embeddings.py` — `all-MiniLM-L6-v2`, ~90MB one-time download; `vec.shape == (384,)` for ANY length text)
- [x] 2.3c Callback: `np.linalg.norm(vec) == 1.0` → the model already returns **unit vectors** ⇒ cosine collapses to plain dot product **ATOM 2.3 DONE**
- [x] 2.4 🔧 Cosine similarity (`learn/phase2/cosine.py` — `np.dot(a,b)/(norm(a)*norm(b))`; 2D "dogs vs money" toy vectors → puppy/retriever `0.998`, puppy/stocks `0.165`). Re-taught geometrically after the algebra proof failed: arrows → angle → number; dot product = **AND-gate agreement score** (a JS `for` loop of `a[i]*b[i]`), lengths divided out so only direction counts. Text→geometry bridge finally landed.
- [x] 2.5 Similarity on real text (`learn/phase2/similarity.py`, `cosine.py` now its own importable module — Atom 2.0c imports reused). `cat`/`kitten` **0.788** vs `cat`/`car` **0.463** ⇒ meaning beats spelling. ⚠️ Key catch: the floor is **NOT 0** (~0.3–0.5 for any two English words) ⇒ **never threshold on absolute cosine, only rank.** Revisit at 2.7.
- [ ] 2.5a 🧮 Span/basis — "features are directions, a vector is a recipe"
- [ ] 2.5b 🧮 Projection — "the dot product is a shadow" *(partly pre-taught at 2.4 via the adjacent-side picture)*
- [x] 2.6a 🧮 **Anisotropy / the cone** — PULLED FORWARD (student's curiosity about the `0.46`). 10 pairs of wildly unrelated words (`cat/car/banana/democracy/hydrogen`) → **not one near 0**; floor `0.186`, ceiling `0.463`. Cone proven. Ranking is semantically real (`car/hydrogen 0.401` > `car/democracy 0.354` ⛽). **Rule earned: absolute cosine lies, ranking tells the truth → always top-k, never a threshold.**
- [x] 2.6b 🧮 **Centering** — `vecs.mean(axis=0)` → `centered = vecs - mean_vec`. **All 10 pairs went negative**, average **`−0.2484`** vs the theoretical `−1/(n−1) = −0.25` for n=5 ✅. Taught with the balance-point/tug-of-war picture (n=2→−1, n=3→−0.5, n→−1/(n−1)); student's own summary was right: *cosine measures direction from an origin, so moving the origin changes every angle.* Corrections given: angles change, **distances don't**; and real similarity **survives** (ranking held) — only the shared lean died. Third independent proof of the top-k rule.
- [x] 2.6c **Pooling** (student's unprompted question: *"embedding models give a vector per token — why one per sentence?"*). Answered: the model emits `(n_tokens, 384)` then **mean-pools + normalizes** — the *same* `.mean(axis=0)` he'd just typed, different axis meaning (he subtracts the mean; the model keeps it). Consequence named: pooling blurs ⇒ **this is why we chunk**. Hands-on proof (`output_value="token_embeddings"`) offered and **made optional — he took the concept and moved on**; nothing depends on it.
  - ✅ **Black-box promise re-stated & verified against the syllabus:** token→vector = **7.7** (lookup table, he builds one), context-awareness = **7.8–7.12** (attention/Q·K·V/masking), where the weights came from = **7.13** + Phase 8. He explicitly asked "can I leave with confidence?" → yes, given green light.
- [x] 2.6 ✅ **VECTOR STORE BUILT** (`learn/phase2/store.py`, data `learn/phase2/about.txt`). Chunk (`split("\n\n")`) → embed (`model.encode(chunks)` → `(2, 384)`) → `search(query, k)` with sort + slice. 🏆 **The rule paid off on his own data:** correct AI chunk `0.416` vs wrong chunk `0.284` — and `0.416` is **below** `cat/car 0.463`, so a `> 0.45` threshold would have silently returned nothing. Ranking was perfect. He fixed `cosine.py`'s `__main__` guard himself. Named his data file `about.txt` (not `about_me.txt`).
- [ ] ⬜ **OPEN CHECK-QUESTION, ask first next turn:** `search("what is his salary expectation?", k=1)` — file says nothing about salary, top-k returns a chunk anyway. Is that a bug? (Answer: no — top-k always returns k; the "I don't know" guardrail is the LLM's job at **2.8**.) He hasn't run it yet.
- [x] 2.7 ✅ **Retrieval on real data.** `about.txt` rewritten from his resume (I extracted the PDF — `pypdf` installed into `.venv` at his request; source: `~/Desktop/portfolio/src/Hemavardhan_resume_latest.pdf`) into **27 one-idea chunks**. **3/4 correct at k=1.** 🏆 The instructive miss: *"what is he learning right now?"* → rank 1 was *"eager to **learn** anything"* (surface-form trap), but **k=3 recovered both correct chunks** (0.248 AI-voice-assistant, 0.175 deep-interest-in-AI). **Rule earned, deeper than 2.6: don't trust rank #1 either — the retriever's job is to get the right chunk *into* the k, the LLM filters.** Also separated the two failure modes: blended chunk → fix chunking; wrong winner → fix k.
- [x] He asked unprompted about **LLM-based semantic/propositional chunking** — confirmed it's a real named technique, cheap because it runs once at ingest; **build it for real at 2.9** on messy notes where `\n\n` won't save us.
- [x] 2.7a 🧮 ✅ **Search = ONE matrix × vector multiply.** Taught picture→numbers→formula→code (2D 3-row worked example by hand). `search()` rewritten loop-free: `scores = vecs @ q` + `np.argsort(...)[::-1][:k]`. Shape rule landed: `(27×384) @ (384,) → (27,)`. **Two gotchas fixed live:** (1) `@` is only cosine *because MiniLM normalizes* — proved with the `[1,0]` vs `[6,8]` example where the long-but-wrong vector wins 6-to-1 raw; habit given: `norm()`-check any new embedding model. (2) He'd left `vecs = [model.encode(c) for c in chunks]` (list of arrays, 27 calls) → corrected to batched `model.encode(chunks)` → real `(27, 384)`. Matrices earned by need; bridges to Phase 7 attention.
  - ⬜ He did **not** run the `print(model)` / `norm(vecs, axis=1)` verification lines — said he was satisfied conceptually. Optional, nothing depends on it.
- [x] 2.8 ✅ **RAG WORKING** (`learn/phase2/rag.py`) — streaming + his `Memory` class (his own extension, unprompted) + `from store import search`. 🛡️ **Guardrail proven:** salary question → *"I don't have that information."* 🐛 **Five bugs debugged live** (wrong module name; `add()` signature; user message added AFTER the call = silent failure; `delta` vs accumulated `s`; `while 1:` above the `__main__` guard). 🔬 **Two retrieval misses found and fixed on his own data:** Acharya/Kira ranked 5th+ (long-chunk pooling dilution — lost to a Jest/Postman chunk) → fixed by splitting headline from detail + `k=5`.
  - 🔥 **THE BIG ARTEFACT — the three retrieval failure modes table** is now in `docs/notes/phase-02-memory-rag.md`: (1) blended chunk → fix chunking; (2) wrong winner → fix k; (3) **vocabulary mismatch** → fix query/hybrid/metadata. All three hit him on real data. Mode 3 is live and unfixed: *"what does he do at his current job?"* retrieves **none** of the payments chunks (sports committee ranks #2) because those chunks never say "job/work/Way2News".
  - ⬜ **OWED:** the memory-snowball fix — storing `CONTEXT + question` every turn reintroduces the 1.6 quadratic cost that RAG was meant to cure. Fix = conversation-only history + fresh context per turn.
  - ⬜ **OWED:** `answer()` streams and returns `None` → `print("A:", answer(q))` prints a trailing `A: None`.
- [x] 2.8a ✅ **Contextual retrieval — vocabulary mismatch FIXED.** `about.txt` restructured with `#` section headings; `store.py` now builds **two parallel lists** — `chunks` (shown to the LLM) and `embed_texts` (`f"{section}: {block}"`, what we embed). **Key idea he now owns: embed one string, display another.** Results: *"current job"* → payments/Cashfree/admin-console chunks (was: sports committee, zero payments); *"what is he learning"* → both AI chunks at `0.494` (was: the *"eager to **learn**"* trap at 0.319); *"payments at scale"* → all three payments chunks at ranks 1–3. RAG answer for Q1 is now genuinely good.
  - ⚠️ Taught alongside: **rising absolute scores ≠ better retrieval** (the whole band shifted because headings are question-shaped) — the proof is the *ranking* changing. Fourth appearance of the top-k rule. Also flagged the opposite risk: over-dominant headings collapse within-section discrimination.
  - 🐛 **Parallel-list drift bug**, debugged live: he left the old `chunks = [...]` line above the new loop → `chunks` 78 entries vs `embed_texts` 33 → `search()` scored one chunk and printed another (*"does he know databases?"* → Acharya at 0.479; `#` headings shown as content). **No error, no crash.** Lesson given: build parallel lists in one loop + `assert len(chunks) == len(embed_texts)`. He caught the nonsense himself by reading the output.
  - 💬 **His reaction — worth remembering:** *"so is this all RAG means... it's too simple actually."* Answered honestly: yes, the core really is ~15 lines; simple to build, hard to make good; the difficulty is measurement, messy data, scale — and this same "simple core, hard engineering" shape recurs (softmax, attention), which is why Phase 7 is learnable.
- [x] 2.9a ✅ **FOLDER LOADER DONE** (28 Jul 2026). `store.py` now `glob`s `learn/phase2/notes/*.txt` → **6 files → 127 chunks**, three parallel lists (`chunks` / `embed_texts` / `sources`, filename via `file.split("/")[-1]`), guarded by `assert len(...) == len(...) == len(...)`.
  - 🐛 **Two bugs, both instructive.** (1) `notes.*.txt` (dot for slash) → 0 files → crash surfaced 26 lines downstream inside `vecs @ q` as a matmul-dimension error. **Lesson: read the first anomaly (`0 files → 0 chunks`), not the traceback.** (2) `sources.append()` left in the *outer* per-file loop → 6 vs 127 → **the `assert` fired immediately.** Contrast drawn with 2.8a, where the identical drift bug had no assert: no crash, silent wrong answers, a whole debugging round lost. Rule earned: **parallel appends live in the same block.**
  - ⚠️ Also taught: `assert` passed on the empty run (`0 == 0 == 0`) ⇒ **it checks the invariant you named, not correctness.**
  - 🏆 **`boundaries.txt` paid off live:** *"does he know databases?"* → #1 MySQL/ClickHouse/Redis `0.544`, **#2 "MongoDB only in college and side projects, not in production" `0.531`** — the honest limit retrieved beside the strength, so the LLM can't over-claim. *"What is he learning right now?"* now ranks both AI chunks #1/#2 (`0.581`/`0.571`) — the 2.7 surface-form trap is fully dead. Score band rose to 0.5–0.58; **flagged for the 5th time that rising absolute scores ≠ better retrieval.**
- [x] 2.9b ✅ **CITATIONS WORKING.** `search()` returns `(score, chunk, source)`; `rag.py` context is `f"[{src}] {chunk}"` + a cite-your-source line in SYSTEM. *"Does he know Kubernetes?"* → *"No, he has not worked with Kubernetes or container orchestration…"* **`[boundaries.txt, skills.txt]`** ✅
  - ⚠️ Taught: **data ≠ instruction** — line 22 was correct for 3 runs before the SYSTEM line was added, so the model *received* the `[src]` tags and correctly ignored them. Also: **the citation is testimony, not evidence** (verify with `print([src for score, chunk, src in hits])`), and changing a return shape breaks every caller *silently* in Python.
  - 🏆 **The accidental headline experiment:** salary → *"I don't have that information"* at 2.8, → *"10–16 LPA, open to discussion"* at 2.9, with **zero logic changed** (only `preferences.txt` now exists). **In RAG, knowledge is a DATA problem, not a CODE problem** — the whole commercial argument, discovered by accident.
  - 🐛 **Big debugging case study, fully written up in `docs/notes/phase-02-memory-rag.md`:** an intermittent 30–90s silent hang. Chain taught: `Ctrl+C` traceback was 100% in `httpx` ⇒ *waiting, not stuck* → `timeout` is **per attempt** (30×3 = 90s) → **a read timeout protects you from silence, not noise** (OpenRouter keep-alive filler resets the clock) → **an in-loop watchdog can't fire on the thread it's watching**. Both hypotheses killed by experiment (content: ran alone, fine; position/rate-limit: reordered, fine). **Verdict: transient upstream stall — no cause in his code.** Rule earned: *when the plausible hypotheses are dead and it still comes and goes, stop hunting a root cause and design for survival.* Kept the `try/except`, **deleted the watchdog** (dead safety code is worse than none). Real fix deferred to FastAPI: `await asyncio.wait_for(...)`.
  - 📌 **`story.txt` DEFERRED by his call (28 Jul 2026): after v1 deployment, not before.** Reason (his words): deciding/thinking on behavioural material takes time and would stall the build. Not dropped — 6 questions still stand.
  - ✅ **Knowledge base written: `learn/phase2/notes/`, 6 files, 44 sections, 132 chunks** (was 30 in 1 file). Sources: his resume PDF (`~/Desktop/portfolio/src/Hemavardhan_resume_latest.pdf`), his **portfolio source at `~/Desktop/portfolio`** (`src/portfolio.config.ts` + `.env` metrics — far richer than the resume), the npm registry API, and GitHub. LinkedIn blocked (HTTP 999); npm web blocked (403) → used `registry.npmjs.org` + `api.npmjs.org` instead.
  - Files: `about.txt` · `projects.txt` · `skills.txt` · `preferences.txt` · `faq.txt` · **`boundaries.txt`** (the sleeper — honest gaps so the bot can't over-claim; taught as *"in RAG, negative facts matter as much as positive ones"*).
  - **Decisions he made this session:** salary **10–16 LPA** · notice **2 months** · Hyderabad preferred, open to South-India relocation, any work mode · **email + links only, NO phone anywhere** · **no npm download numbers** (198/183 first month reads weak) · LinkedIn skipped · uses the **newer portfolio metrics (₹5.2Cr / 74,000)** over the resume's stale 4.9Cr / 68,900.
  - **New facts surfaced that his RESUME IS MISSING — tell him to update the PDF:** he **leads a team of 4 engineers**; the **customer-recovery CRM** (48,000+ drop-offs across 9 stages, 16,520 recovered, 69% return / 34% paid, attribution split 7,942 calls vs 10,874 WhatsApp); the Journey Explorer; the migration framework; the in-progress admin/customer service split. Also: Kira is an **overlay on Acharya**, not independent (both MIT, v1.0.0, 7 Jul 2026).
  - Confirmed gaps: **no Java/Spring, no Kubernetes/Docker orchestration, no Kafka, no GraphQL; MongoDB college/side-projects only** (so "MERN dev" in CLAUDE.md overstates his Mongo experience — production DBs are MySQL/ClickHouse/Redis). Languages: English + Telugu strong; Hindi understands, struggles to speak.
  - ⬜ **`story.txt` NOT written — deliberately.** Behavioural material must be in his own words; 6 questions given (why backend · hardest build/debug · proudest · what went wrong · why AI now · a disagreement). **He asked to build it next session, before finishing 2.9.**
- ⚠️ Housekeeping owed (1 min): `cosine.py` has no `if __name__ == "__main__":` guard, so its `puppy vs retriever` demo prints on every import — flagged, Atom 2.0c callback, not yet fixed.

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
