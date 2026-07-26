# Lesson 01 — The Brain (Phase 1 recap) 🧠

Everything below, YOU built and verified. Files live in `learn/phase1/`.

## The one-line summary
An LLM call is a `fetch` with a fancy body; everything else — personality, memory, creativity, the typing effect — is engineering around that call.

## What each atom taught

| Atom | File | The takeaway (in your words someday) |
|---|---|---|
| 1.0 | `.venv`, `.env` | venv = per-project `node_modules`; isolation first, portability bonus. `pip` = `npm`, `load_dotenv()` must be **called**, not just imported. |
| 1.1 | `first_call.py` | One POST, JSON in, JSON out. Only `.create()` touches the network. We call Claude **through OpenRouter** (`openai` SDK + `base_url`). |
| 1.2 | usage receipt | Tokens ≈ ¾ word; punctuation counts. You pay input AND output. Verified by hand: 18 in + 10 out on Haiku = $0.000068. |
| 1.3 🔧 | `softmax.py` | Model scores every token → **softmax** (`e^score / sum`) turns scores into probabilities → weighted die picks one. `exp` exists so negative scores stay legal. Probabilities are shares of one pie. |
| 1.4 | `temperature.py` | Temperature divides scores before softmax. T=0 → always top token (Starbucks×6). T high → underdogs win rolls. **No competition in the die → temperature changes nothing.** |
| 1.5 | `system_prompt.py` | System prompt = just text, placed first + trained to outrank user. Personality is data, not code. Spoken answers ≠ written answers. |
| 1.6 | `memory.py` | The API is **stateless** (like REST). "Memory" = resending full history. Roles: system/user/assistant — label honestly. Cost **snowballs** with turns; `cached_tokens` (~90% off repeats) is the rescue. Python gotcha: lists don't grow by index — use `.append()`. |
| 1.7 | `streaming.py` | `stream=True`: ONE request, response arrives as delta chunks (SSE). `end=""` + `flush=True` for live typing. Critical for voice latency. |
| 1.8 | `chatbot.py` | Assembly: loop + append + stream + accumulate. Accumulate because memory needs the full reply. `try/except` + `messages.pop()` = don't poison history on errors. |

## Terminal wisdom collected on the way
- Tracebacks read **bottom-up**; the crash line number is a clue, not a verdict.
- `^Z` suspends (parked process, still holding RAM) — `jobs`, `fg`, `kill %1`. Quit with `exit`/`Ctrl+C`.
- Never print full secrets, even locally.

## Cost notes (Haiku 4.5 via OpenRouter)
$1/M input, $5/M output. Whole Phase 1 cost: well under 1 cent. Long chats snowball input tokens → caching + (later) history management matter.

## The cliffhanger → Phase 2
Storing chats in MongoDB makes memory *persist*, but resending everything forever can't scale — and what if the bot needs to remember 10,000 documents? Answer: store knowledge, **search it, send only the relevant bits** = RAG, built on embeddings + cosine similarity. That's the math we open the hood on next.

Foundations ticked so far: **F2 (probability & softmax)** ✅
