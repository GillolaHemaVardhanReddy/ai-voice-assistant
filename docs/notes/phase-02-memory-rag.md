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

## ⬜ Coming next
- **2.9** — point it at a folder of real notes (LLM-based semantic chunking lands here)
- ⬜ **owed:** conversation memory without the context snowball (currently stateless — no follow-ups)
- **2.5a** 🧮 span/basis · **2.5b** 🧮 projection (deferred, not blocking)

---

## Phase 2 so far, in one breath

> Text becomes a **384-number unit vector** whose *direction* is its meaning. Compare directions with **cosine** — which, because the model pre-normalizes, is just a **dot product**. But every embedding leans into a narrow **cone**, so the absolute number is inflated and query-dependent garbage. **The ranking is the signal.** Retrieve **top-k**, never a threshold.
