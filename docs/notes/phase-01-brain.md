# Phase 1 — The BRAIN 🧠 (revision notes)

**What you built:** a streaming chatbot with memory, a product voice, and error recovery — `learn/phase1/chatbot.py`.
**The one sentence:** *an LLM call is a `fetch` with a fancy body; everything else in this phase is what goes in the body.*

⚡ **60-second revision:** read only the 💡 lines. Open a card only if its 💡 feels fuzzy.

---

## 1.0 — venv + SDKs + `.env`

💡 **Idea:** Python's `venv` is `node_modules` — a per-project sandbox so global installs never collide.

💻 **The line that matters:**
```bash
python -m venv .venv && source .venv/bin/activate
```

⚠️ **Gotcha:** `.env` is **gitignored on purpose**. On every new machine you must recreate it by hand (this bit you in Session 5 on the new laptop). `.env.example` lists the keys; it holds no secrets.

❓ **Self-test:** Your terminal prompt shows `(.venv)`. What does that actually change?
<details><summary>answer</summary>It puts <code>.venv/bin</code> at the front of your <code>PATH</code>, so <code>python</code> and <code>pip</code> resolve to the sandbox copies instead of the system ones. That's the whole trick — no magic.</details>

---

## 1.1 — First API call

💡 **Idea:** You talk to Claude through **OpenRouter** using the **`openai`** SDK — one key, many models, swap models by changing a string.

💻 **The line that matters:**
```python
client = OpenAI(base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_API_KEY"))
r = client.chat.completions.create(model="anthropic/claude-haiku-4.5", messages=[...])
print(r.choices[0].message.content)
```

⚠️ **Gotcha:** the `openai` package name says nothing about which model you reach. `base_url` decides the provider, `model` decides the brain. Reading `openai` in the import and assuming GPT is the classic misread.

❓ **Self-test:** Why is the response buried at `.choices[0]`?
<details><summary>answer</summary>The API can return several independent completions for one request (the <code>n</code> parameter). You asked for one, so you take index 0. The list shape is there for the case you're not using.</details>

---

## 1.2 — Tokens & cost

💡 **Idea:** You are billed per **token**, not per request — and **input tokens are far cheaper than output tokens**.

💻 **The line that matters:**
```python
print(r.usage)   # prompt_tokens, completion_tokens, total_tokens
```

⚠️ **Gotcha:** input is cheap because the model reads the whole prompt **in parallel (prefill)** — one pass over all of it. Output is expensive because it's generated **one token at a time, sequentially**, each one requiring a full forward pass. It is *not* about caching. (This exact confusion cost you half a mark on the Phase 1 quiz.)

📊 **Your measured number:** `$0.000068` per call, verified by hand against the price sheet.

❓ **Self-test:** Same total token count, two requests. One is 900 in / 100 out, the other 100 in / 900 out. Which costs more, and by roughly how much?
<details><summary>answer</summary>The 100-in/900-out one, by a lot — output typically runs ~4–5× the price of input. Long prompts are cheap; long answers are not. This is the single biggest cost lever in the whole product.</details>

---

## 1.3 🔧 — Softmax by hand

💡 **Idea:** Softmax turns any list of raw scores (**logits**) into probabilities that sum to 1 — by exponentiating each, then dividing by the total.

💻 **The line that matters** (`learn/phase1/softmax.py`):
```python
exps  = [math.exp(s) for s in scores]
probs = [e / total for e in exps]
```

⚠️ **Gotcha #1 — the one you were missing:** those probabilities are **over the entire vocabulary**. Every token the model knows gets a logit, every step. Not "over the sentence", not "over the options" — over ~50,000 candidate next-tokens. This was the root gap behind *"am I going to keep guessing?"* — patched with the `mat`/`floor`/`roof` worked example.

⚠️ **Gotcha #2:** `exp()` is why **negative scores still produce positive probabilities**. `exp(-1) = 0.37`, small but never negative. You tested this deliberately.

❓ **Self-test:** Why exponentiate at all — why not just `score / sum(scores)`?
<details><summary>answer</summary>Two reasons. (1) Negative scores would produce negative or nonsense "probabilities". (2) <code>exp</code> is what makes the gap between scores <em>multiplicative</em> — a score 2 higher becomes ~7.4× more likely, not "2 more likely". That amplification is exactly the knob temperature turns.</details>

---

## 1.4 — Temperature

💡 **Idea:** Temperature divides the **logits** *before* softmax. Low `T` → sharpens the distribution (predictable). High `T` → flattens it (creative).

💻 **The line that matters:**
```python
temperature = 0.0   # same input → same output, every time
```

⚠️ **Gotcha:** temperature divides **logits, not probabilities**. You had this backwards initially. Dividing probabilities would break the "sums to 1" property; dividing logits and *then* softmaxing keeps it valid. Order matters.

🧪 **Your experiment:** at `T=0.0`, "name a coffee shop" returned **Starbucks** three times — the model reached for the safest real answer. Asking for an *invented* name at the same temperature still gave one repeated answer. `T=0` doesn't mean boring, it means **deterministic**.

❓ **Self-test:** Your product needs an assistant that never contradicts itself between sessions. What temperature, and what's the cost of that choice?
<details><summary>answer</summary>Low (0–0.3). The cost is blandness and repetition — it will reach for the most common phrasing every time, and it can lock onto a bad answer with total confidence. Consistency and interestingness are the same dial.</details>

---

## 1.5 — System prompt

💡 **Idea:** The `system` message sets identity and rules for the whole conversation — it's the highest-leverage free thing in the entire project.

💻 **The line that matters:**
```python
messages = [{"role": "system", "content": "you are ..."}, {"role": "user", ...}]
```

⚠️ **Gotcha:** it is not a separate API or a setting — it's just the **first message in the same list**, with a different `role`. Nothing magical happens; the model was trained to weight that role heavily.

🧪 **Your experiment:** pirate voice → product voice. Same code, same model, completely different assistant.

❓ **Self-test:** Where does the system prompt go once the conversation is 30 turns long?
<details><summary>answer</summary>Still at index 0, and still re-sent on <em>every single call</em>. It never "sticks" server-side. You pay for it every turn — which is exactly why prompt caching exists.</details>

---

## 1.6 — Conversation memory

💡 **Idea:** The API is **stateless**. Memory is an illusion you create by replaying the entire history on every call.

💻 **The line that matters** (`learn/phase1/memory.py`):
```python
messages.append({"role": "assistant", "content": r1.choices[0].message.content})
messages.append({"role": "user", "content": "what is my name?"})
```

⚠️ **Gotcha — the snowball:** turn 20 re-sends turns 1–19. Cost grows **quadratically** with conversation length, not linearly. Prompt caching blunts it; it doesn't remove it. This is the reason Phase 2 exists — *retrieve* the 3 relevant chunks instead of *replaying* all 500.

❓ **Self-test:** You forget to append the assistant's reply, but keep appending user messages. What breaks, and what does it look like?
<details><summary>answer</summary>The model sees user turn after user turn with nothing of its own in between. It loses the thread of what it already said, repeats itself, re-asks answered questions, and drifts — it looks like amnesia, because the transcript it's reading genuinely has its own half deleted.</details>

---

## 1.7 — Streaming

💡 **Idea:** `stream=True` returns **SSE chunks** as they're generated, so the user sees words appear instead of staring at a spinner.

💻 **The line that matters** (`learn/phase1/streaming.py`):
```python
for chunk in response:
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end="", flush=True)
```

⚠️ **Gotcha — two of them:**
- `delta` is often `None` (role-only and terminal chunks). Without `if delta:` you crash mid-stream.
- `flush=True` is mandatory. Python buffers stdout, so without it the text still arrives all at once and you've gained nothing.

📊 **The metric this buys you:** **time-to-first-token**. Total time barely changes; *perceived* speed changes enormously. This matters more in the voice loop (Phase 5) than anywhere else — you can start speaking sentence 1 while sentence 2 is still generating.

❓ **Self-test:** Does streaming reduce your token cost?
<details><summary>answer</summary>No. Identical tokens, identical bill. It buys perceived latency only. (Worth knowing: with <code>stream=True</code>, <code>usage</code> arrives in the final chunk rather than on the response object.)</details>

---

## 1.8 — Chat loop ✅ **working chatbot**

💡 **Idea:** Everything above, in a `while True` — memory + streaming + system prompt + a `try/except` that survives a bad API call.

💻 **The shape:**
```python
while True:
    user = input("you: ")
    messages.append({"role": "user", "content": user})
    # stream reply, accumulate it into `full`
    messages.append({"role": "assistant", "content": full})
```

⚠️ **Gotcha:** when streaming, you must **accumulate the deltas into a string yourself** to append to history. There's no complete message object handed to you at the end — you build it as it arrives, or your bot has amnesia.

❓ **Self-test:** The API throws on turn 5. You catch it and continue the loop. What must you do to `messages` before the next turn?
<details><summary>answer</summary><strong>Pop the user message you already appended.</strong> Otherwise history holds a user turn with no assistant reply, and the damage compounds every subsequent turn. You worked this out yourself in Phase 2 and added <code>pop()</code> to the <code>Memory</code> class unprompted.</details>

---

## 1.9 🚢 — Ship it

💡 **Idea:** A phase isn't done when the code runs — it's done when it's readable, committed, and explainable.

✅ Done: READMEs, pushed to GitHub, 6-question recall quiz **5.5/6**.
⬜ **Still owed:** demo GIF · portfolio card (deferred by choice).

---

## Phase 1 in one breath

> A model call is a stateless HTTP request. You send a list of messages; the model produces **logits over the whole vocabulary**, divides them by **temperature**, softmaxes them into probabilities, samples one token, and repeats. Memory is you re-sending the list. Streaming is you reading the tokens as they're sampled. Cost is tokens — and **output tokens are the expensive ones**.
