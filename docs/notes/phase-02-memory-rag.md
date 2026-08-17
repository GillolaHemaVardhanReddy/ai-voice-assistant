# Phase 2 — MEMORY & RAG 🧬 (revision notes)

**What you're building:** memory that *retrieves* instead of *replaying* — the fix for Phase 1's snowball cost, and the thing that lets a bot answer questions about **you**.
**The one sentence:** *meaning becomes geometry — text → vector → nearest neighbours → paste the winners into the prompt.*

⚡ **60-second revision:** read only the 💡 lines. 🧮 = math sub-atom.

---

## 2.0a–2.0e — Python OOP (via JS)

💡 **Idea:** A Python `class` is a JS `class` with one difference you must never forget: **`self` is written out explicitly** as the first parameter of every method.

💻 **The map:**
```python
class Memory:
    def __init__(self, system_prompt="..."):   # = constructor()
        self.history = [...]                   # = this.history
    def add(self, role, content):              # `self` declared, auto-passed
        self.history.append(...)
```
| JS | Python |
|---|---|
| `constructor()` | `__init__(self)` |
| `this` | `self` (declared, not implicit) |
| `new Memory()` | `Memory()` — no `new` |
| `module.exports` / `import` | `from memory_class import Memory` |

⚠️ **Gotcha — the `__main__` guard:** any code at the *top level* of a file runs when that file is **imported**, not just when it's run. That's why `similarity.py` prints `puppy vs retriever` at startup — it's `cosine.py`'s demo code firing on import. The fix:
```python
if __name__ == "__main__":
    ...demo code...
```
Read it as: *"only if I am the file being run directly."*

✅ **2.0e:** `Memory` now drives the chat loop (`learn/phase2/chat_bot_v2.py`) — and you added `pop()` yourself, unprompted, for the error-recovery case.

❓ **Self-test:** Why does `def add(self, role, content)` take three params but you call `mem.add("user", "hi")` with two?
<details><summary>answer</summary><code>mem.add(...)</code> is sugar for <code>Memory.add(mem, "user", "hi")</code> — the instance is passed as the first argument automatically. Python makes visible what JS hides inside <code>this</code>.</details>

---

## 2.1 / 2.1c — Feeling the failure

💡 **Idea:** Ask the bot about **you** and it fails — but not the way everyone predicts.

⚠️ **The surprise (worth remembering):** Haiku 4.5 **did not hallucinate**. It refused, even under leading questions ("how many years of React?", "hardest project?"). The real failure was: *confidently useless, and it deflects recruiters off-site.* The model named its own fix — **"not in my context."** That sentence is the entire thesis of RAG.

📌 **Decision recorded:** Haiku 4.5 = strong honesty baseline, good default for the P1.5 Recruiter Bot. **Still build the guardrail** — cheaper models later *will* fabricate.

❓ **Self-test:** Fine-tuning also teaches a model new facts. Why is RAG the right tool here?
<details><summary>answer</summary>Facts change. RAG updates by editing a text file; fine-tuning updates by retraining. RAG also lets you cite the source and swap the underlying model freely. Fine-tuning teaches <em>style and behaviour</em>; RAG supplies <em>facts</em>.</details>

---

## 2.2 🔧 — Vectors & the dot product

💡 **Idea:** A vector is a list of numbers = an arrow in space. The **dot product** is an "agreement score": multiply matching slots, add it all up.

💻 **The line that matters:**
```python
np.dot(a, b)      # = a JS: for(i) sum += a[i]*b[i]
```

📊 **Your hand-computed numbers:** `a·b = 32`, `a·a = 14` for `a=[1,2,3]`, `b=[4,5,6]`.

⚠️ **Gotcha — the length bug:** raw dot product **rewards long arrows**. Double a vector's length and its dot product doubles, even though its *direction* — its meaning — didn't change at all. This bug is exactly what cosine exists to fix.

❓ **Self-test:** Two vectors point in identical directions but one is 10× longer. What does the dot product say, and what *should* the answer be?
<details><summary>answer</summary>Dot product reports a number 10× larger — as if they're "more similar". They're not; they're <em>identically</em> similar. Direction is meaning, length is loudness.</details>

---

## 2.2a 🧮 — Magnitude / norm

💡 **Idea:** The norm is the arrow's **length** — Pythagoras in n dimensions.

💻 **The line that matters:**
```python
np.linalg.norm(a)      # == math.sqrt(np.dot(a, a))
```

📊 `[1,2,3]` → `√14 ≈ 3.742`.

❓ **Self-test:** Why is `norm(a)` the same as `sqrt(a·a)`?
<details><summary>answer</summary><code>a·a</code> multiplies every component by itself and sums: <code>1²+2²+3²</code>. That's the inside of Pythagoras. Square-root it and you have the length.</details>

---

## 2.2b 🧮 — Normalizing → unit vectors

💡 **Idea:** Divide a vector by its own length and you get a **unit vector** — direction only, loudness thrown away.

💻 **The line that matters** (`learn/phase2/vectors.py`):
```python
a / np.linalg.norm(a)
```

🧪 **You proved it yourself:** `[1,2,3]` and `[4,8,12]` → **the same unit vector**. Different lengths, one direction, one meaning.

⚠️ **Vocabulary trap you fell into:** a **unit vector** is not a **bias**. Unit vector = direction (÷ its own length). Bias = a number added after a weighted sum inside a neuron — you meet that properly at **7.0**.

❓ **Self-test:** What's the norm of a unit vector, always?
<details><summary>answer</summary><code>1.0</code>. That's the definition, and it's what makes the next atom collapse.</details>

---

## 2.3a–2.3c — First real embeddings

💡 **Idea:** A trained model turns **any** text into a fixed-size vector. `all-MiniLM-L6-v2` → **384 numbers**, always — one word or one paragraph.

💻 **The line that matters** (`learn/phase2/embeddings.py`):
```python
model = SentenceTransformer("all-MiniLM-L6-v2")
vec = model.encode("I know React and Node.js")   # vec.shape == (384,)
```

💰 **Cost:** free, local, ~90 MB one-time download. No API, no per-call charge. (Installing `sentence-transformers` also pulled in `torch` for Phase 7 and `transformers` for Phase 8 — free groundwork.)

⚠️ **Gotcha — the shortcut you found:** `np.linalg.norm(vec) == 1.0`. The model has a `Normalize` module at the end, so it **already returns unit vectors**. Therefore **cosine collapses to a plain dot product** — the division by lengths is dividing by 1 × 1. Free speed, and it's why a whole vector search can later become one matrix multiply.

❓ **Self-test:** A 2-word input and a 200-word input both give `(384,)`. Where did the extra information go?
<details><summary>answer</summary>It was <strong>averaged in</strong> — see the pooling card (2.6c). Longer text doesn't get a longer vector, it gets a more <em>blended</em> one. Which is exactly why RAG chunks documents instead of embedding whole files: blend too much and every chunk drifts toward the same bland average.</details>

---

## 2.4 🧮 — Cosine similarity

💡 **Idea:** Cosine = the dot product **with the lengths divided out** — pure direction agreement. `1` = same way, `0` = perpendicular, `−1` = opposite.

💻 **The line that matters** (`learn/phase2/cosine.py` — now an importable module):
```python
def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

📊 **Your toy result** (2D "dogs vs money"): puppy/retriever `0.998`, puppy/stocks `0.165`.

🖼️ **The picture that made it land** (after the algebra failed): two arrows → the angle between them → one number. The dot product is an **AND-gate agreement score** — for each dimension, "do we both have a lot of this?" Big only when *both* are big. Lengths get divided out so only direction survives.

⚠️ **Teaching note to yourself:** you correctly guessed the collapse-to-dot-product from the picture, then got lost when it was proved with algebra first. **Picture → numbers → formula → code.** Never symbols first.

❓ **Self-test:** In a 384-dim space, what would a cosine of exactly `0` mean about two sentences?
<details><summary>answer</summary>Perpendicular — literally <em>zero</em> shared direction, no dimension where both are meaningfully active. And per the next card, you will basically <strong>never see this</strong> with a real embedder.</details>

---

## 2.5 — Similarity on real text

💡 **Idea:** Embeddings capture **meaning, not spelling**.

📊 **The headline result:** `cat`/`kitten` = **0.788** · `cat`/`car` = **0.463**. Two letters apart wins nothing; meaning wins everything. Any string-matching approach gets this exactly backwards.

⚠️ **The catch that changes your architecture:** the floor is **not 0**. Any two random English words land ~0.3–0.5. `0.463` for `cat`/`car` is *not* "somewhat related" — it's the **baseline**.

❓ **Self-test:** Why would `SELECT ... WHERE text LIKE '%cat%'` fail the job cosine just did?
<details><summary>answer</summary><code>kitten</code> contains no "cat" and would score zero, while <code>catalogue</code> and <code>concatenate</code> would score as perfect matches. String search matches <em>characters</em>; embeddings match <em>meaning</em>. This is the entire reason vector search exists.</details>

---

## 2.6a 🧮 — Anisotropy: the cone

💡 **Idea:** Embeddings don't fill the space. They all lean into a narrow **cone**, so *everything* looks somewhat similar to everything.

💻 **The experiment** (`learn/phase2/similarity.py`): 5 maximally-unrelated words — `cat`, `car`, `banana`, `democracy`, `hydrogen` — all 10 pairs.

📊 **Result:** floor **`0.186`**, ceiling **`0.463`**. **Not one pair near 0.** In a space that *could* give you `−1` to `1`, real words use a band about 0.28 wide.

📊 **But the ranking is semantically real:** `car`/`hydrogen` `0.401` > `car`/`democracy` `0.354`. ⛽ The model knows fuel.

🏆 **THE RULE OF THIS PHASE:**
> **Absolute cosine lies. Ranking tells the truth. → Always top-k, never a threshold.**

A hard-coded `if score > 0.7` will silently return nothing on some queries and everything on others, because the whole band shifts with the query. **Rank and take the best 3.** (Re-flagged at 2.7; centering's real value gets *measured*, not argued, at 10.4.)

❓ **Self-test:** Your RAG retrieves with `if score > 0.5: include`. Describe the bug in production.
<details><summary>answer</summary>Query-dependent and invisible. Common/generic queries push everything above 0.5 → you stuff the prompt with junk and pay for it. Unusual queries push everything below → the bot says "I don't know" while the correct chunk sits at 0.48. Same code, opposite failures, no error message either time.</details>

---

## 2.6b 🧮 — Centering: why the cone can be subtracted

💡 **Idea:** Average all your vectors → that mean **is** the shared junk. Subtract it, and only the differences remain.

💻 **The lines that matter:**
```python
mean_vec = vecs.mean(axis=0)     # the centre of the cone: "the average English word"
centered = vecs - mean_vec       # broadcasting: one vector subtracted from all rows
```

📊 **Result:** every one of the 10 pairs went **negative** (`−0.136` → `−0.361`). Average = **`−0.2484`**.

✏️ **Why all of them go negative — the theory:** once vectors are centered, their sum is zero, so they *must* pull against each other. For `n` maximally-spread vectors the average pairwise cosine is exactly **`−1/(n−1)`**.
- n = 2 → `−1` (two points on a line, opposite by force)
- n = 3 → `−0.5` (a triangle, 120° apart)
- **n = 5 → `−0.25`** … and you measured **`−0.2484`**. ✅

🖼️ **The picture:** 5 kids in a field, flag planted at their balance point. If they all pointed the same way, the flag wouldn't *be* the balance point. Disagreement is mandatory.

⚠️ **The insight, stated properly:** cosine measures direction **from an origin** — so the origin is not a neutral bystander. Moving it changes every angle. It does **not** change the distances between points, and it does **not** destroy real similarity: `cat`/`car` stayed near the top and `banana`/`democracy` at the bottom *after* centering. **The numbers all moved; the order survived.** Which is the third independent proof of the top-k rule.

❓ **Self-test:** You center your document vectors but forget to center the query vector. What happens?
<details><summary>answer</summary>Garbage. You'd be comparing directions measured from two different origins — the angles are meaningless. Any transform applied to the corpus must be applied identically to the query. (This is the vector-search version of "train/serve skew".)</details>

---

## 2.6c — Pooling: why a sentence gets *one* vector

💡 **Idea:** The transformer really does produce **one vector per token**. The last step, **pooling**, averages them into one.

💻 **The line that matters:**
```python
toks = model.encode(text, output_value="token_embeddings")   # (n_tokens, 384)
manual = toks.numpy().mean(axis=0)                           # → (384,)  ...then normalize
```

🔗 **The connection:** this is the *same* `.mean(axis=0)` you used for centering — different axis meaning.
- **You** averaged across **5 words** → the average English word (and *subtracted* it).
- **The model** averages across **9 tokens** → the average meaning of the sentence (and *keeps* it — that IS the embedding).

⚠️ **Consequence for RAG:** averaging blurs. A 2,000-word document pooled into one vector is mush — every long document drifts toward the same bland centre. **This is the real reason we chunk.**

📦 **Still boxed, opens at:** how a token gets its numbers → **7.7** (it's a *lookup table*, one row per token — you build one). How those numbers become context-aware → **7.8–7.12** (attention). Where the trained numbers came from → **7.13** + Phase 8.

❓ **Self-test:** Two documents, identical wording, one is 10× longer (it repeats itself). Similar vectors or different?
<details><summary>answer</summary>Very similar — the mean of repeated content is roughly the same mean. Pooling is scale-invariant that way. Length only shifts the vector when it introduces genuinely <em>new</em> content to average in.</details>

---

## 2.6 — The vector store ✅ (chunk → embed → rank)

💡 **Idea:** A vector store is not a database. It's *a list of chunks + a matrix of their vectors + a sort.* Twelve lines.

💻 **The whole engine** (`learn/phase2/store.py`, data in `learn/phase2/about.txt`):
```python
text   = open("learn/phase2/about.txt").read()
chunks = [c.strip() for c in text.split("\n\n") if c.strip()]   # 1. chunk
vecs   = model.encode(chunks)          # 2. embed → (n_chunks, 384), one row per chunk

def search(query, k=2):                # 3. rank
    q = model.encode(query)
    scored = [(cosine(q, vecs[i]), chunks[i]) for i in range(len(chunks))]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return scored[:k]
```
`model.encode()` takes a **list**, not just a string → you get a matrix back. `key=lambda pair: pair[0]` is JS `pair => pair[0]`.

🧩 **Why chunk at all:** pooling averages (2.6c). One vector for a 10-idea document sits at the **centre of all ten ideas** — it matches every question equally, so you can't pick the topic. *(Your own words, and they're the best statement of it in these notes.)* One vector per idea, not one per file.

⚠️ **Gotcha — chunking has no brain.** `split("\n\n")` doesn't detect ideas. It **borrows the blank lines a human already typed** as a guess at where ideas end. On your file it under-split: chunk 0 held *three* ideas (identity + adaptability + architecting style), averaged into one vector. Smarter options exist (fixed-size windows with overlap; LLM-assisted splitting) — used when the cheat breaks.

🏆 **THE PROOF — your own numbers, the best result of the phase:**
```
query: "is he good at AI and language models?"
0.416  ← the CORRECT chunk (AI/LLMs)
0.284  ← the wrong chunk
```
Now compare to `cat`/`car` = **`0.463`** — two unrelated words. **Your correct answer scored LOWER than two unrelated words.** A `if score > 0.45` filter would have returned *nothing* and told a recruiter "I don't have that information," while the right paragraph sat at 0.416. Silent failure, no error, undebuggable by reading the code. **The ranking, meanwhile, was perfect.** This is the top-k rule paying for itself.

📎 **Minor, real:** your queries are *questions* and your chunks are *statements* — that asymmetry drags absolute scores down a little. Harmless; ranking absorbs it.

⚠️ **Gotcha — the floor is not a constant.** `search("what is his salary expectation?", k=1)` returned a chunk at **`0.042`** — far *below* the `0.186` floor from 2.6a. Why? That floor was measured on **single words**; this is a **question vs a paragraph**. Different text shapes sit in different parts of the cone, so **the whole band moves with the kind of text you compare**. There is no cutoff that survives contact with real data — not `0.45`, not `0.1`. Final nail in the threshold coffin.

⚠️ **The trap `0.042` sets:** it's so low that a threshold looks tempting again. Resist. It's low only because "salary" is *wildly* off-topic. A **subtle** miss ("how many years of React?") scores ~0.35 — indistinguishable from a real hit. Obvious misses are easy; near-misses are what hurt, and no threshold catches those.

❓ **Self-test:** Nothing in the file mentions salary, yet `search` returned a chunk anyway. Is that a bug in the store?
<details><summary>answer</summary><strong>No.</strong> You asked for the best 1 of 2 and got the best 1 of 2 — <code>search()</code> has no concept of "good enough" and shouldn't. Top-k always returns k; that's the contract. The missing layer is above it: a <strong>system prompt</strong> (Atom 1.5) saying <em>"answer using ONLY these chunks; if they don't contain the answer, say you don't know."</em> The retriever <em>ranks</em>; the LLM <em>judges</em>. Separation of concerns — the store is a search engine, not a judge. That guardrail lands at <strong>2.8</strong>.</details>

---

## 2.7 — Retrieval on real data ✅ (and why k > 1)

💡 **Idea:** Retrieval quality is capped by **chunk quality** — garbage chunks in, garbage ranking out. And even with perfect chunks, **rank #1 is not trustworthy.**

📄 **The data:** `about.txt` rewritten from your resume into **27 one-idea chunks** (was 2 fat ones). Your two original lines kept as their own chunk.

📊 **Result at k=1: 3 / 4 correct** out of 27 candidates (random = 4%).

⚠️ **THE FAILURE, and it's the good one:**
```
query: "what is he learning right now?"
  k=1 →  0.319  "I am eager to LEARN anything at any time..."   ← WRONG
```
The word **"learn"** is literally in the wrong chunk. Embeddings capture meaning *mostly*, not *purely* — surface form still leaks in and can outrank the actual intent. The query asked *what subject*; the winner answered *what attitude*.

✅ **The fix — same query at k=3:**
```
  0.319  "eager to learn anything..."          ← wrong
  0.248  "building an AI voice assistant..."   ← RIGHT
  0.175  "deep interest in AI and LLMs..."     ← ALSO RIGHT
```
Both correct chunks recovered. **This is why production RAG retrieves 3–5 chunks, never 1.**

🏆 **The rule, one level deeper than 2.6:**
> Don't just avoid thresholds — **don't trust rank #1 either.** The retriever's job is not to be right; it's to make sure the right chunk is *somewhere in the k you hand over*. The LLM discards the junk, and that's a job it's good at.

🔀 **Two different failures, two different fixes — do not confuse them:**
| Failure | Looks like | Fix |
|---|---|---|
| **Blended chunk** | one fat chunk wins everything, at a diluted score | better **chunking** |
| **Wrong winner** | clean chunks, but a surface-similar one outranks the right one | bigger **k** (later: reranking) |

📌 **Semantic / propositional chunking** (your question, and it's a real named technique): send the raw doc to an LLM → *"rewrite as standalone one-idea statements"* → store those. You did it by hand for the resume. It runs **once at ingest, not per query**, so it's cheap where it counts. It fixes blending; it does **not** fix wrong-winner. Built for real at 2.9.

❓ **Self-test:** Your retriever returns 5 chunks and 3 are irrelevant. Is that a failure?
<details><summary>answer</summary>No — that's the design working. Recall over precision: you optimize for "the right chunk is in there somewhere," and let the LLM filter. The real failure is the opposite — the right chunk <em>missing</em> from the k. You can't recover from that at any later stage; the LLM cannot read what you didn't send it.</details>

---

## 2.7a 🧮 — Search is ONE matrix multiply ✅

💡 **Idea:** A matrix isn't a new concept — it's **rows you already had, stacked**. Matrix × vector runs the same dot product against *every* row at once. Your 27-chunk search is one instruction, not a loop.

🖼️ **Picture:** stop seeing 27 separate arrows in a list. See one block: 27 rows, one arrow per row. Feed it a question-arrow → get a column of 27 answers back.

🔢 **By hand** (2D: frontend-ness, database-ness). Question `[1, 0]` = *"do you know React?"*
```
row 0  [ 1  , 0  ]   →  1×1 + 0×0   = 1.0
row 1  [ 0  , 1  ]   →  0×1 + 1×0   = 0.0
row 2  [ 0.6, 0.8]   →  0.6×1 + 0.8×0 = 0.6
```
Three scores, one operation. That's the whole of matrix × vector.

✏️ **The shape rule** — the only rule, and 90% of matrix bugs are breaking it:
```
(m × n) @ (n,) → (m,)
"m rows each n long, times one arrow of length n, gives m answers"
        m = 27 chunks     n = 384 dimensions
```
The inner `n`s must match; they meet and cancel. The outer number is what you're left with.

💻 **The code — no loop anywhere:**
```python
vecs = model.encode(chunks)          # (27, 384) — ONE batched call, not a list comprehension
def search(query, k=3):
    q = model.encode(query)
    scores = vecs @ q                # (27,384) @ (384,) → (27,)
    top = np.argsort(scores)[::-1][:k]
    return [(scores[i], chunks[i]) for i in top]
```
`@` = matrix multiply. `np.argsort` returns the **indices** that would sort ascending (positions, not values); `[::-1]` flips to descending; `[:k]` takes the top.

⚠️ **Gotcha #1 — `@` is only cosine because the vectors are unit-length.** Dividing by `1 × 1` does nothing, so the division vanishes. **This is a design choice of MiniLM, not a law of embeddings.** Swap in a model that doesn't normalize and `vecs @ q` silently ranks wrong — no error, just bad answers. **Habit: print `np.linalg.norm(vec)` once for any new model.** If it isn't 1.0, normalize yourself or use the full `cosine()`.

🔢 **Why length corrupts ranking — the proof.** Question `q = [1, 0]`:
```
row 0 = [1, 0]   perfect direction, length 1  →  raw dot = 1
row 1 = [6, 8]   worse direction,  length 10  →  raw dot = 6   ← WINS, wrongly
proper cosine:      1/1 = 1.0   vs   6/10 = 0.6                ← correct order restored
```
The wrong chunk beat the perfect one 6-to-1 purely for being long. **Normalizing makes everyone speak at the same volume so only content decides.**

⚠️ **Gotcha #2 — build it as a matrix, not a list.** `[model.encode(c) for c in chunks]` gives a *list of arrays*; NumPy quietly coerces it so `@` still works, but it's 27 separate model calls. `model.encode(chunks)` is **one batched call** → a real `(27, 384)`. Batching is the biggest speed lever in ML inference; you meet it again in Phase 7.

🔗 **Why this matters beyond speed:**
1. **This is what a vector database IS.** Pinecone, FAISS, pgvector — under the marketing it's `vecs @ q` over a big matrix, plus tricks to avoid touching every row. Your 12 lines are the real thing at small scale.
2. **This is the operation Phase 7 is made of.** Attention, every transformer layer, all of training = matmuls. You earned matrices by *needing* one.

❓ **Self-test:** `(27, 384) @ (384,)` works. What does `(27, 384) @ (27,)` do?
<details><summary>answer</summary>Crashes — shape mismatch. The inner dimensions must agree: the matrix's row-length (384) must equal the vector's length. 27 is the count of chunks, not the size of a vector; they aren't interchangeable just because both are numbers. Reading the shapes out loud ("27 rows of 384, times one arrow of 384") is how you catch this before running it.</details>

---

## 2.8 — RAG ✅ (the payoff)

💡 **Idea:** **R**etrieval **A**ugmented **G**eneration = your `search()` + Phase 1's API call + a string join. **There is no RAG library, no RAG model, no RAG API.** It's a formatting step between two things you already owned.

💻 **The whole of it** (`learn/phase2/rag.py`):
```python
from store import search               # ← imports chunking + embeddings + matrix search

def answer(question, k=5):
    hits = search(question, k)
    context = "\n\n".join(chunk for score, chunk in hits)
    m.add("user", f"CONTEXT:\n{context}\n\nQUESTION:\n{question}")   # BEFORE the API call
    # ...stream the reply, accumulate into s...
    m.add("assistant", s)
```

🛡️ **The guardrail — the most important string in the file:**
```
Answer ONLY using the CONTEXT below.
If the CONTEXT does not contain the answer, say you don't have that information.
Never guess or invent details.
```
**It works:** *"what is his salary expectation?"* → *"I don't have that information."* The retriever still returned chunks (top-k always returns k), and the **LLM** refused. Retriever ranks, LLM judges — the separation of concerns from 2.6, now running.

🐛 **Five bugs found and fixed live — all five are classics:**
| Bug | Symptom | Fix |
|---|---|---|
| `from memory import Memory` | `ModuleNotFoundError` | file is `memory_class.py` (phase1's `memory.py` is a *script*) |
| `m.add({"role":..., "content":...})` | `TypeError: missing 1 required positional argument` | signature is `add(self, role, text)` — it builds the dict |
| `m.add(...)` **after** the API call | **silent** — model never sees the question | add the user message **before** `create()` |
| `m.add("assistant", delta)` | saves the last fragment (`"."`) | use the accumulated `s` — the 1.8 streaming gotcha |
| `while 1:` above the `__main__` guard | chat starts on import; test block unreachable | put the loop inside the guard |

⚠️ **`answer()` streams and returns `None`** → `print("A:", answer(q))` prints `A: None` after the text. Either `return s` or don't wrap the call.

⚠️ **Memory + RAG = the snowball is back.** Storing `CONTEXT + question` every turn means 5 chunks of resume in history *forever*. RAG was supposed to cure the 1.6 snowball; naive chat-memory reintroduces it. Fix: keep only the **conversation** in history, attach fresh context to the newest question each turn. **⬜ still owed.**

💰 **Cost:** ~5 chunks ≈ 350 input tokens + short answer ≈ **$0.0002/question** on Haiku 4.5. Embeddings free and local. 1,000 recruiter questions ≈ **20 cents**.

❓ **Self-test:** Your RAG bot gives a wrong answer. What do you check first?
<details><summary>answer</summary><strong>The retriever, always.</strong> Print the top-k for that query before blaming the model. In every failure this session the LLM behaved perfectly and faithfully reported what it was handed — it cannot read what you didn't send it. "Bad RAG answer" is almost always "the right chunk wasn't in the k."</details>

---

## 🔬 The three retrieval failure modes (all three hit you, on your own data)

This table is the most useful thing in these notes. Diagnose before you fix.

| # | Failure | What you saw | Fix |
|---|---|---|---|
| **1** | **Blended chunk** — one chunk holds many ideas, its vector is their average | old `about.txt`: one fat chunk won everything at a diluted score | **better chunking** — one idea per chunk |
| **2** | **Wrong winner** — clean chunks, but a surface-similar one outranks the right one | *"what is he learning?"* → *"eager to **learn** anything"* at rank 1 | **bigger k** (later: reranking) |
| **3** | **Vocabulary mismatch** — the right chunk *answers* the question but shares no words or framing with it | *"what does he do at his current job?"* → **none** of the payments chunks in the top 5; sports committee ranked #2 | **query rewriting, hybrid search, chunk context-prefixes, metadata** — neither k nor chunking fixes this |

⚠️ **Long-chunk dilution, measured:** the chunk beginning *"I published an open-source npm package called Acharya"* ranked **5th** (`0.210`) for *"has he published anything open source?"*, losing to a chunk about **Jest and Postman** (`0.340`). Why: the Acharya chunk was ~60 words, so the "open source" signal was averaged against 50 words of architecture jargon; in the short tooling chunk, *"npm including publishing my own packages"* was a **big fraction** of its average. Kira didn't make the top 8. **Splitting headline from detail + `k=5` fixed it.**

> **On a short query, a short chunk with one relevant sentence beats a long chunk with one relevant sentence.** Pooling dilution (2.6c), costing real answers.

---

## 2.8a — Contextual retrieval ✅ (fixing vocabulary mismatch)

💡 **Idea:** The chunk *"I own the payments subsystem of Vedamandir…"* never says **job**, **work**, or **Way2News** — so it can't be found by *"what does he do at his current job?"* **The chunk lost the context it was written inside.** On the resume, "this is under the Way2News heading" was carried by the *layout*; chunking threw the layout away. So put the context back into the text **before embedding it**.

🔑 **THE TRICK — the most reusable move in this phase:**
> **You can embed one string and display another.** Nothing says the text you search over must be the text you show.
```
embed:   "Current job at Way2News: I own the payments subsystem of Vedamandir..."
display: "I own the payments subsystem of Vedamandir..."
```
The vector gains the missing vocabulary; the LLM still gets clean prose. Real named technique: **contextual retrieval**.

💻 **The code — two parallel lists, built in one loop:**
```python
chunks, embed_texts, section = [], [], []      # chunks = SHOW, embed_texts = SEARCH
for block in text.split("\n\n"):
    block = block.strip()
    if not block: continue
    if block.startswith("#"):
        section = block.lstrip("# ").strip()   # remember the heading, don't store it
    else:
        chunks.append(block)
        embed_texts.append(f"{section}: {block}")
assert len(chunks) == len(embed_texts)         # cheap insurance — see the bug below
vecs = model.encode(embed_texts)               # search over context-rich text
# search() still returns chunks[i] — clean text out
```

⚠️ **The prefix must VARY per chunk.** A prefix identical on every chunk shifts all vectors the same direction — and a constant added to everything barely changes the **ranking**. That's 2.6b (centering) running backwards: *same shift for everyone = no new information.*

📊 **Result — all three failure modes fixed, measured:**
| Query | Before | After |
|---|---|---|
| *"what does he do at his current job?"* | sports committee at #2, **zero** payments chunks in top 5 | payments + Cashfree + admin console → correct answer |
| *"what is he learning right now?"* | *"eager to **learn** anything"* won (0.319) | both AI chunks tied at **0.494** |
| *"has he handled payments at scale?"* | ok | all three payments chunks, ranks 1–3 |

⚠️ **Scores went UP (0.419→0.466, 0.319→0.494) — do NOT read that as "better."** The whole band shifted, *including* for wrong chunks, because the headings are written like the questions people ask. **The proof it worked is that the ranking changed to the right chunks**, not that the numbers grew. (Opposite risk: if a heading dominates its chunks' vectors, everything in that section looks alike and you lose discrimination *within* the section. Keep headings specific and short.)

🐛 **The bug that cost a debugging round — parallel-list drift:**
```python
chunks = [c.strip() for c in text.split("\n\n") if c.strip()]   # ← old line, LEFT IN: 45 blocks
...
    chunks.append(block)                                        # ← then appends 33 more
```
`chunks` had ~78 entries, `embed_texts` had 33. `search()` scored `embed_texts[i]` but printed `chunks[i]` — **different chunks.** Symptom: *"does he know databases?"* returned the **Acharya** chunk at 0.479, and `#` headings surfaced as content.

> **No error. No crash. Both are lists, every index is in range — Python cheerfully returns the wrong string.** The only symptom was answers that made no sense. Diagnosed less carefully, the conclusion would have been "embeddings are unreliable" and the hunt would have gone in the wrong direction entirely.
>
> **Two parallel lists must be built in the same loop, in the same order — or add `assert len(a) == len(b)` and turn a silent wrong answer into a loud crash.** (Same discipline as idempotent webhooks and the zero-double-charge ledger — applied to indices.)

❓ **Self-test:** You prefix every chunk with `"Hemavardhan's profile: "` — same string on all of them. Does retrieval improve?
<details><summary>answer</summary>Essentially no. An identical prefix shifts every vector in the same direction; ranking depends on *relative* angles, so a shift shared by all barely reorders anything. It's the centering lesson (2.6b) in reverse. The prefix has to <em>distinguish</em> chunks — it must vary — to add information.</details>

---

## 2.9a — one file → a folder (+ `assert` as a tripwire)

💡 **Idea:** A real knowledge base is a **folder**, not a file. Loop over it with `glob`, and carry a **third** parallel list — `sources` — so every chunk knows which file it came from. That's provenance, and it's what makes citations possible later.

💻 **The lines that matter:**
```python
import glob
files = sorted(glob.glob("learn/phase2/notes/*.txt"))   # sorted() = stable order every run

for file in files:
    text = open(file, "r").read()
    section = ""
    for block in text.split("\n\n"):
        ...
        else:
            chunks.append(block)                        # → shown to the LLM
            embed_texts.append(f"{section}: {block}")   # → what we embed
            sources.append(file.split("/")[-1])         # → the citation

assert len(chunks) == len(embed_texts) == len(sources)
print(len(files), "files →", len(chunks), "chunks")     # 6 files → 127 chunks
```

⚠️ **Gotcha 1 — read the FIRST anomaly, not the traceback.** A `notes.*.txt` typo (dot for slash) matched nothing → `files` empty → `vecs` shape `(0,)` → the crash surfaced 26 lines later inside `vecs @ q` as a *matmul dimension error*. Line 35 was innocent. The actual diagnosis was the line you printed yourself: `0 files → 0 chunks`. **A crash happens downstream of where things went wrong.**

⚠️ **Gotcha 2 — `assert` checks the invariant you named, nothing more.** With the empty folder it **passed**: `0 == 0 == 0` is perfectly consistent. It guards against *drift*, not against *wrong*.

⚠️ **Gotcha 3 — parallel appends must live in the SAME block.** `sources.append(file)` sat in the outer (per-file) loop while the others sat in the inner (per-chunk) `else` → 6 vs 127. The `assert` fired instantly. **Compare to 2.8a, where the identical drift bug had no assert: no error, no crash, just nonsense answers and a whole debugging round lost.** One line converted a silent wrong answer into a loud, immediate crash.

🏆 **`boundaries.txt` paid off:** *"does he know databases?"* → rank 1 `MySQL/ClickHouse/Redis` (0.544), rank 2 **`MongoDB only in college and side projects, not in production`** (0.531). The honest limit is retrieved *alongside* the strength, so the LLM physically cannot over-claim — the correction is in its context. **Negative facts are retrievable facts.**

⚠️ **Scores rose again (0.5–0.58 vs 0.25–0.42) — fifth reminder: that is NOT "better."** Richer chunks + question-shaped headings lift the whole band. The proof is that *"what is he learning right now?"* finally ranks both AI chunks at #1/#2 instead of the *"eager to **learn**"* surface-form trap from 2.7.

❓ **Self-test:** Your `assert` passes. Does that mean retrieval is working?
<details><summary>answer</summary>No. It only means the three lists are the same <em>length</em>. They could be the same length and still be <em>misaligned</em> (e.g. built in the same loop but one appended in a different order), and they can all three be empty. <code>assert</code> proves consistency, never correctness — you still have to read the output and check the chunks make sense.</details>

---

## 2.9b — citations (+ the hang that had no cause)

💡 **Idea:** Carry the source all the way to the answer. A claim with a receipt (`[boundaries.txt]`) is trustworthy to a recruiter — and for *you* it says instantly whether a bad answer was the **retriever's** fault or the **LLM's**.

💻 **The three lines that matter:**
```python
# store.py
return [(scores[i], chunks[i], sources[i]) for i in top]      # changed the return SHAPE → every caller breaks

# rag.py
context = "\n\n".join(f"[{src}] {chunk}" for score, chunk, src in hits)
# + SYSTEM: "Each context block starts with its source file in square brackets. End your answer with the sources you used."
```
Result: *"does he know Kubernetes?"* → *"No, he has not worked with Kubernetes or container orchestration…"* **`[boundaries.txt, skills.txt]`** ✅

⚠️ **Data ≠ instruction.** Line 22 was fixed for three whole runs before the SYSTEM line was — so the model *received* `[boundaries.txt] ...` and correctly ignored it. **Giving the model information and telling it what to do with the information are two separate jobs.** Neither one alone does anything.

⚠️ **The citation is testimony, not evidence.** The model *claims* which sources it used; nothing verifies it. The ground truth is in your own hands: `print([src for score, chunk, src in hits])`. What you compute = evidence. What it writes = testimony.

⚠️ **Changing a return shape breaks every caller silently.** TypeScript would go red instantly; Python waits for runtime and says `ValueError: too many values to unpack`. (Part of why Pydantic will feel good in Phase 9.)

🏆 **The accidental experiment: `"what is his salary expectation?"`**
At **2.8** it answered *"I don't have that information."* At **2.9** it answers *"10–16 LPA, open to discussion for the right role."* **Zero lines of logic changed** — `preferences.txt` just exists now.
> **In RAG the bot's knowledge is a DATA problem, not a CODE problem.** New capability = a new line in a text file. No retraining, no fine-tune, no redeploy. That is the entire commercial argument for RAG, in one experiment run by accident.

---

### 🐛 The 30-second hang — a debugging case study (worth re-reading)

**Symptom:** one question streamed nothing for 30–90s, no error, blank screen.

**Diagnosis, in order:**
1. `Ctrl+C` → traceback was **100% inside `httpx`/`httpcore`**, 0% inside `rag.py`. ⇒ *not stuck, **waiting*** — blocked on bytes from the network. **A hang is a stack you can't see until you interrupt it.**
2. `timeout=30, max_retries=2` → **90s**, not 30. ⇒ **`timeout` is PER ATTEMPT, not total.**
3. `timeout` still never fired. ⇒ **a read timeout protects you from silence, not from noise** — OpenRouter sends keep-alive filler while waiting on the upstream provider, and every byte resets the clock.
4. In-loop watchdog (`if time.time() - start > 20`) also never fired. ⇒ **a watchdog on the blocked thread cannot fire** — the loop body only runs when a chunk arrives, and no chunk arriving *is* the bug. (Same trap as a health-check served by the wedged process: it can only report healthy.)

**Hypotheses killed by experiment:**
| Hypothesis | Test | Result |
|---|---|---|
| the question's *content* | run it alone | ❌ instant, perfect |
| the *3rd-request position* (rate limit) | reorder the list | ❌ 3rd worked fine |

**Verdict: intermittent upstream stall. No cause in his code, no fix in his code.**
> **Not every bug has a findable cause. When the plausible hypotheses are dead and it still comes and goes, stop hunting a root cause and design for survival.** (Same reflex as dry-runs / rollbacks / go-no-go gates at work — different layer.)

**What was kept:** `try/except` around the call. **What was deleted:** the watchdog — *dead safety code is worse than none, because it makes you believe you're protected.* **Real fix deferred to FastAPI**, where it's one idiomatic line: `await asyncio.wait_for(call(), timeout=20)` — async doesn't block a thread, so the deadline can actually fire.

❓ **Self-test:** Your HTTP client has `timeout=20`. The server sends one meaningless byte every 5 seconds and never answers. How long do you wait?
<details><summary>answer</summary>Forever. A read timeout measures the gap between <em>bytes</em>, not the time to a <em>useful answer</em>. Silence trips it; noise never does. You need a wall-clock deadline on the whole operation, enforced from somewhere the blocking can't reach.</details>

---

## Sub-atom 2.10a 🐍 — Decorators (the `@` is one assignment)

💡 **Idea:** a decorator is **not syntax**. `@loud` above a `def` is *exactly* `greet = loud(greet)`, run by Python the instant it finishes reading the `def`. A decorator is just a function that takes a function and returns a replacement.

💻 **The line that matters** (`learn/phase2/decorator_play.py`):
```python
def loud(fn):
    def wrapper():
        return fn().upper() + "!!!"
    return wrapper      # the function itself — NO parentheses

@loud                   # ≡ greet = loud(greet)
def greet():
    return "hi"
```

⚠️ **Gotcha 1 — the name moves, the object doesn't die.** After `greet = loud(greet)`, `greet.__name__` is `wrapper`. But the original function is *alive*, held in `fn` inside the wrapper — provable with `greet.__closure__[0].cell_contents`. That capture-your-birthplace-variables behaviour is a **closure**; identical to JS `const old = greet; greet = () => old().toUpperCase()`.

⚠️ **Gotcha 2 — why some decorators have `()` and some don't.** `@` always takes exactly **one** thing: the function below. So `@app.get("/ask")` is not "a decorator with arguments" — `app.get("/ask")` is a **call that returns a decorator** (a *decorator factory*). It expands to:
```python
ask = app.get("/ask")(ask)
```
Same idea as Express `app.get('/ask', handler)` — hand your function to the framework so it can register it in the router table. Python just puts it on the line above instead of in the arguments.

📌 **Why now:** FastAPI (P1.5) makes you *read* decorators constantly and *write* them never — so this would have stayed fuzzy forever. Killed it before the service work.

❓ **Self-test:** `@app.get("/ask")` has parentheses; `@loud` doesn't. Why?
<details><summary>answer</summary><code>@</code> only ever takes one argument — the function underneath. <code>loud</code> is already a decorator. <code>app.get("/ask")</code> is a <em>call</em> that runs first and returns a decorator built around that path. Expands to <code>ask = app.get("/ask")(ask)</code>.</details>

---

## 2.10a — The golden question set *(started, not finished)*

💡 **Idea:** it's a **test suite for `search()`**. You've written Jest tests for Node code and **zero** tests for the retriever — every judgement about it so far has been "read the output, looks right." A test needs an expected value; for retrieval, the expected value is **which file should have answered this**.

💻 The whole thing is data, no code:
```python
# rule: a question PASSES only if EVERY file listed appears in the retrieved sources
questions = [
    {"question": "does he know kubernetes?", "file": ["skills.txt", "boundaries.txt"]},
]
```

🏆 **His improvement on the spec:** I specced *one* filename per question; he wrote a **list**. He's right — Kubernetes needs `skills.txt` (what he does know) *and* `boundaries.txt` (that Kubernetes isn't in it). A single-filename label would score a correct retrieval as a miss.

🔬 **Label at the FILE level, never the chunk level.** Atom 2.13 re-chunks everything — a label pinned to a chunk dies the moment you change the thing you're trying to measure. Filenames survive it.

⚠️ **"Every one" costs you something.** Under the strict rule, each extra file in a label makes the test harder to pass. List a file that wasn't really needed and you invent a failure — then at 2.11 you "fix" a retriever that was already fine. **Label only what's genuinely required; when in doubt, list fewer.**

⚠️ **A test suite that always passes is not a test suite.** A golden set made only of easy keyword questions scores 100% on day one and tells you nothing forever. Include the ones you already know are broken.

❓ **Self-test:** his run of `"does he know kubernetes?"` returned `boundaries.txt ×3 · projects.txt · skills.txt` — in that order. Under his own rule, is this a pass at `k=5`? At `k=3`?
<details><summary>answer</summary>k=5 → <strong>PASS</strong> (both labelled files present). k=3 → <strong>FAIL</strong>: only <code>boundaries.txt</code> made it, <code>skills.txt</code> scraped in at rank 5. Same retriever, same question, opposite verdicts — which is exactly why the pass rule has to be decided before scoring, not after.</details>

---

## 2.10.2 — the scorer, and the bug the data could never find 🐛

> ⚠️ **Correction to the card above:** that example labelled Kubernetes as `["skills.txt", "boundaries.txt"]`. Verified later with `grep -il kubernetes service/notes/*.txt` — **`skills.txt` never contains the word.** The real key is `["boundaries.txt"]`. A guessed answer key is a test rigged to fail forever.

💡 **Idea:** the golden set is data; the scorer is the runner. `learn/phase2/score.py` walks every row, calls `search(q, k=5)`, keeps **only the filenames**, and judges with the row's own `"match"` key. Output is a verdict per row **plus what actually came back** — the grade tells you *that* it broke, the payload tells you *where*.

💻 The two branches are Python built-ins — `.some()` and `.every()` with different spelling:
```python
check = [f in results for f in q["file"]]      # walk EXPECTED, ask "did it come back?"
ok = all(check) if q["match"] == "all" else any(check)
```

🐛 **THE HEADLINE — he wrote the two lists in the wrong slots, and nothing could detect it.**
`check = [f in q["file"] for f in results]` walks **results** instead. That asks *"is everything that came back expected?"* — a **purity** check. The correct line asks *"did every expected file come back?"* — a **coverage** check.

**Why five rows sailed past it:** for `"any"` the two directions are *logically identical* — both just mean "the lists overlap". The direction only matters for `"all"`, and every row was `"any"`. ⇒ **Untested branches aren't neutral. They're bugs you haven't met yet.**

**The row that exposed it,** built by him after rejecting a non-discriminating one:
```
"what databases has he worked with?"  →  ["skills.txt", "boundaries.txt"], match "all"
got:  ['boundaries.txt', 'skills.txt', 'skills.txt', 'about.txt', 'skills.txt']
```
Both expected files present ⇒ honest verdict **PASS**. His line said **FAIL**, because `about.txt` tagged along. **One extra file, and a perfect retrieval is graded as a miss.** Same disease as a bad answer key — last time in the *data*, this time in the *runner*.

🔬 **Trap 2, met again unprompted.** He first flipped the *notice period* row to `"all"` and it passed. But its results were `[faq, preferences, faq, faq, faq]` — **every returned file was already expected**, so a correct scorer and a broken one both say PASS. **No discriminating power** — the exact shape of the Session-15 memory A/B failure. He needed a row where a *non-expected* file comes back.

⚠️ **`python file.py` vs `python -m package.module`.** The launch decides `sys.path`: running the file puts *its own folder* on the path (`service` invisible); `-m` from the repo root puts **the repo root** on it (both `learn/` and `service/` visible). Second appearance of the P1.5.2a lesson.

⚠️ **`np.str_` again — a value's type comes from what made it.** `sources` lives in numpy, so `sources[i]` is `np.str_`, and `print()` hid it all through Phase 2. Fixed with `str(...)`. **Unlike `np.float32`, this one is a `str` subclass**, so the `in` checks genuinely worked — cosmetic, not fatal. Same smell, different severity.

🐍 **Syntax patched:** `any(f in got for f in wanted)` has the word `in` doing **two different jobs** — membership (`got.includes(f)`) and iteration (the loop). No `&&` because they don't combine: the loop is a **factory** producing one boolean per pass, and `any`/`all` read the stream. JS: `wanted.map(f => got.includes(f))` then `.some()` / `.every()`.

🏆 **Prediction 5/5 → scored 5/5.** Row 3 is the Session-6 vocabulary-mismatch question (`"what does he do at his current job?"`) that once retrieved **zero** payments chunks — now `about.txt ×5`. The 2.8a fix, re-proven by a script instead of an eyeball, thirteen sessions later.

❓ **Self-test:** a row is `{"file": ["a.txt"], "match": "any"}`. You flip it to `"all"`. The verdict changes. What does that prove?
<details><summary>answer</summary>The <strong>runner</strong> is broken, not the retriever. With exactly one file in the label, "at least one of one" and "every one of one" are the same sentence — the two branches <em>must</em> agree. Any disagreement is a bug in the scorer, and no interpretation of the data can rescue it.</details>

---

## 2.10.2b — two guards the golden set earned the hard way 🛡️

💡 **Idea:** two failures that look identical on screen (`FAIL`) and have nothing to do with the retriever.

🛡️ **Guard 1 — a filename that doesn't exist never matches, silently.** He typed `"project.txt"` (no `s`) into a key. No error, no warning; that row would just fail every run forever while the retriever took the blame. `score.py` now checks every key filename against `service/notes/` on disk and raises before scoring anything.

```python
on_disk = {p.name for p in NOTES.glob("*.txt")}   # bare names, not paths
```

⚠️ **Guard 2 — an `"all"` row listing N files needs `k >= N`.** At `k=1` exactly one chunk comes back, so **one** file is the maximum possible; a 2-file `"all"` row is arithmetically unpassable. Measured: at k=1 the frontend row failed while `search()` had done nothing wrong. **Check `k >= N` before you ever blame the ranking.**

🟢 **The measured win — meaning beat spelling, on a real recruiter question.** New row `"can he start immediately?"` — the word *immediately* appears in **none** of the 6 notes files (grepped) — and `faq.txt` (*"notice period: 2 months"*) comes back at **rank 1**, passing even at `k=1`. Keyword search returns nothing here. This is 2.5's `cat/kitten 0.788` cashing out as a passing test.

🔁 **The pattern across S18–S21: three times the culprit was the TEST, not the code.** (1) `skills.txt` demanded for Kubernetes — word not in the file. (2) `projects.txt` demanded for *"lead a team"* — word present, answer absent. (3) an `"all"` row run at `k=1`. **Add the S19 scorer bug and it's four.** *"The test is broken"* is a real diagnosis; most people never reach for it.

❓ **Self-test:** a row expects `["skills.txt", "projects.txt"]` with `"all"` and fails. What's the first thing you check — the ranking, the key, or `k`?
<details><summary>answer</summary><strong>k</strong>, then the key, then the ranking. <code>k &lt; 2</code> makes the row impossible; a key naming a file that doesn't answer the question makes it impossible too. Only once both are ruled out is a FAIL actually about retrieval.</details>

---

## 2.10.3 — a score that can see *position* (MRR + top1) 📊

💡 **Idea:** hit-rate is **binary** — "is the answer anywhere in the top k?" Reranking's entire job is moving a correct chunk from rank 4 to rank 1, which a binary metric scores **identically**. A perfect reranker would have printed the same 7/7. ⇒ **upgrade the instrument before the atom that needs it.** (His objection, S19. His atom.)

🧮 **Mean Reciprocal Rank, read backwards:** **rank** = position of the first correct file → **reciprocal** = flip it, `1/rank` → **mean** = average over all questions.

```
        (1/rank1) + (1/rank2) + ... + (1/rankN)
MRR =  ------------------------------------------
                        N
```
rank 1 → `1.00` · rank 2 → `0.50` · rank 3 → `0.33` · not found → `0`. Ceiling **1.0**, floor **0**.
**Σ is a `for` loop that adds** — in JS: `scores.reduce((a,b) => a+b, 0) / scores.length`. That *is* the formula, different alphabet.

💻 **The lines that matter** (`learn/phase2/score.py`):
```python
ranks[f] = results.index(f) + 1 if f in results else None   # .index gives the FIRST hit
if 1 in ranks.values():        top1 += 1                     # a question about the ROW, not each file
u = [i for i in ranks.values() if i is not None]             # min() can't compare None to int
if len(u) > 0:                 MRR += 1 / min(u)             # best rank in the row
print(..., round(MRR / len(questions), 2))                   # the 1/N half — he shipped 6.5 without it
```

📊 **BASELINE, pre-rerank** (`learn/phase2/baseline.md`): `k=5` → **7/7 · top1 6/7 · MRR 0.93** · `k=3` → identical · `k=1` → **4/7 · top1 6/7 · MRR 0.86**.

🔑 **The three metrics answer three different questions:**
| metric | asks | changes with k? |
|---|---|---|
| hit-rate | is it **anywhere** in the top k? | **very** |
| MRR | **how high** is the best correct file? | only if the best falls off the end |
| top1 | is **rank 1** correct? | **never** — position 1 is position 1 |

⚠️ **Headroom is +0.07 and that's the corpus, not the harness.** Only row 2 is imperfect (`projects.txt` at rank 2). 6 files on distinct topics is an easy retrieval problem; reranking earns its name on hundreds of confusable chunks. **Know this before 2.11 so a small gain doesn't read as failure.**

🐛 **Three bugs he wrote and fixed, all worth keeping:** (1) `ranks[f] = i` from `enumerate(results)` — the **last** duplicate won, and `.index()` fixed it for free by returning the first; (2) the `top1` check **inside** the per-file loop → one row counted twice, a percentage over 100%; (3) `u.size` — a numpy reflex on a plain dict. *An object's API comes from what created it* — 4th appearance.

❓ **Self-test:** you drop k from 5 to 3 and `top1` doesn't move. Bug or expected?
<details><summary>answer</summary><strong>Expected, always.</strong> Shrinking k truncates the tail, never the head — rank 1 is rank 1 at every k. If <code>top1</code> ever <em>did</em> move with k, the scorer would be broken.</details>

---

## Atom 2.11.0 — reranking (scoped S20, not built)

💡 **Idea:** cosine search is a **bi-encoder** — it embeds the question and each chunk **separately**, so the chunk never actually reads the question. Fast (one matmul over all 132), and slightly dumb. A **cross-encoder** takes `(question, chunk)` as **one input** and returns a single relevance number. Far more accurate, far too slow for the whole store. So:

```
search(q, k=20)   →  20 candidates      (cheap, one matmul)
rerank(q, those)  →  20 relevance scores (a small local model)
sort → keep 3     →  the LLM
```

⚠️ **Retrieve WIDE, not the same k.** Reranking the top 5 can only re-sort the 5 cosine already liked. **The gain comes from rank 9 and rank 14** — chunks cosine ranked too low to send, that the cross-encoder promotes into the top 3. Wide net, strict filter. *(MERN: an indexed Mongo query is `search` — fast, dumb, gets a candidate set. The `.filter()` you run in Node over those docs is the reranker — slow, smart, and you'd never run it over the whole collection.)*

⚠️ **It is NOT an LLM** — his read, corrected. `cross-encoder/ms-marco-MiniLM-L-6-v2` is ~22M params, same MiniLM family as the embedder. **No generation, no tokens, no API.**

| | embedder (bi-encoder) | reranker (cross-encoder) | the brain (LLM) |
|---|---|---|---|
| input | one text | question **+** chunk together | full prompt |
| output | 384-dim vector | one score | generated text |
| can build an index? | ✅ | ❌ *(this is why it can't replace search)* | ❌ |
| cost | free, local | free, local | ₹ per token |
| runs over | all 132 chunks | ~20 candidates | 1 call |

🐳 **HIS CATCH, and he was right — *"did you forget the docker free limit?"*** Verified: `requirements.txt` = **fastapi · uvicorn · pydantic · slowapi · openai · dotenv · numpy**. **No torch. No sentence-transformers.** `service/embedder.py` calls OpenRouter's `text-embedding-3-small` over HTTP and `index.npz` is 972 KB of precomputed vectors — **that is why Spidy fits Render free and why the cold start isn't 30 seconds.** `pip install sentence-transformers` drags **torch** into a **512 MB** instance ⇒ **OOM, not slowness.** ⇒ **"free and local" is a property of the machine, not the model.** Free on his Mac ≠ free on the box that ships.

📌 **Decided (option A): measure first, ship later.** `learn/` is in `.dockerignore`, so cross-encoder experiments never touch the image. Get the number, *then* choose a door: **B** hosted rerank API (no weights, +200–400ms) · **C** LLM-as-reranker (reuses `openai`, costs tokens) · **D** MMR/keyword heuristics (pure numpy, free).

🎯 **And the reason the scorer comes first:** **reranking changes ORDER, not MEMBERSHIP.** His line 11 — `[f in results for f in q["file"]]` — is **set membership**: position 1 and position 5 are the same to it. **A perfect reranker would still print 6/6.** ⇒ **a saturated benchmark measures nothing**, and every ship-door above is unfalsifiable until `top1` exists. Same family as 2.10's lesson: there an *untested branch* hid a bug; here a *maxed-out score* hides a gain.

❓ **Self-test:** you swap in a flawless reranker and `score.py` prints `6/6`, exactly as before. Name the two different things that could mean, and the one change to the scorer that tells them apart.
<details><summary>answer</summary>Either (a) the reranker did nothing, or (b) it moved the right chunks from rank 4 to rank 1 and the metric can't see it. <code>f in results</code> is membership-only, so both look identical. The fix: record each expected file's <strong>1-based position</strong> and add a strict <code>top1</code> tally — then (b) shows as <code>top1</code> rising while <code>score</code> stays 6/6. Dropping to <code>k=3</code> adds headroom on top.</details>

---

## ⬜ Coming next
- ⬜ **owed:** follow-up questions — conversation history without re-sending CONTEXT every turn (the 1.6 snowball)
- **2.9c/2.10** — LLM-based semantic chunking, when the data is messy enough to need it
- **P1.5** — FastAPI service → React recruiter bot on the portfolio
- ⬜ **owed:** conversation memory without the context snowball (currently stateless — no follow-ups)
- **2.5a** 🧮 span/basis · **2.5b** 🧮 projection (deferred, not blocking)

---

## Phase 2 so far, in one breath

> Text becomes a **384-number unit vector** whose *direction* is its meaning. Compare directions with **cosine** — which, because the model pre-normalizes, is just a **dot product**. But every embedding leans into a narrow **cone**, so the absolute number is inflated and query-dependent garbage. **The ranking is the signal.** Retrieve **top-k**, never a threshold.
