# Prompt — add the versioned AI assistant to hemavardhanreddy.vercel.app

> Paste everything below the line into a fresh Claude Code session opened in
> `/Users/hemavardhang/Desktop/portfolio`.
>
> The assistant is named **Spidy**. Paste as-is — no placeholders left to fill.
> You will need to add a cover image at `src/assets/spidy.jpg` yourself.

---

I want to add my own AI assistant to this portfolio: a floating chat widget that
answers recruiter questions about me, plus a project card for it. The backend is
already built, deployed and working — you are only building the frontend.

## 1. What already exists (do not rebuild any of this)

**The API is live:** `https://ai-voice-assistant-su60.onrender.com`

| | |
|---|---|
| `GET /health` | → `{"status":"ok"}` |
| `POST /ask` | body `{"question": "..."}` → `{"answer": "..."}` |

It is a retrieval-augmented bot over my own notes: it retrieves the 5 most
relevant chunks about me and answers only from those, so it refuses politely
instead of inventing things. It is named **Spidy** and refers to me in the third
person — it is my assistant, not me.

**Response details that matter for the UI:**

- The `answer` string's **last line is a citation list** in the form
  `[skills.txt, preferences.txt, faq.txt]`. Parse that off the end and render it
  as small source chips under the message — do **not** show it as body text.
- **Rate limited to 20 requests/minute per IP** → HTTP `429`.
- **HTTP `502`** when the upstream model is unavailable. The body is
  `{"detail": "Upstream model unavailable. Try again."}`.
- No auth, no API key. Never add one in frontend code.
- **⚠️ The host sleeps.** It is on a free tier that spins down after ~15 minutes
  of inactivity. **A cold first request can take 30–60 seconds.** This is the
  single most important UX constraint in this task — see §4.

## 2. The codebase you are working in

- **Vite + React 19 + TypeScript.** `framer-motion` for animation, `lenis` for
  smooth scroll. No Tailwind, no component library in use.
- **ALL site content lives in `src/portfolio.config.ts`.** Components import from
  it and render. Follow this pattern strictly — every string, URL and version in
  this feature goes in the config, not hardcoded in a component.
- **Styles are plain CSS in `src/styles/global.css`**, BEM-ish class names
  (`.proj`, `.proj__cover`, `.proj__body`). Add your styles to that file in the
  same style. **Do not** add CSS modules, styled-components, or Tailwind.
- **Use the existing design tokens.** Do not introduce new colours:

  ```
  --bg #0c1013   --card #12181d   --card-2 #0f1418   --line #1f2830
  --txt #edf3f0  --body #b7c2c4   --dim #93a1a8      --dim-2 #5e6c74
  --green #3ce8a0   --green-dim #1e7a55
  --green-bg rgba(60,232,160,.07)   --green-line rgba(60,232,160,.18)
  --r 16px   --pad-x   --disp (Space Grotesk)   --body-font (Inter)   --mono (JetBrains Mono)
  ```

- Env vars use the `VITE_` prefix (see `.env` and `src/metrics.ts`).
- `App.tsx` composes the page. Sections live inside `<main>`; a fixed overlay
  should mount **outside** `<main>`, as a sibling of `<Nav />`.
- Reusable helpers already available: `Reveal` (scroll-in animation),
  `Magnetic`, `SectionHead`, `SpotlightCard`.

## 3. What to build

### 3a. A bot **version registry** in `src/portfolio.config.ts`

I will ship successive versions of this assistant. The widget must open the
**latest** version by default and let a visitor switch to and read about
**previous** versions. Build that shape now, even though only v1 exists today.

```ts
export const assistant = {
  name: 'Spidy',
  tagline: 'Ask about my work — answers come from my own notes, with sources.',
  bubbleLabel: 'Ask Spidy',
  // newest first — index 0 is what opens by default
  versions: [
    {
      id: 'v1',
      label: 'v1 · Grounded Q&A',
      apiUrl: import.meta.env.VITE_ASSISTANT_V1_URL ?? 'https://ai-voice-assistant-su60.onrender.com',
      status: 'live' as const,          // 'live' | 'legacy' | 'coming-soon'
      released: '2026-07',
      blurb: 'Retrieval-augmented answers from my own notes, with source citations. Each question is answered independently.',
      capabilities: ['Grounded answers', 'Source citations', 'Refuses what it does not know'],
      limitations: ['No follow-up memory', 'Text only'],
    },
  ],
}
```

Rules for this registry:

- `status: 'live'` → selectable and usable.
- `status: 'legacy'` → selectable; the composer still works but show a small
  "older version" note above the thread.
- `status: 'coming-soon'` → visible in the list, **not** selectable, composer
  disabled, no network calls. Do not invent any coming-soon entries — I will add
  them myself.
- **Do not** render a version switcher UI that implies choice when only one
  version exists. With a single entry, show the version as a quiet label; render
  the switcher only when `versions.length > 1`.

### 3b. A project card

Add an entry to the existing `projects` array in `src/portfolio.config.ts`,
matching the shape already there (`name`, `kind`, `year`, `image`, `url`,
`linkLabel`, `description`).

- `name: 'Spidy'`
- `kind: 'Live AI assistant'`
- `url` → the live API base URL
- Needs a cover image. `src/assets/` has `kira.jpg`, `acharya.jpg`,
  `vedamandir.jpg`. **There is no image for this one yet** — do not reuse
  `kira.jpg` (that belongs to the `kira-multi-repo-bridge` package card and would
  be confusing). Instead: leave the `image` field referencing a new
  `./assets/spidy.jpg`, create nothing, and **tell me in your summary that
  I need to drop that file in.** Do not generate a placeholder image.

Suggested description (edit to taste, keep it honest):

> A retrieval-augmented assistant that answers questions about my work from my
> own notes — with citations, and an honest "I don't know" when the answer isn't
> in them. Python/FastAPI, running in 63MB of RAM.

### 3c. `src/components/AskBot.tsx` — the widget

**Closed state:** a fixed bubble, bottom-right, above all content. Circular or
pill, `--green` accent, `--mono` label. Respect safe-area insets on mobile.

**Open state:** a panel anchored bottom-right on desktop (≈380×560px, capped by
viewport), **full-screen sheet on mobile** (`max-width: 640px`). Contains:

1. **Header** — bot name, the active version label, a close button. If
   `versions.length > 1`, a switcher here (dropdown or segmented control).
2. **Thread** — alternating question/answer bubbles, newest at the bottom,
   auto-scrolled. Each answer renders its citation chips underneath.
3. **Empty state** — the tagline plus 3 clickable starter questions. Use these
   verbatim, they are known to retrieve well:
   - "Has he handled payments at scale?"
   - "What is he learning right now?"
   - "Does he know databases?"
4. **Composer** — a text input plus send button. Enter submits, Shift+Enter
   newlines. Disabled while a request is in flight.

**Version detail:** clicking the version label opens a small panel showing that
version's `blurb`, `capabilities` and `limitations` from the registry. This is
how a visitor "explores previous versions" — they read what each one could do and
can switch to it.

State is in-memory only. **Do not persist the thread** to localStorage.

### 3d. Styles + mounting

- Add all classes to `src/styles/global.css` following the existing conventions.
- Mount `<AskBot />` in `App.tsx` as a sibling of `<Nav />`, outside `<main>`.
- Use `framer-motion` for the open/close transition, matching the easing already
  used in `Reveal.tsx`. Respect `prefers-reduced-motion`.

## 4. The cold-start problem — handle this properly

The free tier sleeps. A recruiter's first question can hang for 30–60 seconds,
and a spinner that long reads as "broken".

Required behaviour:

1. **Warm on open.** The moment the panel opens, fire `GET /health` on the active
   version's `apiUrl` and ignore the result. This starts the container waking
   while the visitor is still reading and typing.
2. **Timeout of 90 seconds**, not the browser default, via `AbortController`.
3. **Escalating status text** while a request is pending — replace the message,
   don't stack them:
   - 0–4s: `Thinking…`
   - 4–12s: `Waking the server — it sleeps when idle…`
   - 12s+: `Still waking up. First question of the day takes a moment.`
4. **Distinct, human error states:**
   - `429` → "That's a lot of questions! Give it a minute."
   - `502` → "My model provider is having a moment. Try again?"
   - abort/network/timeout → "Couldn't reach the assistant. It may be asleep — try once more."
   - Every error keeps the typed question recoverable and offers a retry.

## 5. Constraints

- **No new dependencies.** `fetch`, React state, and `framer-motion` are enough.
- **TypeScript strict.** No `any`. Type the API response and the registry.
- Accessible: the panel is a labelled dialog, focus moves into it on open and
  returns to the bubble on close, `Esc` closes, the thread is an aria-live
  region, everything is keyboard reachable.
- Mobile-first. The bubble must never cover the footer's interactive elements.
- Never send anything except the visitor's question. No analytics, no PII, no
  keys.
- Keep the answer rendering plain text with preserved line breaks. **Do not add a
  markdown renderer** — that is a new dependency and the API returns plain prose.

## 6. Do NOT

- Do not modify any existing component's behaviour or restyle existing sections.
- Do not touch `src/metrics.ts`, `src/metrics.shared.ts` or `scripts/`.
- Do not rename or alter the existing `Kira` project entry
  (`kira-multi-repo-bridge`) — it is a different, unrelated project.
- Do not invent capabilities, versions, or metrics for the assistant.
- Do not hardcode the API URL anywhere except the config registry.

## 7. Done means

- `npm run build` passes clean (`tsc -b` included).
- `npm run dev` → bubble visible on every section; panel opens; a real question
  gets a real answer from the live API with source chips.
- Rate limit, 502 and timeout paths each produce their own message (force them by
  temporarily pointing `apiUrl` at a bad URL to check the failure path).
- With one version in the registry, **no switcher UI renders** — just a quiet
  label.
- Your summary tells me: the cover image I still need to add, and anything you
  had to guess.

Work in small steps and show me the config changes before you build the
component.

---

## ⚠️ One change needed in the *backend* repo first

In `/Users/hemavardhang/ai-voice-assistant/service/main.py`, the CORS middleware
currently allows only `POST`. The widget's warm-up ping is a `GET`, so add it:

```python
allow_methods=["GET", "POST"],
```

The origins are already correct — `https://hemavardhanreddy.vercel.app` and
`http://localhost:5173` are both allow-listed. Commit, push, and Render will
redeploy automatically.
