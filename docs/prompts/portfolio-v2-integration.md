# Prompt for the portfolio-repo Claude session (8 Aug 2026)

Paste everything below the line into a Claude Code session opened in the **portfolio repo**
(`hemavardhanreddy.vercel.app`), not this one.

---

I have a chat widget ("Spidy") on my portfolio site that talks to a FastAPI backend I wrote.
I need two things done: **(1) upgrade it to the v2 API with conversation memory**, and
**(2) fix a mobile layout bug.** Please investigate the existing widget code first and tell me
your plan before changing anything.

## Task 1 — move the widget from `/ask` to `/v2/ask` (conversation memory)

**Base URL:** `https://ai-voice-assistant-su60.onrender.com`

The widget currently calls `POST /ask`, which is stateless — every question is answered with no
knowledge of the previous ones. There is now a `/v2/ask` that accepts conversation history, so
follow-ups like *"and is he good at it?"* resolve correctly.

**Exact contract (do not guess it — this is copied from the FastAPI source):**

```
POST /v2/ask
Content-Type: application/json

{
  "question": "so he knows it?",
  "history": [
    { "role": "user",      "content": "does he know MongoDB?" },
    { "role": "assistant", "content": "He has used MongoDB only in college..." }
  ]
}

200 → { "answer": "...", "version": "v2" }
```

**Hard constraints from the server side — violating these returns 422 and the handler never runs:**

- `role` is a strict `Literal["user", "assistant"]`. **No `"system"`, no other value.** The
  server rejects the whole request, it does not skip the bad turn.
- `history` is optional and defaults to `[]`. Sending `[]` or omitting it is identical to the old
  stateless behaviour.
- Extra fields in the body are **silently dropped**, not rejected. Don't rely on sending extras.
- Rate limit is **20 requests/minute per IP** → `429`.
- Upstream model failures come back as **`502`** with `{"detail": "..."}`.
- CORS already allows `https://hemavardhanreddy.vercel.app` and `http://localhost:5173`.
  **Do not ask me to change the backend for CORS** — it is configured.

**What the widget needs to do:**

1. Keep the conversation in component state as an array of `{role, content}` turns.
2. On send: POST the new `question` plus the history **so far** (i.e. *not* including the question
   being asked — the server appends it itself). On success, push both the user turn and the
   assistant's `answer` into state.
3. **Cap the history** before sending — send at most the last ~6 turns (3 exchanges). The full
   history is replayed to the LLM on every single request, so an uncapped array means cost and
   latency grow forever. Keep the full history for *display*, cap only what is *sent*.
4. On a failed request, do **not** push a broken turn into history — the next request would
   replay the corruption.

**Latency reality — the UI must be designed around this, it is the main UX risk:**

- The endpoint **does not stream.** It returns one complete string. Typical total is **3–5
  seconds**, and I have measured **11+ seconds** on the first request after idle, because the
  backend is on Render's free tier and spins down.
- So: a visible thinking/typing indicator is mandatory, the send button and input must be
  disabled while a request is in flight, and there should be a sensible timeout with a retry
  affordance. Several seconds of a dead-looking box is the failure mode to avoid.
- If the widget already pings `GET /health` to warm the backend, keep that. If it doesn't, add it
  on first open of the chat — it turns a cold 11s first answer into a warm one.

## Task 2 — mobile bug: the header scrolls off-screen when the keyboard opens

**Symptom:** on a real mobile browser, tapping the chat input opens the on-screen keyboard, and
the entire chat header goes off the top of the screen. The layout is not usable while typing —
I can't see whose chat I'm in, or the close button.

**Please reproduce it first** in a narrow viewport with a simulated keyboard/soft-keyboard
resize before you change any CSS, and tell me what you find.

**Likely causes, in the order I'd check them** — confirm rather than assume:

- The container is sized with `100vh`. On mobile `100vh` ignores the keyboard and browser
  chrome, so the box stays taller than the visible area and the top gets pushed out.
  `100dvh` (dynamic viewport height) is usually the fix.
- The browser is auto-scrolling the focused input into view, scrolling the whole page and taking
  the header with it. The fix there is making the **message list** the scroll container and the
  header `position: sticky; top: 0` inside a non-scrolling shell — so only messages move.
- If the widget is `position: fixed`, iOS Safari in particular repositions fixed elements when
  the keyboard opens; the `visualViewport` API may be needed to track the real visible height.

**Acceptance criteria:**

- With the keyboard open on a small viewport, the header stays visible and pinned.
- The message list scrolls, the page itself does not.
- Newest message stays visible when the keyboard opens.
- Nothing regresses on desktop.
- Test at 320px, 375px and 768px widths.

## How I'd like you to work

- Read the existing widget code and show me your plan before editing.
- Do the two tasks as **separate commits** so I can revert one without the other.
- I want to understand the changes, not just receive them — explain the reasoning for the CSS
  fix in particular, since I need to not write this bug again.
