# LinkedIn — the public offer post

⚠️ **Do not publish before Mon 24 Aug 2026.** Article #2 went out 20 Aug; his own S19 finding is that
two posts close together kill the second one. Post ~9:00 AM IST, Mon or Tue.

⚠️ Replace every `<<...>>` before posting. **Never post with a placeholder or an unverified number.**

---

## Variant A — "the free build" (recommended first post)

Direct, states the trade, no false modesty. Same voice as the v3 post.

---

I'm going to build one company a production RAG chatbot. For free.

Not a trial. Not a discount. Zero fee, and you keep the code.

Here's the honest reason: I've spent the last two months building a retrieval system from scratch
and publishing every number, including the ones that embarrassed me. Reranking that moved my
retrieval score by exactly nothing. A relevance cutoff I calibrated on clean test data that was
3x too low the moment it touched real data.

What I don't have yet is a corpus that isn't mine. 144 chunks over 8 files teaches you the mechanics
and then stops teaching you anything. Vector databases, hybrid search, observability, the failure
loop — none of it is real below a few thousand documents.

So I want one. And I'd rather earn it than buy an ad.

What I'll build:
→ Retrieval over your documentation, with citations to your own pages
→ A golden question set — the actual test suite, so quality is a number, not a vibe
→ Abstention. It says "I don't know" instead of inventing something. This is the hard part
→ An API + an embeddable widget
→ Full handover: code, repo, docs. Yours

What it costs you: the model API after handover (cents per hundred questions) and your own domain.
That's the entire bill. I cover everything during the build.

What I want back: a testimonial, and permission to write up what I learned.

I'll pick one. I'm looking for thick public developer docs, no existing docs bot, and someone
who'll give me 30 minutes a week for a month. Payments and fintech first — that's my day job, so
I can tell a correct answer from a plausible one, and that's most of the work.

Live demo of the current version, and the write-up with all the numbers: <<portfolio link>>

DM me, or gillolahemavardhanreddy@gmail.com

#RAG #AI #LLM #Freelance #BuildInPublic #BackendEngineering

---

## Variant B — "the audit" (stronger, use once he has ONE real audit done)

Opens with a number about someone else. Far higher engagement, but it must be true.

---

I asked <<Company>>'s documentation 20 questions this weekend. Their search answered 6 of them.

To be fair to them, that's not a broken search. It's a normal keyword search meeting questions
phrased the way an actual integrator phrases them — "why did my webhook fire twice", not "idempotency".

I rebuilt it as a retrieval system: embeddings, a reranker, a calibrated relevance cutoff.
It answered <<17>>, each one citing the exact page it came from. And on 4 questions their docs
genuinely don't cover, it said so instead of inventing an answer — which took me longer to build
than the answering did.

I did it because I wanted to know if what I'd been practising on my own 144-chunk corpus survives
contact with a real one. It mostly did. <<one honest thing that broke>>.

I'm doing this for one company for free — the full build, handed over, no fee. You'd pay the model
API after handover and nothing else.

If you own developer docs and you've ever watched a support ticket that was already answered on
page 4, I'd like to run this on yours.

The whole method, with the numbers: <<article link>>

#RAG #AI #DeveloperExperience #LLM #BuildInPublic

---

## Follow-up post (~1 week later, if replies are thin)

Never repost the same offer. Post a *finding* instead and put the offer in the last line.

Skeleton:
- One surprising number from the week's audits ("three of the four docs sites I tested rank their
  changelog above their reference for version questions")
- The mechanism — why it happens
- What he changed
- Last line: "Still building one of these for free. One slot. <<link>>"

---

## Rules for the comments (this is where the client actually appears)
- Reply to **every** comment within an hour of posting. LinkedIn weights early replies.
- Never argue with a critic. "That's a fair hit — here's the number, tell me if you read it differently."
  His two articles work because he's wrong in public gracefully. Keep doing that.
- Anyone who comments something substantive gets a DM the next day. Not a pitch — a question about
  their stack. The pitch is the second message, or never.
