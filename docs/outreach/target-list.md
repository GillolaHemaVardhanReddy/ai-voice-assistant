# 🎯 Target pipeline

Fill this in. Do not keep the pipeline in his head — after 15 sends he will not remember
who got which version or who he already followed up with.

**Status values:** `unverified` -> `has-bot ❌` -> `audit-pending` -> `audited` -> `sent` ->
`replied` -> `call-booked` -> `WON` / `passed` / `dead`

## Lane 1 — payments / fintech (filter 4: he can grade the answers)

| Company | Docs URL | Bot today? | Human (role) | Status | Sent | Notes |
|---|---|---|---|---|---|---|
| Cashfree | cashfree.com/docs | ✅ YES | — | `has-bot ❌` | — | Ruled out 12 Aug — ships its own docs RAG |
| Juspay | juspay.io/docs | ⬜ | | `unverified` | | thick, HyperSDK, Indian |
| Chargebee | apidocs.chargebee.com | ⬜ | | `unverified` | | subscriptions/billing edge cases = gradeable |
| Zerodha Kite Connect | kite.trade/docs | ⬜ | | `unverified` | | small team, devs answer directly |
| Razorpay | razorpay.com/docs | ⬜ | | `unverified` | | best known, thickest docs, LOWEST reply odds |
| Decentro | docs.decentro.tech | ⬜ | | `unverified` | | smaller = far likelier to reply |
| Setu | docs.setu.co | ⬜ | | `unverified` | | |
| PhonePe / PG | developer.phonepe.com | ⬜ | | `unverified` | | |

## Lane 2 — adjacent dev-tools with thick docs (if lane 1 goes quiet)

| Company | Docs URL | Bot today? | Human (role) | Status | Sent | Notes |
|---|---|---|---|---|---|---|
| | | ⬜ | | `unverified` | | |

Good shapes for lane 2: Indian API-first startups, Series A-C, 30-150 people, docs written by
2-3 people who know they're stretched. Bad shapes: anyone with an "Ask AI" button already,
anyone where the docs lead is 4 layers below a VP.

---

## 🐘 Lane 3 — BIG non-technical corpora (his call, 20 Aug: go for size)

**This is now the primary lane.** He wants a corpus large enough to stress-test the system —
the thing his own 144 chunks can never teach. These are 10-100x his current corpus and public.

### The gate every one of these must pass
> **Fact-lookup, not judgment.** The answer must be *locatable in the document* — a clause,
> a limit, a date, a rate, an eligibility rule. If answering correctly needs professional
> judgment, it is out, no matter how big the corpus.

| Sector | Why the corpus is big | Gradeable? | Why they'd care |
|---|---|---|---|
| **Insurance** (policy wordings, claims FAQs) | every product = a 40-page wording doc | ✅ clauses, limits, waiting periods, exclusions | customers cannot find exclusions; support drowns |
| **Tax / compliance** (guides, filing help) | thousands of guides, changes yearly | ✅ rates, slabs, due dates, section numbers | seasonal support spike, huge public content library |
| **HR / benefits platforms** (handbooks, leave & payroll policy) | every customer has a handbook | ✅ policy rules, entitlements | the #1 repeated internal question set |
| **Government schemes / public policy** | enormous, genuinely public | ✅ eligibility, amounts, deadlines | real public good; but *who is the client?* — usually an NGO or a portal |
| **University / education** (regulations, catalogs, aid rules) | handbooks + per-course rules | ✅ credit rules, deadlines, fees | students ask the same 200 questions forever |
| **Logistics / e-comm ops** (SOPs, seller policy) | seller policy docs are vast | ✅ rules, fee tables, timelines | seller support cost |
| ❌ **Medical advice** | huge | ❌ needs clinical judgment | **REFUSE** |
| ❌ **Legal interpretation** | huge | ❌ needs legal judgment | **REFUSE** — *statute lookup* is fine, advice is not |

### Candidates to verify (all: `unverified` until he opens the site)

**✅ VERIFIED BY HIM, 20 Aug 2026 — widget check done on all six.**

| Company | Corpus | Bot today? | Human (role) | Status | Notes |
|---|---|---|---|---|---|
| **ClearTax** | tax guides, filing help | ❌ none | | 🎯 `audit-pending` | **#1 PICK** — biggest public corpus on the list, most reputed name |
| **Quicko** | tax guides + Quicko Learn | ❌ none | | 🎯 `audit-pending` | **#2 PICK** — same domain as ClearTax ⇒ **the 20 questions get reused**, second audit is ~30 min |
| Ditto Insurance | insurance explainers + wordings | ❌ none | | `unverified` | founders very active on LinkedIn. ⚠️ gate risk: *"which policy should I buy"* is judgment; wordings/waiting periods/exclusions are fact-lookup. Audit only the fact-lookup half |
| Plum (plumhq.com) | group health content | ❌ none | | `passed for now` | no bot, but **public** corpus is thin — the real corpus is per-client policy docs, which are private |
| Keka | HR policy + payroll compliance + product docs | 🟡 **has AI over employee data, no docs bot** | | `parked` | Hyderabad, pure fact-lookup corpus, strong fit — **but they already ship AI features, so they have a team who'd build this themselves.** Lower odds, not zero |
| Onsurity | group health | ✅ **WhatsApp assistant that takes actions** | — | `has-bot ❌` | ruled out — theirs does login + actions, a bigger build than this |
| Zerodha Varsity | finance education | ⬜ site clean, **app unchecked** | | `unverified` | park it — Zerodha builds everything in-house |

### 💡 The efficiency call (20 Aug): audit ClearTax and Quicko together
They are the **same domain**, so one set of 20 tax questions scores against **both** corpora.
Audit #1 costs ~2 hours; audit #2 costs ~30 minutes. **Two audited sends for the price of 1.2.**
General rule to reuse: *pick the second target from the first target's domain.*

⚠️ **The size trap.** A 50,000-chunk corpus is the point, but it changes the build: `index.npz`
in memory stops being viable, which is precisely **Atom 2.14 (ANN / vector DB)** and **2.15
(observability)**. That is a feature — those two atoms cannot be taught honestly on 144 chunks.
But be honest in the pitch about the timeline: a big corpus is 4-6 weeks, not 3.

---

## Verification checklist — run before any audit (10 min, saves 2 hours)
- [ ] Open the docs. **Is there a search widget / "Ask AI" / chat bubble?** If yes -> `has-bot ❌`, stop.
- [ ] Is the corpus actually thick? Under ~200 pages isn't worth a month.
- [ ] `robots.txt` — is crawling the docs path allowed?
- [ ] ToS — anything forbidding automated access or reuse?
- [ ] Is there a **named human** on LinkedIn with DX / docs / DevRel in the title?
- [ ] Can HE grade 20 questions in this domain without asking anyone?

## Weekly log

### Week of 24 Aug 2026
- Post published: ⬜
- Audits done: 0 / 2
- Sends: 0
- Replies: 0
- What changed:

---

## Scoreboard (the only honest signal)
| | audits | sends | replies | calls | won |
|---|---|---|---|---|---|
| total | 0 | 0 | 0 | 0 | 0 |

**Benchmark: 1-2 replies per 10 audited sends.** Below that, the *subject line and first two lines*
are the problem, not the offer — rewrite those before rewriting anything else.
