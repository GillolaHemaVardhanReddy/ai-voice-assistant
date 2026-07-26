# Phase 1 — The Brain 🧠: a streaming terminal chatbot

A terminal chatbot with real conversation memory, live token streaming, a configurable personality, and error recovery — built line by line to understand what's actually happening inside an LLM call. Runs Claude (Haiku 4.5) through OpenRouter.

**Demo GIF coming soon.**

## The scripts (in learning order)

| Script | What it proves |
|---|---|
| `first_call.py` | An LLM call is just a POST with a JSON body — model + messages in, text out |
| `softmax.py` | The next-word picker, coded by hand: `e^score / sum` turns raw scores into probabilities |
| `temperature.py` | Temperature reshapes those probabilities — T=0 locks the top pick, T=1 lets underdogs win |
| `system_prompt.py` | Personality is just a message with `role: "system"` — data, not code |
| `memory.py` | The API is stateless; "memory" = resending the whole history every call |
| `streaming.py` | `stream=True`: one request, reply arrives as live token chunks (SSE) |
| `chatbot.py` | All of it assembled into a working chat loop |

## What's actually happening inside

1. **An LLM call is a `fetch` with a fancy body.** One HTTP POST to `/chat/completions` with `{model, messages}`; the reply text is dug out of the response JSON. The SDK is just a pre-configured HTTP client.

2. **Tokens are the currency.** ~¾ of a word each; punctuation counts. You pay for input AND output. Our first call: 18 in + 10 out = $0.000068 on Haiku ($1/M in, $5/M out) — verified by hand against the response's `usage` receipt.

3. **The next word comes from a weighted die.** The model scores every token in its vocabulary, softmax (`e^score / sum of exps`) turns scores into probabilities that sum to 1, then one token is sampled. `exp` exists so even negative scores become legal probabilities.

4. **Temperature is the die's fairness knob.** Scores are divided by T before softmax. T=0 → always the top token (same answer every run). Higher T → flatter probabilities, more surprise. Caught in the wild: "name a coffee shop" gave `Starbucks` at every temperature — when one candidate holds ~97% of the die, there's nothing to shuffle. Randomness needs competition.

5. **The model has no memory — chat apps fake it.** Like REST, every call starts from zero (call 2 had no idea what call 1 promised to remember). The fix, used by every chat app: append each turn to a `messages` list (`user` / `assistant` roles) and resend it all, every call. Input cost therefore snowballs with conversation length — which is why providers give ~90% off repeated (cached) input tokens.

6. **Streaming = one request, many pieces.** With `stream=True` the connection stays open and delta chunks arrive as the model generates them (Server-Sent Events, like `res.write()` in Node). The chatbot prints each chunk immediately (`end="", flush=True`) while also accumulating the full reply — because history needs the whole text.

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install openai python-dotenv
cp .env.example .env   # put your OPENROUTER_API_KEY in .env
python learn/phase1/chatbot.py
```

Type `exit` to quit (the conversation vanishes with the process — persistent memory is Phase 2's problem 😉).
