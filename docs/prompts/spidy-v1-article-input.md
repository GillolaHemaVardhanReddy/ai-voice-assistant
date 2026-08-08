# Spidy **v1** — article input (Design D · pipeline map)

For the portfolio-repo session building `/spidy/v1`. This answers the seven questions that
session asked for, from the actual build history in `docs/progress.md`, `docs/session-log.md`
and `docs/notes/`. **Every number here was measured, not estimated.**

> **Pipeline stages v1 touched:** `Question` ● · `Retrieve` ● · `Generate` ●
> (`Rerank` and `Context` were untouched — Context arrives in v2, Rerank at 2.11.)

---

## 1 · Why this version existed

I asked a plain LLM questions about myself and watched it fail — but **not** in the way I
expected. It didn't hallucinate a fake CV. It did something worse for a portfolio: it was
**confidently useless**. It refused politely, then pushed the visitor off-site — *"you should
check his LinkedIn"* — which is the exact opposite of what a portfolio assistant is for.

The model named its own problem in its own reply: **"not in my context."** That sentence is the
entire reason v1 exists. The model didn't need to be smarter. It needed to be *given my notes*.

## 2 · What I actually changed

The whole of RAG, built from scratch — no LangChain, no framework:

- **6 text files → 127 chunks.** My notes about work, skills, boundaries, projects.
- **`embedder.py`** — one `encode()` function, text → vector. Started local
  (`all-MiniLM-L6-v2`, 384-d), ended on a hosted embedding API (`text-embedding-3-small`,
  1536-d) for reasons in §3. **Swapping engines cost 4 lines**, because everything else only
  ever talked to `encode()`.
- **`store.py`** — retrieval is one matrix multiply. `vecs @ q` over a `(127, 1536)` matrix,
  then `argsort` for the top-k. That's it. That is what a vector database is underneath.
- **`rag.py`** — retrieved chunks pasted into the prompt under a `CONTEXT:` heading, with a
  system prompt that says *answer ONLY from the context, and say so when it isn't there.*
- **Citations.** Each chunk carries its filename, so answers end `[skills.txt, boundaries.txt]`.
  A visitor can see which of my notes an answer came from.
- **`main.py`** — FastAPI. `POST /ask`, `GET /health`, a Pydantic request model, an explicit
  CORS origin list, `slowapi` rate limiting at 20/min per IP, and a **502 instead of a lie**
  when the model is unreachable.
- **Deployed** on Render's free tier, embedded as a React widget on the portfolio.

## 3 · The hard part — it didn't fit

The retrieval was the easy bit. **The hard part was making it fit in 512MB of RAM**, which is
what Render's free tier gives you. My first Docker image was **1.95GB.**

Then I did the arithmetic that redirected the entire project:

```
127 chunks × 384 dimensions × 4 bytes  =  190 KB
```

**The data was 190 kilobytes. The machinery I had shipped to produce it was 1.8 gigabytes.**
I was deploying a factory in order to deliver one envelope.

What came out of chasing that down, in order:

- **A model is not a runtime.** The weights were ~90MB. `sentence-transformers` + `torch` around
  them were ~1.8GB. I had been thinking of them as one thing.
- **`torch` had two doors.** Removing it from `requirements.txt` wasn't enough — the Dockerfile
  pulled it back in by a second route. A dependency you removed once may not be removed.
- **`sympy`, 57MB.** A symbolic-algebra library, in a web service that does no algebra, pulled
  in transitively by the ONNX runtime. I only found it by running `du` *inside* the container.
- **Build time is not run time.** The 127 chunks never change between requests, so chunking and
  embedding them at boot was pure waste. `build_index.py` runs once, offline, and writes
  `index.npz`; the server just `np.load`s it.
- **`float64 → float32`** shrank the index from 1.7MB to 949KB and changed **zero digits** of any
  score — the provider had already rounded to float32 before sending it.
- **`allow_pickle=False`**, because a `.npz` can carry pickled objects and unpickling executes
  code. My own index file is a supply chain.

**Result: 1.95GB image → 347MB on disk / 72.6MB compressed. Runtime memory 625MB → 63.4MB.
Build time 1.8 seconds.** Same 127 chunks, same answers — I verified all 12 retrieval scores
matched the pre-change baseline to three decimals before I trusted a single byte of it.

**The bug I'd tell a recruiter about, though, was smaller and worse.** Early on the bot answered
in the first person — *"I built the analytics platform"* — because nothing in the prompt told it
who it was. It was quietly impersonating me on my own website. The fix was one paragraph of
system prompt: *you are Spidy, you are NOT Hemavardhan, always third person.* The lesson stuck
harder than the 1.9GB one: **the failure that scared me wasn't a crash, it was the system
confidently doing something wrong and nobody noticing.**

## 4 · Proof

Same question, before and after retrieval. *(Suggested before/after block — screenshots to follow.)*

| | Question: **"Does he have experience with MongoDB?"** |
|---|---|
| **Before v1** | Deflects — no knowledge of me, suggests checking elsewhere. Polite, useless, sends the visitor away. |
| **After v1** | *"Hemavardhan has used MongoDB in college and side projects, but not in production. His production database experience is with MySQL, ClickHouse, and Redis."* `[boundaries.txt]` |

The second answer is not just correct — it's **correct about a limitation**, sourced from a file
I wrote precisely so the bot would never oversell me. And it names the file it used.

**Measured on the live deployment:** cold start 22.5s (free tier sleeps) · warm `/ask` 3.4s ·
embedding cost ~$0.0004 per 1,000 tokens.

## 5 · What it still can't do

- **No memory.** Every question is answered in isolation. Ask *"does he know MongoDB?"* then
  *"so he knows it?"* and the second question means nothing to it. → **fixed in v2**
- **Retrieval is blind to the conversation** even once the model has history — it only ever
  embeds the raw sentence you just typed. → **fixed in v2 with query rewriting**
- **Citations are filenames.** `[boundaries.txt]` is honest but not friendly, and it will be
  actively wrong once answers are spoken aloud.
- **Doesn't really stream.** The widget appears to type, but the answer is buffered first — the
  perceived wait is far longer than the API's own 3.4s.
- **Exact terms get blurred.** Ask for a specific product or library name and meaning-search can
  return things that are merely *about* that area. → **the case for hybrid search, later**

## 6 · Screenshots / diagrams to include

1. **The 190KB arithmetic**, as a single line of text on its own — `127 × 384 × 4 bytes = 190 KB`
   next to `image: 1.95GB`. That contrast is the article.
2. **Before/after retrieval hits** — the top-5 chunks with their cosine scores for one question.
3. **The pipeline strip** — Design D's own component, with `Retrieve` lit.
4. **Size timeline** — 1.95GB → 751MB → 347MB → 63.4MB RSS, four bars.
5. *(optional)* `docker history` / `du` output showing `sympy` at 57MB — the moment of finding it.

## 7 · Pipeline stage tag (Design D config)

```
stages: [question, retrieve, generate]
primary: retrieve
```

---

### Tone note for whoever writes the copy

The interesting thing about v1 is **not** "I built a RAG bot" — everyone has. It's that the
retrieval was 40 lines and the deployment was three days, and the article should be honest about
that ratio. The engineering story is **190KB of data behind 1.8GB of machinery**, and noticing.
