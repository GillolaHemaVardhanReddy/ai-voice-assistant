<!-- Spidy v2 -> v3 LinkedIn article. Written 19 Aug 2026 (S22).
     Every number is from the session logs. Nothing invented.
     Callback thread: the 11 Aug article stated a rule AND an unsolved problem.
     This one solves the problem by breaking the rule. -->

# I ended my last article with a problem I couldn't solve. Fixing it meant breaking a rule I published in the same article.

Last month I wrote about building **Spidy**, an AI assistant on my portfolio that answers questions about my work. It reads six plain text files about me, cut into 127 pieces, and finds the relevant ones before answering.

Two things from that article matter here.

The first was a rule I stated with a lot of confidence:

> **The score on its own means nothing. Only the order means anything. Take the top five, never "everything above 0.45."**

The second was a problem I described honestly and had no fix for:

> *"It still returned five results, confidently. Top-k search always returns k. **There is no way for it to report that it found nothing.** It hands you five pieces of your own notes with a straight face and the model does its best with them."*

This month I fixed the second one. The only way to do it was to break the first one.

Here's what I got right, what I got wrong, and the mistake in the middle that cost me an evening.


## Why the rule was correct

Quick recap, because the rest doesn't make sense without it.

Text gets turned into a list of numbers — a **direction**. Similar meanings point similar ways. You compare two pieces of text by measuring the angle between their arrows, and that measurement, **cosine similarity**, comes out between 0 and 1.

The trap is that these arrows don't spread out. They all crowd into one narrow cone. I measured the floor myself: ten pairs of completely unrelated words — `cat` vs `democracy`, `car` vs `hydrogen` — and the lowest score I could produce was **0.186**. Nothing ever approaches zero, because nothing is ever actually pointing away.

Which is why `cat` vs `car` scoring **0.463** doesn't mean cats and cars are somewhat alike. It means the floor is high and 0.463 is barely off it.

So a fixed cutoff is meaningless. Set it at 0.45 and it throws away a correct answer that scored 0.416 while keeping junk that scored 0.47. **Rank the results and take the top few** — that was the rule, and for that tool it is the right rule.

![Measured on my own corpus. Nothing scores below 0.186, so a 0.45 cutoff would have thrown away a correct answer at 0.416 while keeping junk above it.](~/Desktop/spidy-v3-figures/01-cosine-cone.png)
*Measured on my own corpus. Nothing scores below 0.186, so a 0.45 cutoff would have thrown away a correct answer at 0.416 while keeping junk above it.*


What I got wrong wasn't the rule. It was the **scope**. I stated a property of one specific technique as a law of the whole field.


## A different instrument answers a different question

The thing that turns text into a direction is called a **bi-encoder**. The word matters: it encodes the two pieces of text *separately*. Your question becomes an arrow, my notes became arrows weeks ago, and the search compares arrows that were never in the same room.

That's why it's fast — the notes are pre-computed, and the search is one matrix multiplication over 127 rows.

A **cross-encoder** does the opposite. It takes the question and one chunk **together, as a single input**, reads them as one piece of text, and outputs a single number: how relevant is this chunk to this question.

That's a completely different question being asked. Not *"which direction is this text pointing?"* but *"does this text answer this question — yes or no?"*

It's slower, obviously. You can't pre-compute anything, because the score depends on the pair. Scoring 127 chunks means 127 comparisons at query time instead of one matrix multiply. So nobody uses it alone. The standard pattern is:

**Retrieve wide and cheap, then re-score narrow and expensive.** Take the top 20 by cosine, hand those 20 to the cross-encoder, keep the best 3.

![The difference the whole article rests on. A bi-encoder turns each text into a direction separately; a cross-encoder reads the pair together and scores it directly.](~/Desktop/spidy-v3-figures/02-bi-vs-cross.png)
*The difference the whole article rests on. A bi-encoder turns each text into a direction separately; a cross-encoder reads the pair together and scores it directly.*


That's called **reranking**, and every RAG guide recommends it. But the reason I wanted it wasn't better ordering. It was that a cross-encoder trained to answer "is this relevant, yes or no" produces a number that means something **on its own** — not just relative to whatever else happened to be in the list.

If that's true, I get a threshold. And a threshold can return nothing.

My first test, one question against two chunks:

> the chunk that answers it → **0.411**
> a chunk about something else → **0.036**

Cosine's floor was 0.186 for maximally unrelated words. This scored 0.036 for text about the same person. The bottom of the scale looked real.


## Then I set the cutoff, and I set it badly

I built a proper test. Eight documents: two that genuinely answer the question, some that are about me but answer a different question, and two that are absurd — `the sky is blue`, `cat is sitting on the mat`.

The absurd ones scored **0.015** and **0.024**. The correct one scored **0.411**. Clean separation, big empty gap in the middle. I put the cutoff at **0.05** and felt good about it.

Then I ran it against my actual notes with a question they can't answer — *"what is his favourite movie?"* — and got back three chunks scoring **0.065, 0.061, 0.058**.

All above my line. Nothing about movies. The cutoff did nothing.

The reason is obvious in hindsight and I'd like you to have it without the evening I spent on it. **My test documents were too easy.** `cat is sitting on the mat` shares nothing with a question about me — not the subject, not the topic, not even the pronoun. But every one of the 127 chunks in my notes is *about the same person*. Ask *"what is **his** favourite movie?"* and all 127 match on "this is a fact about this man." The whole corpus floats three times higher than a sentence about a cat.

So I threw the lab number away and measured on the real thing. Five questions my notes genuinely cannot answer:

| question | highest score it returned |
|---|---|
| what was his 12th standard percentage? | *nothing came back* |
| what is his favourite movie? | 0.065 |
| what car does he drive? | 0.079 |
| does he have a US visa? | 0.094 |
| **is he married?** | **0.158** |

![The same 0.05 cutoff against hand-picked test documents and against my real notes. In the lab it separated everything cleanly. In production it separated nothing.](~/Desktop/spidy-v3-figures/03-two-scales.png)
*The same 0.05 cutoff against hand-picked test documents and against my real notes. In the lab it separated everything cleanly. In production it separated nothing.*


That last one is the interesting failure. *"Is he married?"* pulled up **"He is currently open to opportunities."** — because **"open to"** genuinely echoes across both meanings. It isn't a dumb mistake, which is exactly what makes it the number that matters.

Then the other side: across my test questions, the lowest score on a chunk that *was* the correct answer was **0.204**.

```
0.158  ← the highest junk can climb
   ↕     the gap
0.204  ← the lowest a real answer sinks
```

The cutoff goes in there. I set it at **0.18**, and wrote the two measurements into the code above it so the next person — me, in four months — can see where the number came from instead of treating it as magic.

![Two numbers decide a threshold: how high junk climbs, and how low a real answer sinks. The line goes between them.](~/Desktop/spidy-v3-figures/04-the-gap.png)
*Two numbers decide a threshold: how high junk climbs, and how low a real answer sinks. The line goes between them.*


**The lesson, and it's the one I'd most want you to take:** calibrate a threshold on the corpus you will actually run against, using queries that actually fail. A threshold tuned on clean examples is tuned for a world you don't ship into.


## Why not something cleverer than a hardcoded number

This bothered me, so I tested it properly.

The popular alternative is the **elbow method**: sort the scores, find the biggest drop, cut there. No constant, the data picks the line. On my scores — `0.411, 0.073, 0.036, 0.030, 0.024, 0.021` — the biggest drop is right at the top, between 0.411 and 0.073.

So the elbow cuts there and throws away the second chunk, which **genuinely answers the question.** The gap being the biggest didn't make it the right one. What matters is what sits on either side of a gap, not how wide it is.

The other adaptive rules fail for a deeper reason. *"Keep anything within 15% of the top score"* works fine — until every candidate is junk, and then it keeps the best junk. `mean + one standard deviation` is worse: one strong hit drags the mean up and cuts the second-best correct answer off.

They all share the same flaw. **Every one of them defines the boundary in terms of the candidates in front of it, so there is always something above the line.** None of them can ever return zero. That is top-k's exact limitation wearing a maths costume.

![The elbow method cuts at the biggest gap — which here sits between two correct answers and throws one away.](~/Desktop/spidy-v3-figures/05-elbow-trap.png)
*The elbow method cuts at the biggest gap — which here sits between two correct answers and throws one away.*


Only an absolute number can abstain. And an absolute number is only defensible when the score is calibrated — which is the whole reason the tool had to change before the rule could.


## The upgrade improved my retrieval score by exactly zero

I had built a test suite before doing any of this: real questions, and which file should answer each. It reports whether the right file came back and how highly it ranked.

Before reranking: **MRR 0.93**.
After reranking: **MRR 0.93**.

Nothing. Every guide says reranking is the biggest single quality jump in RAG, and on my corpus it did not move the number at all.

That result is correct, and it's worth understanding. A reranker earns its reputation by taking a correct chunk buried at position 9 and pulling it to position 1. My score was already 0.93 out of 1.00 — plain cosine was putting the right file first for six of my seven questions. **There was nothing buried.** Six files on clearly different topics is not a hard retrieval problem. Reranking pays off on large, confusable corpora, and mine is neither.

I shipped it anyway, because it fixed something my test suite was never measuring.


## And then my own assistant failed in front of me

While all this was running, I opened my live portfolio and asked Spidy a question any recruiter would ask:

**"Which company does he work for right now?"**

> *"I don't have that information."*

The answer is in its notes. **Five times.** One of the chunks says, in plain English, *"This is his current employer and his current job."*

Here's what the old search actually returned:

```
0.502  "He is open across company stages..."
0.456  "A product company appeals more than a services company..."
0.445  "He leads a team of 4 engineers..."
```

The word **"company"** matched *company stages* and *product company*. It found three chunks about what kind of company I'd like to work at, and never surfaced the one naming where I work. My test suite was passing every row, green, the entire time.

Reranking returns the correct chunk at **0.569**, first place.

![Before and after, on a question any recruiter would ask. The word "company" matched "company stages" and "product company" and never surfaced the chunk naming where I work.](~/Desktop/spidy-v3-figures/06-way2news.png)
*Before and after, on a question any recruiter would ask. The word "company" matched "company stages" and "product company" and never surfaced the chunk naming where I work.*


**That's the part I'd underline.** A test suite you write yourself tests the things you thought of. It cannot test the things you didn't. That question is now a permanent row in my suite — the first one I didn't invent, and the only one that was ever actually broken in production.

One more result I liked. Ask *"has he worked with Kubernetes?"* and the top chunk, at **0.834** — the highest score anything got all day — is the one that says **he hasn't.** Relevance is not agreement. Saying no *is* answering, and the system now scores it that way.


## What it costs

Reranking adds about **0.9 seconds** per question and **$0.001** per query, priced per search rather than per document, so widening the candidate pool from 2 to 20 costs the same.

For a bot that stops improvising at recruiters, that is not a difficult trade.

One thing that nearly went wrong: the reranker used the `requests` library, which was in my local environment only because an unrelated experiment had installed it. It was never in `requirements.txt`. On the server it would have failed at import — and because the import chain runs through the app's entry point, **the entire API would have failed to boot**, not just the new endpoint. Caught it before deploying by checking which package actually required what. *Works on my machine* and *ships* are two different claims, and the gap between them is usually a dependency you never chose.


## What I'd tell you

**A score you can threshold and a score you can only rank are different kinds of number.** Find out which one you have before you write the `if`.

**Calibrate on your real data, with queries that really fail.** Clean test examples give you a clean number for a world you don't ship into. Mine was three times wrong.

**Clever adaptive cutoffs are usually top-k in disguise.** If the rule is defined relative to the candidates present, it can never return nothing — which is the one behaviour you wanted.

**A null result is only visible if you measured first.** My score didn't move, and knowing *that* is worth more than assuming an improvement I never had.

**And your test suite tests what you thought of.** Mine was 7/7 green while the bot couldn't name my employer. Go and use the thing yourself. Every real failure becomes a row that can never silently break again.

Spidy can now say **"I don't have that in my notes"** — and mean it, rather than handing a model three irrelevant paragraphs and hoping.

That was the whole point.


---

Spidy is live on my portfolio if you want to try breaking it. Ask it something my notes can't cover and it should tell you so — that behaviour is one day old and it's the part I'm most pleased with.

If you find a question it gets wrong, I'd genuinely like to know. Every real failure becomes a row in the test suite, and that suite is turning out to be the most valuable thing in the project.
