# 🎯 Outreach — landing the first client RAG build

Written 20 Aug 2026 (S24), on his call from S22: *"find a freelance client (paid or free) and build their chatbot."*
Extends the S19 plan in `progress.md`. **Nothing here gets sent without his explicit approval.**

---

## The offer, in his words (do not water it down)

- Build a **production-grade RAG chatbot** over their corpus. Free. No fee, ever, for this first one.
- **He** covers build + testing costs during the build.
- **They** pay only: the **LLM/API cost** after handover, and any **domain/hosting** they choose.
- Full **handover** — code, repo, docs. It is theirs.
- He picks **ONE** client. Best corpus or best-known company. Everyone else gets filtered out.

## Why free (say this out loud in every message)

Not "I'm cheap." Not "I'm unsure." The real reason, and it's a strong one:

> "I'm starting freelancing. One production system with a real corpus and real users is worth
> more to me right now than a first invoice. I'll take a testimonial and permission to write it up."

That is a trade, not a favour. People respect a trade.

---

## ⚠️ The one rule that makes this work: AUDIT FIRST, THEN SEND

**Never send a message that asks for the work. Send one that already contains the work.**

Bad:  "I'd love to build a RAG chatbot for your docs for free."     ← a request. Ignorable.
Good: "I asked your docs 20 questions. Your search answered 6. Mine answered 17." ← a result. Not ignorable.

Cost: ~2 focused hours per target before any send. That is the feature. It caps him at 3-5 targets
a week and guarantees he only contacts companies he actually wants.

### The 2-hour audit, per target
1. **Verify no bot exists** (10 min). Open their docs. Look for a search widget / "Ask AI" button.
   Cashfree was ruled out this way on 12 Aug. **This is step 1, not an afterthought.**
2. **Scrape the public docs** (20 min). `robots.txt` + ToS first. Public pages only.
3. **Index it** (20 min) — his existing pipeline: chunk -> embed -> `index.npz`.
4. **Write 20 golden questions** (40 min) — real integrator questions, the kind HE was confused by.
   These must be gradeable by him. If he can't tell a right answer from a plausible one, wrong target.
5. **Score both**: their native docs search vs `search_reranked`. Record hits, top1, MRR.
6. **Record a 90-second demo** (30 min) — screen recording, their docs, 4 questions, one of them
   unanswerable so they see it abstain. **The abstention is the demo.** Everyone shows a right answer.

### 🔴 The number is the whole asset
A single invented or sloppy number ends this before it starts. **Never send with a placeholder
still in the text. Never send a number he has not personally re-run the same day.**
If their search actually beats his, he says so — and that target becomes a case study in learning,
not a pitch. Honesty here IS the differentiator; his two published articles are built on it.

---

## Target filter (priority order, from S19)

1. **Thick public docs** — API/developer docs. Exact tokens, error codes, version numbers.
   (Also the corpus that justifies 2.12 hybrid/BM25.)
2. **No docs chatbot today** — verified by visiting, every time.
3. **A reachable human** — founder, head of DX, docs lead, DevRel. Someone with a LinkedIn presence.
4. 🔑 **A corpus he can GRADE.** Updated 20 Aug — his call: go for size, including non-technical.
   That breaks the old "a domain he knows" filter, so it's replaced by a sharper one:

   > **Fact-lookup corpora, not judgment corpora.**
   > Gradeable = the right answer can be *located in the documents and pointed at* — a clause,
   > a limit, a date, a rate, a rule. Verified with `grep` + reading, exactly like `golden.py` in S18.
   > Ungradeable = the right answer needs professional judgment (is this claim valid, should I
   > take this drug, will this contract hold). **Refuse those. The liability isn't worth a portfolio piece.**

   Payments/fintech is still the *warmest* lane (Way2News: integrations, idempotency, webhooks,
   double-charge prevention — he *was* the confused integrator), but it is no longer the only one.
5. **Big enough to be worth the name, small enough to reply.** Series A-C beats a giant.
   A 5,000-person company routes him to procurement. A 60-person company routes him to the founder.

## Filter-out list (protect the one slot)
- Anyone who already ships a docs bot.
- Anyone who wants it "by Friday" — this is a 3-4 week build.
- Anyone who won't name a point of contact. No contact = no corpus = dead project.
- Anyone who asks him to sign away his right to say he built it.
- Private/regulated data (customer PII, medical, unreleased legal) — out of scope for a free first build.

---

## The non-monetary price (he must ask for all four)

Free does not mean free of obligations. Put these in the first call:

1. **The corpus** — export or crawl permission, within 1 week of yes.
2. **A named point of contact** who answers questions within ~48h.
3. **30 minutes a week for 3-4 weeks.** Nothing else works.
4. **A testimonial + permission to publish a written case study** (numbers can be anonymised).

If they won't give these four, the project will die halfway and cost him a month. Walk.

---

## Channel plan

| Channel | Use for | Cadence |
|---|---|---|
| **LinkedIn public post** | inbound. Lets the best client find him. | 1 post/week, Mon or Tue ~9 AM IST |
| **LinkedIn DM** | outbound to a named human. Warm after they see the post. | 3-5/week, audited only |
| **Cold email** | outbound where email is findable. Higher intent than DM. | 3-5/week, audited only |
| **The articles** | proof. Every message links one. | already live |

⚠️ **Spacing, his own finding (S19):** two posts too close together and the second one dies.
Article #2 went out **today, 20 Aug**. **Do not post the free-offer post before Mon 24 Aug.**

## Weekly rhythm (keep it small enough to actually do)
- **Mon** — post. 30 min.
- **Tue/Wed** — 2 audits. ~4 hrs total, spread over the week.
- **Thu** — send those 2, plus follow-ups on anything 5+ days silent.
- **Fri** — log replies in `target-list.md`. Adjust.

Expect **1-2 real replies per 10 audited sends.** That is normal and it is enough — he needs one.

---

## Files here
- `linkedin-post.md`   — the public offer post (2 variants) + a follow-up post
- `dm-templates.md`    — connection note, cold DM, warm DM, follow-ups
- `email-templates.md` — the audit email, a no-audit fallback, follow-up ladder
- `target-list.md`     — the pipeline. Fill it, don't keep it in his head.
- `scope-one-pager.md` — what he sends AFTER they say yes. Prevents the free project from eating him.
