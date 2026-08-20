# 📄 Scope one-pager — send AFTER they say "tell me more"

This exists so a free project cannot quietly eat three months. Free work with no scope is
the single most common way a first freelance project ends badly — for both sides.

Send it as a short doc or the body of an email before the first call. Keep the tone
collaborative, not legalistic. It's a shared understanding, not a contract he'll enforce.

---

## RAG documentation assistant — scope

**Prepared for:** <<Company>> · **By:** Hemavardhan Reddy · **Date:** <<date>>

### The deal, plainly
I build this at no charge and hand it over. I'm early in freelancing and want one real
production system with a real corpus. In return I'd like a short testimonial and permission
to write publicly about what I learned — with any numbers anonymised if you prefer.

### What I deliver
1. **Ingestion** for your public documentation — chunking tuned to your page structure,
   re-runnable when docs change.
2. **Retrieval** — embeddings + reranking + a relevance cutoff calibrated on YOUR corpus,
   not on defaults. (On my own corpus the textbook cutoff was 3x too low. It's per-corpus work.)
3. **Answers with citations** to the exact page. No uncited claims.
4. **Abstention** — "I don't have that in the docs" instead of a confident invention.
   This is the part that makes it safe to put in front of your users.
5. **A golden question set** — 30-50 real questions with a verified answer key, plus the
   scorer. This is the deliverable I care most about: after handover, your team can prove a
   change made things better instead of guessing.
6. **An HTTP API** + an embeddable chat widget.
7. **Handover** — repository, deployment notes, a runbook, and a walkthrough call.

### What I don't do in this build
Fine-tuning a custom model · voice · multi-language · authenticated or customer-specific
content · anything touching PII or regulated data · SLA-backed uptime. Happy to discuss any
of it separately, later.

### What I need from you
1. A docs export, repo access, or written permission to crawl the public docs.
2. **One named point of contact** who can answer questions within ~2 working days.
3. **~30 minutes a week for 3-4 weeks** — a working call, not a status update.
4. Sign-off on the golden question set. You know your users' questions better than I do.

Without 1 and 2 the project stalls, and I'd rather say that now than discover it in week three.

### Timeline
| Week | |
|---|---|
| 1 | Ingestion + first index. Golden question set drafted, you review it. |
| 2 | Retrieval tuned, cutoff calibrated, first scored run. You see the number. |
| 3 | API + widget, abstention hardened, failure cases from your review folded in. |
| 4 | Deploy, handover, walkthrough. |

Realistically 4-6 weeks — I have a full-time job and I'd rather promise honestly.

### Costs
- **My time: 0.** Not discounted. Zero.
- **During the build:** I cover embedding, reranking and model calls out of pocket.
- **After handover, yours:** the model API — order of <<$X per 1,000 questions>> at current
  pricing, and I'll show you the exact per-query cost measured on your corpus before handover,
  not estimated. Plus a domain and hosting if you want it on your own infrastructure. Hosting
  can be a free tier to start.
- There is no other cost, and no invoice from me at any point.

### Data handling
Public documentation only. Nothing redistributed or published. The demo lives behind a private
link. Everything deleted within 48 hours of you asking, no reason needed. Happy to sign your NDA.

### Ending it
Either of us can stop at any point, no cost, no notice period. If you stop, you keep whatever
exists at that point.

### After handover
It's yours and it runs without me. If you want ongoing work, we can talk about it then —
as a normal paid engagement, and with no obligation on either side.
