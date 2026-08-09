# 📝 Mock Exam — v1 + v2 end to end (9 Aug 2026)

**18 questions · 6 sections · 10.5/18**, graded on **mechanism, not outcome**. Several 🟡s were right answers with the wrong *why*. Judged on "does he know what his system does," this is comfortably north of 80%.

This file is **the warm-up question bank** until every ⚠️ below is green. Q3 of each session's recall comes off this list.

---

## 🩺 The diagnosis that matters — MERGE, not blankness

Three times, asked about X, he answered with **an adjacent fact from the same lesson**:

| Asked about | He answered with | Both from |
|---|---|---|
| `[src]` prefix in `rag.py` | `{section}:` prefix in `build_index.py` | the same file-pair lesson |
| the failure caused by `split("\n\n")` | `{section}:` prefix **again** | same lesson |
| Docker `CMD` shell-vs-exec form | `--host 0.0.0.0` | the same Docker session |
| why input tokens are cheap | "cache" | the same cost lesson (answer: **prefill**) |

**He is not forgetting. Neighbouring facts collapse into one slot, and whichever he learned best wins the slot.**

⇒ **Re-teaching does not fix this. Contrast drills do.** Put the two confusable facts side by side, force a choice, then **make him run it** — the S14 `phonebook` method that killed a 3-session miss in 60 seconds.

---

## 🟢 Strong — defensible in an interview tomorrow

- 💡 **Normalize → unit vectors → dot product *is* cosine.** Denominator is `1×1`, so it vanishes.
- 💡 **Absolute scores lie, ranking tells the truth.** Volunteered the S5 centering experiment **unprompted** — *"even after removing the similarity they still come out in the same order, so we trust top-k."* **Best answer of the exam.**
- 💡 **Index time vs query time**, as an axis. Recipe vs cake, outcome **and** mechanism — a repaired S13 gap.
- 💡 **v2 memory design.** Call counts (incl. the embedding call), mutable-default trap all three parts.
- 💡 **v1's stream dies inside the server** — the recruiter never sees it.

---

## ⚠️ The gaps — each one is a warm-up question

### 1. Two prefixes, two times
```python
build_index.py:24   embed_texts.append(f"{section}: {block}")   # INDEX time → read by the EMBEDDER
rag.py:31           f"[{src}] {chunk}"                          # QUERY time → read by CLAUDE
```
<details><summary>❓ Delete <code>[{src}]</code> from rag.py. What breaks?</summary>
Nothing crashes. 200 OK, answer looks fine. But <code>SYSTEM</code> line 24 still orders the model to cite sources it can no longer see — so it drops citations or <b>invents filenames</b>. A <b>contract between two files</b>, failing silently.
</details>

### 2. Which guardrail actually works
| | `SYSTEM` prompt | `boundaries.txt` |
|---|---|---|
| present when | **always, every request** | only if retrieval surfaces it |
| reliability | unconditional | at the retriever's mercy |

<details><summary>❓ What stops Spidy inventing a salary?</summary>
The <b>SYSTEM prompt</b> ("Answer ONLY using the CONTEXT... never guess"). <code>boundaries.txt</code> is a second layer that only helps <i>if it wins a top-k slot</i> — and <code>blind_retriever.py</code> proved top-k returns 5 confident junk chunks and <b>cannot return 0</b>.
</details>

### 3. The blended chunk
Measured on his real index: **127 chunks · min 38 · max 361 · mean 176 chars.**
```
38  → "He is currently open to opportunities."          ← one sharp idea
361 → "...softmax, temperature, streaming, memory,
        embeddings, cosine, retrieval, RAG..."          ← EIGHT ideas, ONE vector
```
<details><summary>❓ What failure does <code>split("\n\n")</code> cause?</summary>
<b>Blended chunks.</b> An embedding is roughly the <i>average</i> of what it contains, so a long multi-topic chunk points at the centre of everything and sharply at nothing — it can rank <b>below</b> a short chunk that's merely on-topic. Plus <b>zero overlap</b>: a fact spanning a paragraph break is severed. His chunker only works today because <b>he hand-wrote the corpus to fit it</b>. → Atom 2.13.
</details>

### 4. The deploy sequence
<details><summary>❓ Get "Rust" in front of a live recruiter — every step.</summary>
1. edit <code>service/notes/skills.txt</code> · 2. <code>python -m service.build_index</code> <b>on the laptop</b> · 3. 💀 <b><code>git add service/index.npz</code></b> — skip it and deploy still goes green with the old answer · 4. push · 5. Render rebuilds, <code>COPY service/</code> brings the new npz · 6. fresh process → <code>store.py:5</code> loads at <b>import time</b> · 7. recruiter sees Rust.<br><br>
<b>What makes it a laptop job:</b> the Dockerfile has <b>no <code>RUN python -m service.build_index</code></b> — by omission. And that's <i>correct</i>: indexing needs the API key, and 🔒 <b>images never forget</b> — a secret in a layer survives deletion in a later one.
</details>

### 5. 🔴 CORS is a **browser** policy, not a server firewall
FastAPI has no deny-list. `CORSMiddleware` only **adds response headers**; the *browser* reads them and decides.
<details><summary>❓ Delete the CORS block. Does the POST reach the server? Does it cost money?</summary>
<b>No and no.</b> A POST with <code>Content-Type: application/json</code> is not a "simple request" — it <b>preflights</b>. The browser sends <code>OPTIONS</code> first, gets no CORS headers back, and <b>never sends the real POST</b>. <code>answer()</code> never runs. Zero spend.<br><br>
💀 <b><code>curl</code> and Postman ignore CORS entirely.</b> So the endpoint tests perfect from your terminal while the widget is stone dead.
</details>

### 6. 🔴 Docker shell vs exec form
| | runs as PID 1 |
|---|---|
| `CMD uvicorn ...` (**shell form**) | `/bin/sh` — uvicorn is its child |
| `CMD ["uvicorn", ...]` (**exec form**) | **uvicorn itself** |

Docker sends `SIGTERM` to **PID 1**. `sh` does **not** forward it → uvicorn never hears it → `SIGKILL` 10s later, mid-request.
<details><summary>❓ Why couldn't he just use exec form?</summary>
<code>${PORT:-8000}</code> is <b>shell syntax</b> — only a shell expands it. Exec form would pass uvicorn the literal 13 characters. <b>Fix that gets both</b> (shipped 9 Aug):<br>
<code>CMD ["sh","-c","exec uvicorn service.main:app --host 0.0.0.0 --port ${PORT:-8000}"]</code><br>
<code>exec</code> <b>replaces</b> the shell with uvicorn — same PID, so uvicorn becomes PID 1 and gets its signal.
</details>

### 7. 🔴 Retries are **extra**, not total
<details><summary>❓ <code>timeout=30.0, max_retries=2</code> — worst case before a 502?</summary>
<b>90 seconds</b> — 1 initial + 2 retries = <b>3 attempts</b> × 30s (plus backoff). He said 60. <br>
<b>Product point:</b> no recruiter waits 90s. They're gone at 8 — so the real worst case is <i>"recruiter left, and you paid for three timed-out attempts anyway."</i>
</details>

### 8. Softmax — the two slips
<details><summary>❓ Logits are one number per what? And do you need softmax to find the winner?</summary>
<b>One logit per token in the vocabulary</b> (~100k+), rebuilt from scratch for <i>every token emitted</i>. (He said "features" — this is the exact S3 gap, slipped again.)<br><br>
<b>No — you don't need to run it.</b> Softmax is <b>monotonic</b>: <code>exp()</code> is strictly increasing and every logit is divided by the same denominator, so the biggest logit is <i>always</i> the biggest probability.<br>
<code>2.0, 1.0, 0.1 → 7.389, 2.718, 1.105 (÷11.212) → 0.659, 0.242, 0.099</code> — order unchanged.<br><br>
🔗 <b>This is the SAME principle as "ranking beats absolute scores," which he owns cold in the vectors room and didn't recognise in the brain room.</b> Centering changed cosine numbers not their order; softmax changes logits not their order.<br><br>
<b>So why run it at all?</b> Because you don't always take the winner — sampling needs real probabilities.
</details>

### 9. Temperature's default is **1.0**, not 0
<details><summary>❓ What was temperature in rag.py before 9 Aug?</summary>
<b>Never set ⇒ the API default of 1.0</b> — maximum sampling, on a citation-bound factual bot. <br>
🏆 <b>His own data already disproved his "default 0" answer:</b> at temperature 0, <code>noise_floor.py</code> would have returned <b>three byte-identical answers</b>. It didn't. <b>Fixed 9 Aug: 0.2 in both answer paths, 0 in the rewriter.</b>
</details>

### 10. 🔴 Prefill, not cache — and the doubled snowball
<details><summary>❓ Why is input cheaper than output?</summary>
<b>Parallelism.</b> Input = <b>prefill</b>: the GPU sees the whole prompt at once, one big batched matmul. Output = <b>one full forward pass per token</b>, strictly sequential — token 11 can't start until token 10 exists. 200 output tokens = 200 passes. <b>Caching is separate and he isn't using it</b> (no <code>cache_control</code> anywhere).
</details>
<details><summary>❓ Turn 10 vs turn 1 — and the v2-specific catch?</summary>
<b>Snowball.</b> Each turn resends everything before it, so total spend grows ~<b>quadratically</b> — turn 10's input is ~10× turn 1's, at full price.<br><br>
🔍 <b>Unnamed until the exam:</b> in v2, <code>rewrite()</code> gets the full history <b>and</b> <code>answer()</code> puts it in <code>messages</code> — <b>the history is sent twice per follow-up turn.</b> That's the hidden second cost of query rewriting, sitting in <code>rag_v2.py</code> right now.
</details>

---

## 🔧 Shipped the same session

| Fix | Why |
|---|---|
| `temperature=0.2` in `rag.py`, `rag_v2.py` | was on the **1.0 default**; tighter answers + a smaller noise floor for every future A/B test |
| `temperature=0` in `rewrite.py` | a rewriter should be deterministic |
| `CMD ["sh","-c","exec uvicorn ..."]` | uvicorn becomes PID 1 → clean SIGTERM shutdown; `${PORT}` still expands (verified) |
| **measured** `embedder.py:19` | raw API norms are `1.0004` / `0.9998` — **not** a no-op, a ~0.04% correction. **Keep it as a contract enforcer**, not for the 0.04%. |
