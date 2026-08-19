# Prompt for the portfolio-repo Claude session — Spidy v3 (19 Aug 2026)

Paste everything below the line into a Claude Code session opened in the **portfolio repo**
(`~/Desktop/portfolio`, currently on branch `redesign`), not this one.

Every API fact below was verified against the live service with `curl` on 19 Aug 2026 —
the endpoint is deployed and answering. Deadline: the article that points readers at this
behaviour publishes **Thu 20 Aug 2026, 9:00 AM IST**.

---

I have a chat widget ("Spidy") on my portfolio that talks to a FastAPI backend I wrote.
The backend has a **new v3 endpoint that is already live**. The widget currently offers only
v1 and v2. I need **v3 added as the new default version, with its build write-up page**, before
9 AM IST tomorrow — an article I'm publishing tells readers to come and try v3's new behaviour.

Read `src/spidyVersions.ts`, `src/spidyApi.ts`, `src/portfolio.config.ts` and
`src/components/AskBot.tsx` first, then tell me your plan before changing anything.

## 1 — The API contract (copied from the FastAPI source, then verified live)

**Base URL:** `https://ai-voice-assistant-su60.onrender.com` (same host as v1/v2 —
`ASSISTANT_HOST` in `portfolio.config.ts` already covers it, nothing to change there).

```
POST /v3/ask
Content-Type: application/json

{
  "question": "which company does he work for right now?",
  "history": [
    { "role": "user",      "content": "does he know MongoDB?" },
    { "role": "assistant", "content": "He has used MongoDB only in college..." }
  ]
}

200 → { "answer": "...", "version": "v3" }
```

**v3 is byte-identical to v2 on the wire.** Same Pydantic model (`AskV2Request`), same
`{question, history}` body, same `{answer, version}` response. In this repo's vocabulary it is
the **`history` contract family** — so `askWithHistory()` in `src/spidyApi.ts` serves it
**unchanged**. Do not add a new request function, and do not add a `version === 'v3'` branch
anywhere. If you find yourself editing `spidyApi.ts`, stop and tell me why.

**Server-side constraints (unchanged from v2, and still hard):**

- `role` is a strict `Literal["user", "assistant"]`. A bad role 422s the **whole** request.
- `history` is optional, defaults to `[]`. Empty array == stateless behaviour.
- Extra body fields are silently dropped.
- Rate limit **20 requests/minute per IP** → `429`.
- Upstream model failure → `502` with `{"detail": "..."}`.
- CORS already allows `https://hemavardhanreddy.vercel.app` and `http://localhost:5173`.
  **Do not ask me to change the backend.**

## 2 — What v3 actually does differently (this is the whole point of the release)

v2's retrieval: embed the question, take the **top 5 chunks by cosine similarity**, always.
Top-k always returns k, so v2 *always* has context, even when the context is junk.

v3's retrieval, server-side:

1. retrieve the **top 20** by cosine (wide and cheap),
2. rerank those 20 with a **cross-encoder** (`cohere/rerank-v3.5` via OpenRouter) which reads
   `(question, chunk)` together and scores relevance directly,
3. **drop everything below an absolute cutoff of 0.18** — calibrated on the real corpus
   (highest junk score measured: 0.158; lowest correct-answer score measured: 0.204),
4. keep the best 3.

**If nothing survives the cutoff, the server never calls the LLM at all** and returns this
exact string — it is a hardcoded constant, not model output:

```
I don't have that in my notes. For anything not covered here, it's best to ask
Hemavardhan directly at gillolahemavardhanreddy@gmail.com.
```

That abstention is the feature. v3 is the first version that can find nothing and say so.

**Two live responses I captured today, use these as the demo/proof pairs:**

| question | v2 | v3 |
|---|---|---|
| *which company does he work for right now?* | "I don't have that information." (wrong — `Way2News` is in the notes 5×; cosine matched the word *company* to *"company stages"* / *"product company"*) | "Hemavardhan currently works at **Way2News** in Hyderabad as a Backend / Full-Stack Software Engineer, a position he's held since February 2025. [about.txt]" |
| *what car does he drive?* | a polite four-line paragraph explaining what it does have and offering to help with something else | the one-line abstention above |

**Latency** — measured on the live deployment today:

- reranking adds **~0.9 s** of server time per question (0.73 s → 1.64 s internal), plus
  **$0.001 per query**, priced per search not per document.
- End-to-end from my machine: **8.5 s** on a warm-ish box, **22.5 s** cold start on `/health`
  (Render free tier spins down).
- The endpoint **does not stream** — one complete string. Keep the existing thinking indicator,
  the disabled input while in flight, the timeout/retry, and the `/health` warm ping on open.
  v3 is the slowest version, so if the escalating status copy in `AskBot.tsx` has thresholds,
  sanity-check them against ~9 s rather than ~4 s.

## 3 — Task A: add v3 to the registry

`src/spidyVersions.ts` is built so that a new version is **one entry, newest first**, and that
entry drives the widget timeline, the `/spidy` index, the static `/spidy/v3` route and its
link-preview card. Follow that design — do not special-case v3 anywhere else.

The entry:

- `id: 'v3'`, `path: '/v3/ask'`, `contract: 'history'`, `status: 'live'`, `released: '2026-08'`.
- `name` — the human label in the picker, in the same voice as `'no memory'` / `'remembers the
  conversation'`. Something like `'knows when it doesn't know'`. Propose 2–3 and let me pick.
- `whatChanged` — one sentence a recruiter understands: it now reranks what it retrieves and
  says "I don't have that in my notes" instead of answering from irrelevant context.
- `limitations` — honest, from my own notes: text only; retrieval is still meaning-only, so
  exact terms like `ClickHouse` or `PM2` can still be blurred (hybrid search is the next fix);
  the relevance cutoff is a hand-calibrated constant and has to be re-derived if the notes or
  the reranker change; ~0.9 s slower per question.
- `stages: ['question', 'retrieve', 'rerank', 'context', 'generate']` with
  `primaryStage: 'rerank'` — `'rerank'` already exists in `PIPELINE_STAGES`.
- **Demote `v2` to `status: 'legacy'`** (it renders as "superseded"), matching how v1 was
  treated when v2 shipped. v2 stays selectable and still works — confirm the picker still
  offers all three and that `newestVersion` / the default selection resolve to v3.

## 4 — Task B: the `/spidy/v3` and `/spidy/v2` write-ups

**Both write-ups are already drafted for you** at
`/Users/hemavardhang/ai-voice-assistant/docs/prompts/spidy-v2-v3-articles.md` — read that file
first. It is written in this repo's own vocabulary: headings map 1:1 onto `sections[]`, every
paragraph is labelled with its block `kind`, and it includes the `proof` pairs, the suggested
`name` / `whatChanged` / `limitations` / `stages` for both entries, and which figures exist.
Prose there is final-draft — assemble it, don't rewrite it, and bring me anything you think is
wrong rather than silently improving it.

**v2 currently has no `article` field at all**, so this task covers both versions. It also
carries two corrections to the existing v2 entry, both explained in that file: `stages` should
be `['question', 'retrieve', 'context', 'generate']` (v2's second half was query rewriting,
which changes the `retrieve` stage — the current `['context']` undersells it), and its
`limitations` list gains the two that v3 exists to answer.

The full 2,300-word source for v3 is `docs/prompts/linkedin-article-v3.md` in the same repo, if
you need more than the portfolio cut. Do **not** invent numbers; every figure came from a
session log. Load-bearing facts for v3:

- **Headline angle:** last month's article published a rule — *"the score means nothing, only
  the order does; take the top five, never a threshold"* — and an unsolved problem: *"there is
  no way for it to report that it found nothing."* v3 solves the problem by breaking the rule.
- **`proof`** (goes above the fold): use the *"which company does he work for right now?"* row
  from the table above — before = v2's "I don't have that information" (verdict: the answer is
  in the notes five times), after = the Way2News answer with its `[about.txt]` citation.
- **Bi-encoder vs cross-encoder** — separately-encoded directions vs reading the pair together.
  This is why the score becomes thresholdable at all.
- **The mistake in the middle:** cutoff of 0.05 calibrated on lab documents (`the sky is blue`,
  `cat is sitting on the mat` scored 0.015/0.024) did nothing on the real corpus, where every
  chunk is about the same person — *"is he married?"* pulled *"He is currently open to
  opportunities"* at **0.158**. Re-derived on real failing queries: junk tops out at 0.158,
  the lowest correct answer sinks to 0.204, cutoff set at **0.18** with the provenance written
  into the code above it.
- **Why not an adaptive rule:** the elbow method cuts at the biggest gap — on
  `0.411, 0.073, 0.036, ...` that is between the two *correct* chunks. Every relative rule
  ("within 15% of the top", "mean + 1 SD") defines the line from the candidates present, so
  **none of them can ever return nothing**. Only an absolute number can abstain.
- **The null result, kept in on purpose:** golden-set MRR was **0.93 before and 0.93 after**.
  Six files on distinct topics means nothing was buried at rank 9 for a reranker to rescue.
  It shipped for the abstention, not for the ranking.
- **The closing lesson:** a test suite tests what you thought of — it was 7/7 green while the
  bot couldn't name my employer. That question is now a permanent row in the suite, the first
  one harvested from a real production failure.
- Nice extra: *"has he worked with Kubernetes?"* scores **0.834** — the day's highest — on the
  chunk that says he **hasn't**. Relevance is not agreement.

**Figures:** the six PNGs (`01-cosine-cone`, `02-bi-vs-cross`, `03-two-scales`, `04-the-gap`,
`05-elbow-trap`, `06-way2news`) live in `~/Desktop/spidy-v3-figures/` **on my other laptop** —
check whether that directory exists here first. If it does, copy them into `public/spidy/` and
set `src`. If it doesn't, **declare the `Figure` entries without `src`** — the type makes it
optional precisely so unfinished figures are hidden in production and shown as labelled slots
in dev. Do not ship empty boxes, and do not block on the images.

`DiagramId` is a closed union backed by hand-written renderers in `SpidyFigures.tsx`. Reuse
existing ids only. If you think a v3 idea (the calibration gap, the elbow trap) deserves a new
inline diagram, propose it as a separate follow-up commit — do not silently add one.

## 5 — Task C: make the new behaviour easy to see

The article sends readers here specifically to try abstention, so:

- The abstention answer arrives as a normal `200` with a short body and **no citation**. Make
  sure nothing in the widget treats a citation-less or short answer as an error state.
- If the widget renders links or has an email affordance, the `gillolahemavardhanreddy@gmail.com`
  in that string should be clickable. If it currently renders plain text, tell me the cost
  before adding a linkifier — I'd rather ship plain text than a regex I don't trust.
- If there are suggested-question chips, put both demo questions in reach:
  *"which company does he work for right now?"* (v3 right, v2 wrong) and
  *"what car does he drive?"* (v3 abstains, v2 waffles). The version picker keeps the messages
  on screen across a switch, so a visitor can perform the contrast themselves — that comparison
  is the release.

## 6 — How I'd like you to work

- Plan first, and show me the registry entry's prose (`name`, `whatChanged`, `limitations`)
  before you write the article body — the voice matters more than the volume.
- Separate commits: (1) v3 registry entry + v2 demotion/stages fix, (2) the two articles,
  (3) any widget/UX fix.
- Run `npm run build` — `tsc -b` plus the `spidy-routes` plugin, which must report one more
  emitted page than before. Then check `/spidy`, `/spidy/v3`, `/spidy/v2` (it has a real article
  now, not just the facts block) and the widget in `npm run dev` at 320px, 375px and 768px.
- Ask a real question against v3 from the running dev server before you call it done, and paste
  me the answer. Don't verify by reading code alone — the backend is real and cheap to hit.
- I want to understand the changes, not just receive them.
