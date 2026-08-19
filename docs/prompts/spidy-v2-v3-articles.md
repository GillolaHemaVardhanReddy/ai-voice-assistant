# Spidy v2 + v3 — build write-ups for the portfolio `/spidy` series

Source material for the `article: VersionArticle` field in `~/Desktop/portfolio/src/spidyVersions.ts`.
v1's entry already has one and is the reference for voice and structure — these two are written to
match it: same block kinds, same "what it still could not do" ending, same rule that **every number
comes from a session log, nothing is invented.**

Written 19 Aug 2026 from `docs/notes/p1.5-recruiter-bot-service.md` (P1.7.0–P1.7.4), the session log
(S13, S15, S21, S22), and the live service. Numbers marked ✅ were re-verified with `curl` today.

**Assembly notes for whoever pastes this in:**

- Block kinds available: `p` · `list` · `pull` · `callout {lines, punchline}` · `stats {items}` ·
  `photo {figure}` · `diagram {id}`.
- **`DiagramId` is a closed union** (`'ratio' | 'shrink' | 'architecture' | 'scores'`) backed by
  hand-written renderers in `SpidyFigures.tsx`. v2 and v3 below use **no** `diagram` blocks —
  the places where one would help are marked 🎨 as optional follow-ups.
- `photo` figures may omit `src`; the type makes it optional so unshot figures hide in production
  and show as labelled slots in dev. Every figure below is listed without a `src` unless the file
  already exists.
- Headings and block order below map 1:1 onto `sections[]`. Prose is final-draft — edit for voice,
  not for facts.

---

# v2 — the registry entry

The existing `v2` entry keeps its `id`, `path`, `contract`, `released`, `name`
(`'remembers the conversation'`) and `whatChanged`. Three fields to change:

- **`status`** → `'legacy'` once v3 ships (renders as "superseded").
- **`stages`** → `['question', 'retrieve', 'context', 'generate']`, currently just `['context']`.
  That is a factual fix, not a polish: v2's second half was **query rewriting**, which changes what
  gets embedded — the `retrieve` and `question` stages. Keep `primaryStage: 'context'`; memory is
  still what the version was about.
- **`limitations`** → the current two are true but thin. Suggested replacement:
  - `'Text only'`
  - `'Remembers the last few turns, not the whole thread'`
  - `'The retriever still cannot say "no match" — top-k always returns five chunks'`
  - `'No streaming, so the 4–5 second wait is silent'`

---

# v2 — the article

**headline**

> The model remembered the conversation. The search engine didn't.

**lede**

> v1 answered every question as if it were the first one ever asked. Adding memory took twenty
> lines, because a language model has no memory to add — you just re-send the transcript. Then the
> follow-ups still broke, and the reason had nothing to do with memory: the retriever was still
> being handed the word *"it"* and asked to find something.

**proof** — the two-turn test, both arms measured (S15)

- `question`: *"so he knows it?"* — asked straight after *"does he know MongoDB?"*
- `before` — label **v1 · no memory**
  - answer: *"I don't have enough context to answer what 'it' refers to."*
  - verdict: ✕ The pronoun has nothing to point at — the question arrived alone
- `after` — label **v2 · remembers the conversation**
  - answer: *"He has used MongoDB in college and side projects, but not in production. [boundaries.txt]"*
  - verdict: ✓ Resolves the pronoun against the previous turn, and still cites its source

## Section: Why this version existed

`p` — v1 was stateless by construction. Every request built exactly two messages: the system prompt
and the question. That is fine for *"does he know MongoDB?"* and useless for the way people actually
talk, where the second question is *"so he knows it?"* and the third is *"and is he good at it?"*.

`p` — A recruiter does not re-state the subject of every sentence. If the assistant needs them to,
it isn't a conversation, it's a search box with manners.

## Section: Memory is a lie you re-tell every request

`p` — The first surprise: there is nothing to build. The model has no memory and never will — every
call is a stranger reading the page for the first time. "Memory" is the `messages` array getting
longer. Nothing is stored, nothing is looked up; the whole past is re-sent and re-read from scratch,
every single request.

`callout`
```
lines:     v1:  [ system,             user ]
           v2:  [ system, ...history, user ]
punchline: That is the entire feature. The server stores nothing — the browser holds the
           conversation and hands it back on every request.
```

`list` — What that shape forces you to get right:
- **Order is design, not formatting.** The model reads top to bottom and answers the *last* message.
  History sits behind the new question as background; put the new question in the middle and it
  stops being the thing being answered.
- **History goes in as real `user`/`assistant` turns, never inside the retrieved context.** Context
  is evidence from my notes. History is what was said. Fold them together and *"things I said"*
  start reading as *"facts from his files."*
- **Cap what you send.** The full array is replayed to the model on every request, so an uncapped
  thread grows cost and latency without bound. The widget keeps the whole thread for display and
  sends the last few turns.
- **The endpoint raises now, the handler decides.** v1 swallowed its own errors and returned `None`.
  v2's `answer()` raises and the route turns it into a clean `502`. Libraries raise, callers decide.

`p` — `stream=True` came out. v1 streamed tokens from the provider and then glued them into one
string before responding, so the streaming bought nothing — the visitor waited for the whole answer
either way. It comes back when there is a real pipe to push into.

## Section: The bug that memory didn't fix

`p` — With history wired, I asked *"does he know MongoDB?"* and then *"so he knows it?"*, and the
answer was right. It was right for a reason I hadn't earned. Retrieval still ran on the raw sentence
the visitor typed:

`callout`
```
lines:     hits = search(question, k)    ← `question` only. History never reaches it.
punchline: The model remembered the conversation. The search engine was still being handed
           the word "it" and asked to find something.
```

`p` — So I checked it with no model involved at all — same retriever, same `k=5`, two queries, and
the cosine scores printed. Deterministic, free, and it cannot flatter itself.

`stats`
- *"Does he have experience in MongoDB?"* → **0.620**, right chunk at #1
- *"so he knows it?"* → **0.344**, right chunk **absent from the top five**
- Unrelated-words floor, measured earlier → **0.186**

`p` — Every score in the second query sits below every score in the first, and 0.344 is not far off
the floor for words that have nothing to do with each other. The retriever found nothing. It
returned five chunks anyway, confidently, because **top-k always returns k** — there is no way for
it to report a miss.

`pull` — *"The answer had been correct because the previous turn's evidence was still sitting in the
history. The retrieval for that turn was junk, and the junk was in the answer."*
label: The seam I could see in my own output

`p` — The proof was in the good answer itself. It ended *"it's best to ask him directly — he prefers
that to having assumptions made on his behalf"*, which is a paraphrase of the top junk chunk for
*"so he knows it?"*. The reply was a blend: MongoDB facts from the history, the closing sentence
from that turn's useless retrieval. You could see the seam.

## Section: Two fixes, and the one that scales

`p` — The obvious fix is to embed the history along with the question. I tried it, and it works —
for about two turns.

`stats`
- *"Does he have experience in MongoDB?"* → top **0.620**, gap to second place **0.128**
- *"…MongoDB? so he knows it?"* → top **0.585**, gap **0.091** — the margin fell 29%
- Four junk words also pushed an unrelated chunk into second place

`p` — An embedding is roughly the average meaning of the sentence. Two ideas in, and the arrow lands
between them; add noise and the average drifts off topic. At two turns that costs you margin. At
a hundred and twenty messages the current question is one arrow out of a hundred and twenty and the
topic drowns.

`p` — So the fix is **query rewriting**: one cheap model call turns *"so he knows it?"* into
*"Does Hemavardhan have knowledge of MongoDB?"* **before** anything is embedded. What gets searched
is always one short clean sentence, never a growing blob. If there is no history at all, the
function returns the question untouched and makes no call — first-time visitors pay nothing.

## Section: The rewriter took four attempts, and the fix was not a better prompt

`p` — Getting a model to rewrite a question and *only* rewrite the question is harder than it reads.
Four runs, in order:

`list`
- **Run 1** returned *"Based on the conversation history, here's the rewritten question:"* followed
  by the question **and an answer**. The prompt never said "don't answer."
- **Run 2** rewrote it as *"…experience with MongoDB **in production environments**?"* — it had
  absorbed a detail out of the assistant's previous reply. The question now meant something narrower
  than what was asked.
- **Run 3** added *do not change the meaning* in bold-ish English. Still drifted:
  *"Does Hemavardhan have **production** experience with MongoDB?"*
- **Run 4** ✅ *"Does Hemavardhan have knowledge of MongoDB?"* — and the change wasn't in the prompt.

`pull` — *"You cannot fix a structural problem with more adjectives."*
label: The lesson from run 3 to run 4

`p` — The input was one run-on smear — `user: … assistant: … so he knows it?` — with nothing marking
where the history ended and the question began. The fix was labelled blocks, `HISTORY:` and
`QUESTION:` on their own lines. The same trick already sitting one file over, where retrieved
evidence is labelled `CONTEXT:`. Three rewrites of the instructions lost to one heading.

`p` — And the receipts were in the citations, not in my reading of the wording: the contaminated
runs cited `[boundaries.txt, skills.txt]`, the clean run went back to `[boundaries.txt]` alone. The
retrieval target really had moved, and it really moved back.

## Section: Measuring it without fooling myself

`p` — I wanted the rewriter's cost. The obvious method is to time an answer with it and an answer
without it and subtract. That method is wrong here, and I only knew because I had measured the noise
first — the same question asked three times, nothing changed, just to see how much the number moves
on its own.

`stats`
- Total answer time, no history: **2.76 s** at best, **11.24 s** at worst — same code, same question
- The rewrite call itself, instrumented directly: **~1.8 s**
- The rewrite call when there is no history: **0.0000 s** — the guard means no API call happens
- Cold start on the free tier: **22.5 s** ✅

`p` — The effect is smaller than the noise. Subtracting two totals can never find a 1.8-second
change inside a number that swings by eight seconds on its own, and any answer you get that way is
a coincidence you'll believe. So the timing went onto the *parts* instead — a decorator wrapped
around `rewrite` and `answer`, printing each one's own elapsed time on the real code path rather
than in a benchmark script that doesn't ship.

`pull` — *"Measure your noise floor before you measure your change. Otherwise the first number that
agrees with you wins."*
label: What I took from v2

## Section: What it still could not do

`list`
- **The retriever still could not say "no match."** Top-k always returns five chunks, so a question
  my notes cannot answer still arrived at the model as five confident irrelevant paragraphs. That is
  the whole subject of v3.
- **Retrieval quality was unmeasured.** I had no score for whether the right file came back — every
  judgement was me reading an answer and nodding. The golden set came next.
- **Two model calls per follow-up.** Rewriting costs ~1.8 s and a second call on any turn with
  history. Cheap, but it is the price of the fix.
- **No streaming.** Same total latency as v1, but silent, which feels considerably longer.
- **Exact terms still get blurred.** Meaning-search returns things that are *about* the area when
  you ask for a specific library or product name.

🎨 Optional figures (declare without `src`, or shoot them later):
`retrieval-blind` — the two-query score table, 0.620 vs 0.344 against the 0.186 floor ·
`rewrite-runs` — the four rewriter outputs stacked, wrong to right ·
`timing-swing` — `answer`'s 2.76→11.24 s spread with the 1.8 s rewrite drawn to scale inside it.

---

# v3 — the registry entry

New entry, **first in the array** (newest first drives the default).

- `id: 'v3'` · `path: '/v3/ask'` · `contract: 'history'` · `status: 'live'` · `released: '2026-08'`
- **`name`** — pick one: `'knows when it does not know'` · `'admits when it does not know'` ·
  `'says no instead of guessing'`
- **`whatChanged`** — *"Started re-reading each retrieved note against the question before answering,
  and returning nothing at all when none of them are relevant — so an unanswerable question gets an
  honest 'not in my notes' instead of an answer built from three unrelated paragraphs."*
- **`stages`** — `['question', 'retrieve', 'rerank', 'context', 'generate']`,
  `primaryStage: 'rerank'`
- **`limitations`**
  - `'Text only'`
  - `'The cutoff is a hand-calibrated constant — it has to be re-derived if the notes or the reranker change'`
  - `'Still meaning-only search, so exact terms like ClickHouse or PM2 can be blurred'`
  - `'About 0.9 seconds slower per question, and $0.001 per query'`
  - `'Reranking did not improve ranking on a corpus this small — it earns its place on abstention alone'`

---

# v3 — the article

The long-form version is `docs/prompts/linkedin-article-v3.md` (2,300 words). This is the portfolio
cut — same facts, tighter, same structure as v1's page.

**headline**

> I published a rule last month. Fixing my assistant meant breaking it.

**lede**

> Last month's write-up ended with a rule I was confident about — *the score means nothing, only the
> order does, so take the top five and never use a threshold* — and a problem I had no fix for:
> *there is no way for it to report that it found nothing.* This version solves the second one, and
> the only way to do it was to break the first.

**proof** — verified live today ✅

- `question`: *"which company does he work for right now?"*
- `before` — label **v2 · top-five by similarity**
  - answer: *"I don't have that information."*
  - verdict: ✕ Wrong — the answer is in its notes five times over
- `after` — label **v3 · reranked, with a relevance cutoff**
  - answer: *"Hemavardhan currently works at Way2News in Hyderabad as a Backend / Full-Stack Software
    Engineer, a position he's held since February 2025. [about.txt]"*
  - verdict: ✓ The right chunk, reranked from nowhere to first place at 0.569

## Section: Why this version existed

`p` — Top-k search always returns k. Ask my assistant something my notes genuinely do not cover and
it still received five chunks, confidently, and did its best with them. It could not find nothing,
so it could not say nothing.

`p` — And the failure that finally forced it wasn't hypothetical. I opened my own live portfolio and
asked the most ordinary recruiter question there is — *"which company does he work for right now?"*
— and got *"I don't have that information."* The answer is in the notes five times. One chunk says,
in plain English, *this is his current employer and his current job*.

`callout`
```
lines:     0.502  "He is open across company stages…"
           0.456  "A product company appeals more than a services company…"
           0.445  "He leads a team of 4 engineers…"
punchline: The word "company" matched company stages and product company, and never surfaced
           the chunk that names where I work. My test suite was green the entire time.
```

## Section: A different instrument answers a different question

`p` — The thing that turns text into a direction is a **bi-encoder**: it encodes the two pieces of
text separately. My notes became arrows weeks ago, your question becomes an arrow now, and the
search compares two arrows that were never in the same room. That is exactly why it is fast — one
matrix multiply over 127 rows.

`p` — A **cross-encoder** does the opposite. It reads the question and one chunk **together**, as a
single input, and scores how relevant that chunk is to that question. Different question entirely:
not *"which direction is this pointing?"* but *"does this text answer this question?"* It cannot be
pre-computed, so nobody uses it alone. The standard shape is retrieve wide and cheap, then re-score
narrow and expensive — top 20 by cosine, rerank those 20, keep the best 3.

`p` — I wanted it for the number, not the ordering. A score trained to mean *is this relevant, yes
or no* means something on its own, rather than only relative to whatever else happened to be in the
list. And a score that means something on its own can be thresholded — and a threshold can return
nothing.

## Section: I set the cutoff, and I set it badly

`p` — I built a test with eight documents: two that answer the question, some that are about me but
answer something else, and two absurd ones — *the sky is blue*, *cat is sitting on the mat*. The
absurd ones scored 0.015 and 0.024, the correct one 0.411. Clean separation, big empty gap. I put
the line at 0.05 and felt good about it.

`p` — Then I ran it against my real notes with a question they cannot answer, and got three chunks
back at 0.065, 0.061 and 0.058. All above my line. Nothing about the subject. The cutoff did
nothing.

`p` — My test documents were too easy. *Cat is sitting on the mat* shares nothing with a question
about me — not the subject, not the topic, not even the pronoun. But all 127 chunks in my notes are
about the same person, so every one of them matches on *this is a fact about this man*. The whole
corpus floats about three times higher than a sentence about a cat.

`stats` — measured on the real corpus, questions my notes genuinely cannot answer
- *what is his favourite movie?* → **0.065**
- *what car does he drive?* → **0.079**
- *does he have a US visa?* → **0.094**
- *is he married?* → **0.158**

`p` — That last one is the interesting failure. *"Is he married?"* pulled up *"He is currently open
to opportunities"*, because **open to** genuinely echoes across both meanings. It is not a stupid
mistake, which is what makes it the number that matters. On the other side, the lowest score I could
find on a chunk that *was* the correct answer was 0.204.

`callout`
```
lines:     0.158  ← the highest junk climbed
              ↕     the gap
           0.204  ← the lowest a real answer sank
punchline: The cutoff goes in there. I set it at 0.18 and wrote both measurements into the
           code above it, so the next person to read it sees where the number came from.
```

`pull` — *"Calibrate a threshold on the corpus you will actually run against, using queries that
actually fail. A threshold tuned on clean examples is tuned for a world you don't ship into."*
label: The lesson I'd most want you to take

## Section: Why not something cleverer than a hardcoded number

`p` — Every adaptive rule I tried is top-k in disguise. The popular one is the **elbow method**:
sort the scores, find the biggest drop, cut there. On a real set of mine — 0.411, 0.073, 0.036,
0.030, 0.024, 0.021 — the biggest drop is right at the top, so the elbow throws away the second
chunk, which genuinely answers the question. The gap being widest didn't make it the right place to
cut; what matters is what sits on either side of it.

`p` — *"Keep anything within 15% of the top"* works fine until every candidate is junk, and then it
keeps the best junk. *Mean plus one standard deviation* is worse: one strong hit drags the mean up
and cuts off the second-best correct answer. They share one flaw — each defines the boundary from
the candidates in front of it, so **there is always something above the line**. None of them can
ever return zero, which is the one behaviour I was building.

## Section: The upgrade improved my retrieval score by exactly zero

`p` — I had built a test suite first: real questions, and which file should answer each, scored on
whether the right file came back and how highly it ranked.

`stats`
- Mean reciprocal rank, before reranking → **0.93**
- Mean reciprocal rank, after reranking → **0.93**

`p` — Nothing. Every guide calls reranking the biggest single quality jump in RAG, and on my corpus
it moved the number not at all. That result is correct and worth understanding: a reranker earns its
reputation by dragging a correct chunk from position nine up to position one, and at 0.93 out of
1.00 plain cosine was already putting the right file first almost every time. Six files on clearly
different topics is not a hard retrieval problem. **There was nothing buried.**

`p` — I shipped it anyway, because it fixed something the suite was never measuring. And that is the
part I would underline: a test suite tests the things you thought of. Mine was seven for seven,
green, while the bot could not name my employer. That question is now a permanent row in it — the
first one I didn't invent.

`p` — One more result I liked. Ask *"has he worked with Kubernetes?"* and the top chunk, at **0.834**
— the highest score anything got that day — is the one that says he hasn't. Relevance is not
agreement. Saying no *is* answering, and the system now scores it that way.

## Section: What it costs

`stats`
- Added latency → **~0.9 s** per question (0.73 s → 1.64 s inside the service)
- Added cost → **$0.001** per query, priced per search rather than per document
- End-to-end, warm, measured live → **~8.5 s** ✅
- Cold start on the free tier → **22.5 s** ✅

`p` — Widening the candidate pool from 2 to 20 costs the same, because the price is per search, not
per document. For a bot that stops improvising at recruiters, that is not a difficult trade.

`p` — One thing that nearly went wrong on the way out: the reranker used a library that was in my
local environment only because an unrelated experiment had installed it. It was never in
`requirements.txt`. On the server it would have failed at import — and because the import chain runs
through the app's entry point, **the entire API would have failed to boot**, not just the new
endpoint. *Works on my machine* and *ships* are two different claims, and the gap between them is
usually a dependency you never chose.

## Section: What it still cannot do

`list`
- **The cutoff is a constant.** 0.18 is right for this corpus and this reranker, and it is a lie the
  moment either changes. It has to be re-derived, which is why the two measurements it came from are
  written above it in the code.
- **Search is still meaning-only.** Ask for an exact term — `ClickHouse`, `PM2`, `Cashfree` — and a
  meaning-based search can return things that are merely *about* that area. Hybrid search is next.
- **It is the slowest version.** About 0.9 s more per question, and still no streaming, so the wait
  is silent.
- **Reranking bought no ranking improvement here.** On a bigger, more confusable corpus it would.
  On 127 chunks across six distinct topics it earns its place on abstention alone, and I would
  rather say that than claim a number I didn't measure.
- **The suite is still small.** Seven questions, one of them harvested from a real failure. Every
  new failure a visitor finds becomes a row that can never silently break again — which is the
  actual reason the article asks people to try to break it.

🎨 Optional figures (the six PNGs exist as `01-cosine-cone`, `02-bi-vs-cross`, `03-two-scales`,
`04-the-gap`, `05-elbow-trap`, `06-way2news` in `~/Desktop/spidy-v3-figures/` **on the other
laptop** — declare them without `src` until the files are on the machine that builds).
