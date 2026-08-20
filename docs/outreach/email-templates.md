# Cold email templates

⚠️ **He approves every send.** Nothing leaves without his explicit OK.
⚠️ **Never send with a `<<placeholder>>` still in it, or a number he hasn't re-run today.**

## Mechanics
- **From his own Gmail** — `gillolahemavardhanreddy@gmail.com`. No mail-merge tool, no tracking pixel.
  A cold email from a real person beats a sequenced one, and tracking pixels get flagged.
- **One recipient. Never CC, never BCC a list.** That is the difference between outreach and spam.
- **Send Tue-Thu, 9-11 AM their local time.**
- **Subject line: lowercase, specific, no colon-heavy marketing.** It should look like a colleague wrote it.
- **Plain text.** No logo, no banner, no HTML signature block.
- Total length: **under 200 words.** If it doesn't fit, the audit wasn't sharp enough.

## Who to write to (in order)
1. Head of Developer Experience / DevRel lead
2. Docs lead / technical writing manager
3. CTO or founding engineer (small companies)
4. `support@` or `hello@` — last resort, expect nothing

---

## TEMPLATE 1 — the audit email (primary; requires the 2-hour audit)

**Subject:** `i asked your docs 20 integration questions — search found 6`

```
Hi <<first name>>,

I build payment integrations for a living (currently at Way2News). Last month I built a
retrieval system from scratch and published the numbers, including the parts I got wrong.

This weekend I pointed it at <<Company>>'s public docs as a test. I wrote 20 questions the
way an integrator actually asks them — "<<real question 1>>", "<<real question 2>>" — and
ran them through your docs search. It surfaced the right page for <<6>>.

Mine answered <<17>>, each one citing the exact <<Company>> page it came from. On the
<<4>> questions your docs genuinely don't cover, it says so instead of guessing — that
part took me longer to build than the answering did.

90-second demo on your own docs, no signup: <<private link>>

I'd like to build you the full version. Free — no fee, and I hand over the code and repo
at the end. The only running cost is the model API, roughly <<$X per 1,000 questions>>.

Why free: I'm starting freelancing and one real production system matters more to me right
now than a first invoice. I'd want a testimonial and permission to write it up.

What I'd need: a docs export or crawl permission, one person to answer questions, and
about 30 minutes a week for 3-4 weeks.

Public docs only, nothing redistributed, demo is private and deleted the day you ask.

Worth 15 minutes?

Hemavardhan Reddy
<<portfolio>> · <<article>> · <<github>>
```

---

## TEMPLATE 2 — no-audit fallback (only for a target too big/gated to crawl)

Weaker. Use sparingly — the audit is the whole edge.

**Subject:** `free RAG build for <<Company>>'s docs — one company, my pick`

```
Hi <<first name>>,

Short version: I'm building one company a production RAG chatbot over their documentation,
free, and I'd like it to be <<Company>>.

I've spent two months building retrieval from scratch — embeddings, reranking, a calibrated
relevance cutoff, a golden test set — and publishing every number, including the reranker
that improved my retrieval score by exactly zero. Live demo and the write-ups: <<link>>

What I'd deliver: retrieval over your docs with citations to your own pages, a golden
question set so quality is a number rather than an opinion, abstention when the docs don't
cover it, an API plus an embeddable widget, and full handover of the code.

Your cost: the model API after handover, and your domain. Nothing else, ever.

Why free: I'm starting freelancing and want one real production corpus more than a first
invoice. I'd want a testimonial and permission to write up what I learned.

If <<Company>> isn't the fit, I'd genuinely value a pointer to someone whose docs are.

Hemavardhan Reddy
<<portfolio>> · <<github>>
```

---

## Follow-up ladder (max 2, then stop)

**+5 days — add value, don't nag.** Subject: `Re: <original>`
```
Hi <<first name>> — following up once.

Since I wrote, I <<one concrete thing: added the 3 questions your changelog answers but
search doesn't / fixed X in the demo>>. Demo's still up: <<link>>

If this isn't the quarter for it, that's completely fine — just say so and I'll stop.
```

**+12 days — the close.** Subject: `closing the loop`
```
Hi <<first name>> — I'm picking the company I build this for on <<date>>, so I'll take
this off my list unless I hear otherwise. No hard feelings either way.

If it's useful, the 20 questions I ran and how your docs scored on each are here — yours
to keep whether or not we work together: <<link>>
```

**Then stop.** Two follow-ups. That's it. A third makes him the guy who won't stop emailing,
and he only needs one client.

## When they reply "yes, tell me more"
Do NOT start building. Send `scope-one-pager.md` and get the 30-minute call. The most common
way a free project dies is enthusiasm before scope.
