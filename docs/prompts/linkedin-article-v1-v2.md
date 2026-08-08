# LinkedIn **article** — Spidy v1 → v2

**Format notes before you paste:** LinkedIn articles handle headings, bold, and images well.
They handle **tables and code blocks badly** — so there are none here. Images go where marked;
sources are in `spidy-v1-figures.md`. Screenshot each SVG (or export from the preview page) —
LinkedIn wants image files, not markup.

**Publish tonight, share as a post Tuesday or Wednesday 9–10 AM IST.**

**Suggested title:** *I built an AI assistant that answers questions about me. Then I found out it couldn't hear a follow-up.*

**Subtitle / first line:** *What two versions of a retrieval-augmented assistant taught me about measuring things I couldn't see.*

---

## The article

I built an assistant for my portfolio. It answers questions about my work — my skills, my projects, what I have and haven't done in production. It's called Spidy, it's live, and getting it there took two versions and a lot of being wrong in public.

This is what happened, and what I'd tell anyone building the same thing.

### It started with a polite failure

I asked a language model questions about myself and watched it fail — but not the way I expected. It didn't invent a fake CV. It did something worse for a portfolio: it was **confidently useless**. It refused politely, then sent the visitor away — *"you should check his LinkedIn."*

The model named its own problem in its own reply: **"not in my context."**

That sentence is the reason v1 exists. The model didn't need to be smarter. It needed to be handed my notes.

### Version 1: teaching it to read my files

The technique is called **RAG** — retrieval-augmented generation — and underneath the acronym it is simpler than it sounds.

I wrote six plain text files about my work. A script splits them into 127 short pieces, and turns each piece into a list of numbers that represents its meaning. When a visitor asks a question, the question gets turned into numbers the same way, and the system finds the pieces whose numbers point in the most similar direction. Those pieces get pasted into the prompt, with an instruction: *answer only from this, and say so when the answer isn't here.*

That's it. **Retrieval is one matrix multiply.** No framework, no library — about forty lines.

> **[IMAGE 1 — Figure 4, "v1 architecture"]**
> *Caption: The half most RAG diagrams leave out is the top one. Chunking and embedding happen offline, once. Only the bottom row runs per question.*

Every answer ends with the files it used, like `[boundaries.txt]`, so a visitor can see where it came from. That mattered more than I expected: it's the difference between a chatbot and a source.

> **[IMAGE 2 — Figure 5, "What retrieval actually returns"]**
> *Caption: Real scores for "Does he have experience in MongoDB?" The right chunk wins by 0.128, while the four runners-up sit within 0.02 of each other. That gap is the signal.*

### The hard part wasn't the AI

Retrieval was the easy bit. **The hard part was making it fit in 512 MB of memory**, which is what a free hosting tier gives you. My first container image was **1.95 GB**.

Then I did the arithmetic that changed how I think about deployment:

**127 chunks × 384 dimensions × 4 bytes = 190 kilobytes.**

The data was 190 kilobytes. The machinery I had shipped to produce it was 1.8 gigabytes. **I was deploying a factory in order to deliver one envelope.**

> **[IMAGE 3 — Figure 1, "The ratio"]**
> *Caption: At the same scale, the actual data would be 0.09 pixels wide. So it isn't drawn as a bar — drawing it would be a lie.*

Chasing that down taught me more than the retrieval did:

**A model is not a runtime.** The weights were about 90 MB. The libraries wrapped around them were 1.8 GB. I had been thinking of them as one thing.

**A dependency you removed once may not be removed.** I took a large library out of the requirements file and it came back in through the Dockerfile by a second route.

**Look inside the container, not at the manifest.** I found a 57 MB symbolic-algebra library sitting in a web service that does no algebra, pulled in as somebody else's dependency. I only found it by running `du` inside the running image.

**Build time is not run time.** The 127 chunks never change between requests, so chunking and embedding them at every boot was pure waste. That work moved offline into a file the server just loads.

Final result: **1.95 GB down to 347 MB on disk, and 625 MB of runtime memory down to 63.4 MB.** Same 127 chunks, same answers — I verified all twelve retrieval scores matched my saved baseline to three decimals before trusting a single byte of it.

> **[IMAGE 4 — Figure 2, "The shrink"]**
> *Caption: Two measures, two scales, two panels. The first build simply did not fit under the ceiling.*

### The bug that actually scared me

Early on, Spidy answered in the first person. *"I built the analytics platform."*

Nothing in the prompt had told it who it was, so it quietly assumed it was me. It was **impersonating me on my own website**, and it never once looked broken. The fix was one paragraph: *you are Spidy, you are not Hemavardhan, always speak in the third person.*

The lesson stuck harder than the 1.9 GB one. **The failure that scared me wasn't a crash. It was the system confidently doing the wrong thing with nobody noticing.**

### Version 2: it couldn't hear a follow-up

v1 answered every question as if it were the first thing you'd ever said. Ask *"does he know MongoDB?"* and it answers well. Ask *"so he knows it?"* and it has no idea what "it" means.

The obvious fix is to send the conversation history along with the question, and that half works immediately — the model can now see the earlier turn.

But there's a second half almost everyone misses, and I missed it too. **The search doesn't see the conversation.** It only ever gets the raw sentence you just typed. So on the follow-up, my system was searching 127 chunks for the literal phrase *"so he knows it?"*

I measured what that costs.

> **[IMAGE 5 — Figure 6, "The retriever going blind"]**
> *Caption: Same chunks, same retriever, two questions one turn apart. The MongoDB chunk doesn't rank fifth on the follow-up — it doesn't appear at all.*

The best match for the follow-up scored **0.344**. The right question scored **0.620**. And when I measured what five completely unrelated words score against my notes, the floor was **0.186**. So the follow-up's best match was closer to random noise than to an answer.

Worse: **the search still confidently returned five chunks.** Top-k always returns k. It has no way to say "I found nothing."

The fix is to rewrite the question before searching — turn *"so he knows it?"* into *"Does Hemavardhan have knowledge of MongoDB?"*, then search for that.

> **[IMAGE 6 — Figure 7, "What query rewriting changes"]**
> *Caption: The user types the same four words either way. One extra call before retrieval decides whether the system can answer at all.*

It took four attempts. The first rewrite came back wrapped in *"Here's the rewritten question:"* plus an unsolicited answer — all of which got fed into the search. The second absorbed a fact from the previous answer and quietly changed what was being asked. I added a rule to the prompt saying *don't change the meaning.* **It still failed.**

What actually fixed it was not a better instruction. It was **giving the input structure** — labelled sections, so the model could tell where the conversation ended and the question began. Three prompt rewrites lost to one heading.

**You cannot fix a structural problem with more adjectives.**

### What I actually gained

The technical parts are learnable from any tutorial. These weren't.

**Measure your instrument before you measure your change.** Early on I "proved" the memory feature worked because the answers looked different with it on. Then I ran the identical question three times with nothing changed at all — and the wording differed every time. My proof had been noise. Now the first thing I build for any change is the measurement of doing nothing.

**An experiment where both options pass is not evidence.** My first memory test used a follow-up that happened to contain its own keyword, so the search found the right answer without needing any history. Both versions passed. The test had no power to distinguish anything, and I nearly shipped on it.

**Know the size of what you're actually shipping.** 190 kilobytes of value inside 1.8 gigabytes of packaging. Nobody's build log tells you that ratio. You have to go and divide.

**The dangerous failures don't crash.** An assistant speaking as me. A rewritten question that silently narrowed its own meaning. Retrieval returning five confident irrelevant results. Every one of them ran perfectly and returned a 200.

### Where it goes next

v2 is live. It remembers, and it can follow a pronoun. It still can't tell an exact product name from a general topic, still returns whatever five chunks are nearest without checking whether they're any good, and still takes a few seconds to answer.

Each of those has a name and a known fix, and I'll write them up as I build them. The next one is the least glamorous and the most useful: a set of real questions with the file that should answer each — so that from here, every improvement gets a number instead of my opinion.

Spidy is on my portfolio if you want to ask it something. It'll tell you what I haven't done, too — I wrote those notes deliberately.

---

## The share-post (separate, Tuesday 9–10 AM IST)

> I built an AI assistant for my portfolio. It worked — until someone asked a follow-up question.
>
> "Does he know MongoDB?" → perfect answer.
> "So he knows it?" → no idea what "it" means.
>
> The model had the conversation. **The search didn't.** It was looking through 127 documents for the literal phrase "so he knows it?"
>
> I measured how badly that fails. The right question scores 0.620. The follow-up scores 0.344. Five completely unrelated words score 0.186.
>
> The follow-up was closer to random noise than to the answer — and the system still returned five confident results, because that kind of search has no way to say "I found nothing."
>
> I wrote up both versions: what RAG actually is under the acronym, why my first container was 1.95 GB to ship 190 KB of data, the bug where the bot started speaking as me, and the four attempts it took to fix the follow-up problem.
>
> Link in comments 👇
>
> #AI #RAG #LLM #SoftwareEngineering #MachineLearning

**Why link in comments:** LinkedIn suppresses posts with external links in the body. Put the
article link in the first comment, immediately after posting.
