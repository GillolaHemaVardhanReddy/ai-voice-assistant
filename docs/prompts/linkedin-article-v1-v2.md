<!-- Spidy v1->v2 LinkedIn article. Rendered copy: paste from the artifact page, not from here. -->
<!-- REWRITE 9 Aug 2026: restructured from a findings-report into the actual climb.
     Two additions his call: (1) the authorship crisis as the turning point, full honesty,
     (2) one deep math dive - 0.416 vs 0.463 - explained properly instead of skipped.
     Nothing invented. Every number and quote is from the session logs. -->

# I built an AI assistant for my portfolio. Then I found out I couldn't write it.

I'm a MERN developer. JavaScript, React, Node, MongoDB. For the last few months I've been learning AI by building one real thing properly instead of watching tutorials.

The thing is **Spidy**, an assistant on my portfolio that answers questions about my work. It's live now. Getting there took two versions, a lot that I got wrong, and one afternoon where I found out I'd been fooling myself about how much of it I actually understood.

That last part turned out to be the most useful thing that happened, so it's in here too.


## Why I built it

First I just asked a normal AI model some questions about myself, to see what would happen.

It didn't invent a fake resume. That's what I'd expected and it didn't do it. What it actually did was politely say it didn't know, and then send the visitor off to go check my LinkedIn.

So it wasn't lying. It just had nothing to work with. Its own answer said it: **"not in my context."**

That's the whole problem. The model didn't need to be smarter. It needed my notes.


## The forty lines that took me four weeks to understand

The technique is called **RAG**, retrieval-augmented generation. It means: search your own documents first, then hand what you found to the model and tell it to answer only from that.

Here's the version everyone writes. I wrote six plain text files about my work. A script cuts them into 127 short pieces and turns each piece into **a list of numbers that represents its meaning**. When someone asks a question, the question becomes numbers the same way, and I keep the pieces whose numbers are most similar. Those go into the prompt with one instruction: answer only from this, and say so if the answer isn't here.

That's it. The search itself is one matrix multiplication. No framework, no library, around forty lines.

I can write that paragraph in thirty seconds now. **Understanding the fourteen words in the middle of it — "a list of numbers that represents its meaning" — took me about a month**, and it's the part every tutorial waves past.

Here's what's underneath it.

A list of numbers is a **direction**. Two numbers give you a direction on a page, three give you a direction in a room, and these have hundreds. You can't picture hundreds, but the rule doesn't change: **things that mean similar things end up pointing similar ways.** To compare two pieces of text you measure the angle between their arrows. That measurement is called **cosine similarity** and it comes out between 0 and 1. Point the same way, you get 1. Point at right angles, you get 0.

So far so good. I tested it on words and it behaved exactly like I hoped:

> `cat` vs `kitten` → **0.788**
> `cat` vs `car` → **0.463**

Two words that mean nearly the same thing scored high. Two words that only share their spelling scored much lower. **Meaning was beating spelling.** I was thrilled.

And then I made the obvious mistake. If 0.788 is a good match and 0.463 is a bad one, then somewhere around 0.45 is the line. So filter on it — only keep pieces that score above 0.45, throw away the rest, and you'll never feed the model junk.

Then I ran a real question against my real notes, and **the piece that actually contained the answer scored 0.416.**

Lower than `cat` versus `car`.

That filter would have thrown away the correct answer and kept nothing. My assistant would have looked a visitor in the eye and said *"I don't have that information"* about a fact sitting in its own files. No error. No crash. Nothing in any log.

**The reason is something nobody mentions.** I'd assumed these arrows spread out across all available directions, the way you'd expect — related things close together, unrelated things far apart, opposites pointing away. They don't. They all crowd into one narrow cone. Everything points roughly the same way as everything else.

I measured the floor. Five completely unrelated words, compared against each other: the lowest score I could produce was **0.186**. Nothing ever comes near zero, because nothing is ever actually pointing away.

So `cat` vs `car` at 0.463 doesn't mean "cats and cars are somewhat alike." It means **the floor is high and 0.463 is barely off it.** The number on its own was never telling me what I thought it was telling me.

I proved the cone was real before I believed it. There's a correction called centering, where you find the average direction of everything and subtract it, which should collapse the cone. I ran it on ten pairs. Every single pair went negative, averaging **−0.2484**, against a theoretical prediction of **−0.25**. That matched to three decimals and I finally stopped arguing with it.

Which leaves one rule, and it's the single most useful thing I learned in the entire project:

> **The score on its own means nothing. Only the order means anything.**

So you never filter by score. You take the top few, whatever they scored, and you let the model work with them. **Take the top five, never "everything above 0.45."**

I got that wrong, in a different costume, four separate times before it stuck.


![The top half is the part most RAG diagrams skip. Chunking and embedding happen offline, once. Only the bottom row runs when someone asks something.](~/Desktop/spidy-figures/04-arch.png)
*The top half is the part most RAG diagrams skip. Chunking and embedding happen offline, once. Only the bottom row runs when someone asks something.*

Every answer ends with the files it used, like `[boundaries.txt]`, so people can check where an answer came from instead of trusting it.


![Real scores for "Does he have experience in MongoDB?" The right piece wins by 0.128. The next four are all within 0.02 of each other.](~/Desktop/spidy-figures/05-hits.png)
*Real scores for "Does he have experience in MongoDB?" The right piece wins by 0.128. The next four are all within 0.02 of each other.*


## What I was actually shipping

Retrieval turned out to be the easy part. The hard part was getting the whole thing to fit in **512 MB of memory**, which is what free hosting gives you.

My first Docker image was **1.95 GB**.

At some point I sat down and did this multiplication:

> **127 pieces × 384 numbers each × 4 bytes = 190 kilobytes**

190 KB. That's the actual data my assistant needs to work. I had shipped 1.8 GB of libraries in order to produce it. **I'd built a whole factory to deliver one envelope.**


![At this scale the real data would be 0.09 pixels wide, so I didn't draw it as a bar.](~/Desktop/spidy-figures/01-ratio.png)
*At this scale the real data would be 0.09 pixels wide, so I didn't draw it as a bar.*

Fixing that taught me more than the AI part did.

**A model is not a runtime.** The weights were about 90 MB. Everything wrapped around them was 1.8 GB. In my head those had been one thing.

**Removing a dependency once doesn't mean it's gone.** I took a large library out of `requirements.txt` and it walked straight back in through the Dockerfile.

**Check inside the container, not the manifest.** I found a 57 MB symbolic algebra library sitting inside a web service that does no algebra. It arrived as somebody else's dependency. I only found it by running `du` inside the running container.

**Build time is not run time.** Those 127 pieces never change between requests, and I was re-cutting and re-embedding every one of them every time the server started. That moved offline into a file the server just loads.

Where it ended up: **1.95 GB down to 347 MB on disk, and 625 MB of memory down to 63.4 MB.** Same 127 pieces, same answers. I saved all twelve retrieval scores before I started and checked them again afterwards, matching to three decimals, before I believed any of it.


![Two different measurements, so two panels. The dashed line is the limit the first build couldn't get under.](~/Desktop/spidy-figures/02-shrink.png)
*Two different measurements, so two panels. The dashed line is the limit the first build couldn't get under.*


## The failures that returned 200 OK

Early on, Spidy answered in first person. *"I built the analytics platform."*

Nothing in the prompt had told it who it was, so it assumed it was me. It was speaking **as me**, on my own site, and nothing about it looked broken. The fix was one paragraph: you are Spidy, you are not Hemavardhan, always speak in third person.

That one stayed with me longer than the 1.9 GB did. It didn't crash. **It ran perfectly and did the wrong thing.**

There was a worse one. I had two lists, one of scores and one of text, and I'd let them drift out of alignment — so the system was ranking one piece of text and then printing a different one. There is no error for that. The program was completely happy. I only caught it because the output stopped making sense and I trusted that feeling enough to go looking.

Both of those returned **200 OK**. That's the category of bug this whole project taught me to be afraid of.


## v2: it couldn't follow a conversation

v1 treated every question as though it were the first thing you'd ever said. Ask *"does he know MongoDB?"* and it answers properly. Ask *"so he knows it?"* immediately after, and it has no idea what "it" is.

The obvious fix is to send the conversation history along with the question, and that half works immediately. The model can see the earlier turn now.

But there's a second half I completely missed. **The search doesn't get the conversation.** It only ever receives the sentence you just typed. So on that follow-up, my system was searching 127 pieces of text for the phrase *"so he knows it?"*

I measured how bad that is.


![Same 127 pieces, same search, two questions one turn apart. The MongoDB piece doesn't come fifth on the follow-up. It doesn't show up at all.](~/Desktop/spidy-figures/06-blind.png)
*Same 127 pieces, same search, two questions one turn apart. The MongoDB piece doesn't come fifth on the follow-up. It doesn't show up at all.*

Best match on the follow-up: **0.344**. Best match on the properly-worded question: **0.620**. And the floor — five unrelated words against my notes — was **0.186**.

So the follow-up landed closer to random noise than to the answer.

What bothered me more: **it still returned five results, confidently.** Top-k search always returns k. There is no way for it to report that it found nothing. It hands you five pieces of your own notes with a straight face and the model does its best with them.

The fix is to rewrite the question before searching. Turn *"so he knows it?"* into *"Does Hemavardhan have knowledge of MongoDB?"*, and search for that instead. The person still typed four words; a small extra call in between decides whether the thing can answer at all.


![Same four words typed by the user either way. One extra call before the search decides whether the thing can answer at all.](~/Desktop/spidy-figures/07-rewrite.png)
*Same four words typed by the user either way. One extra call before the search decides whether the thing can answer at all.*

It took me four attempts.

The first came back as *"Here's the rewritten question:"* followed by the question and then an answer nobody asked for — and all of that went into the search. The second quietly lifted a fact out of the previous answer and changed what was being asked. I added a line to the prompt telling it not to change the meaning. It failed again.

What finally worked wasn't a better instruction. It was giving the input **structure** — labelled sections, so the model could see where the conversation ended and the question began. Three prompt rewrites, beaten by one heading.

> **You can't fix a structural problem by adding adjectives.**


## The afternoon I found out I couldn't write it

Here's the part I nearly left out of this post.

By this point I had a working system. Retrieval, citations, memory, a deployed API, a widget on my portfolio. I could explain every piece of it. I'd debugged it, measured it, shrunk it by 82%.

And then I noticed something I didn't like. **Every line of it had been typed by me, and almost none of it had been written by me.** I'd been learning with AI assistance, and I'd let myself land in a pattern where the code appeared, I read it, I understood it, I typed it, it worked. I could follow every line. I had never once faced a blank file.

So I deleted one. `git rm` on the main retrieval file, the one I'd just finished. No reference open. Just a written description of what it had to do, and an empty editor.

What I typed into my notes about ninety minutes later was:

> *"damnnn its too worst… i couldnt even write code properly"*

Here's what actually happened, because the details are funnier and more useful than the feeling.

The structure came out **right**. Six separate design decisions — which pieces to import, how to order the messages, a subtle one about default arguments that I'd learned the previous week and applied without being prompted. That part I genuinely owned.

Then there were four bugs:

- I used **JavaScript's spread syntax** in Python. Muscle memory from my day job, in a language that doesn't have it. Instant syntax error.
- I called a method that belongs to **LangChain**, a library this project has never had installed. I had absorbed it from reading example code somewhere and stored it as though it were something I knew.
- I returned the whole API response object instead of the text inside it. The envelope instead of the letter.
- And the real one: I built the final message and **left the retrieved context out of it.** That doesn't crash. It produces an assistant that politely answers *"I don't have that information"* to every question forever, while the retrieval underneath it works perfectly.

That last bug is the same species as everything else in this post. It returns 200. It looks like the guardrail working.

**What I got wrong wasn't the code. It was what I thought "I understand this" meant.**

Understanding code and producing code are two different skills, and the first one feels almost exactly like the second one right up until the editor is empty. Reading a solution and agreeing with it is not the same as being able to reach for it. I had months of the first and almost none of the second, and I couldn't tell from the inside.

The reframe that made it bearable came when I looked at the four bugs properly: **those mistakes were always in me.** They didn't appear that afternoon. They'd been getting absorbed and corrected before I ever saw them, which gave me the pleasant illusion of a clean run. I wasn't suddenly worse at this. I was seeing, for the first time, what had always been there.

I write everything from a specification now. I get a description of what a file has to do and what it must not do, and then I write it, badly, and then I fix it. It is slower and significantly less pleasant and it is the only reason I can say I built this.

If you're learning anything with AI right now, that's the thing I'd want to hand you. **Delete a file you just finished and try to write it again from memory.** You'll find out in twenty minutes what I took months to notice.


## What I actually learned

The technical facts are in any tutorial. These weren't.

**Measure your instrument before you measure your change.** Early on I decided the memory feature was working because the answers looked different with it turned on. Then I ran the same question three times with nothing changed at all, and got three different wordings. My proof had been noise the whole time. Now the first thing I build for any change is the measurement of changing nothing.

**If both options pass, you didn't test anything.** My first memory test used a follow-up question that happened to contain its own keyword, so the search found the right answer without needing any history. Both versions passed. I nearly shipped on that and called it evidence.

**The number and the ranking are different things.** 0.416 was the right answer and 0.463 was two unrelated words. Trusting the number would have quietly broken the product.

**Know what you're actually shipping.** 190 KB inside 1.8 GB. No build log tells you that ratio; you have to go and divide it yourself.

**The failures that matter don't crash.** The bot speaking as me. A question that quietly rewrote itself into a different question. Search returning five confident wrong results. A message built without its context. Every one of them returned 200 OK.

**Comprehension isn't authorship.** That one cost the most and I'd pay it again.


## What's next

v2 is live. It remembers, and it can follow a pronoun.

It still can't tell an exact product name from a general topic. It still takes whatever five pieces are nearest without checking whether they're any good. It still takes a few seconds to answer.

All of those have names and known fixes, and I'll write them up as I build them. The next one is the least interesting and the most useful: a set of real questions paired with the file that should answer each one, so that from here every change gets a number instead of my opinion.

Spidy is on my portfolio if you'd like to try it. It'll also tell you what I haven't done — I wrote those notes on purpose.

---

## Alternate titles

1. **I built an AI assistant for my portfolio. Then I found out I couldn't write it.** ← current
2. I shipped an AI assistant I understood completely and couldn't have written.
3. My AI assistant worked. Deleting one file showed me how little of it was mine.
4. What I learned building a RAG assistant, including the afternoon I couldn't type a blank file.

---

## The share-post (separate from the article)

Post Tuesday or Wednesday, 9–10 AM IST. **Article link goes in the first comment, not the post
body** — LinkedIn suppresses posts that carry external links.

Every technical term is glossed in the sentence it appears in, so a non-technical reader can
follow every line while a technical reader still sees the right vocabulary.

```
I spent a few months building an AI assistant for my portfolio. It uses RAG, retrieval-augmented generation, meaning it searches my own notes before answering instead of guessing.

It works. It's live. And a few weeks ago I deleted one of its files to see whether I could write it again from scratch.

I couldn't.

The structure came out right. Then I used JavaScript's spread syntax in Python, called a method belonging to a library this project has never had installed, returned the whole API response instead of the text inside it, and built the final prompt while leaving out the retrieved context entirely.

That last one doesn't crash. It produces an assistant that politely says "I don't have that information" to every question forever, while the search underneath it works perfectly.

Every line of that project had been typed by me. Almost none of it had been written by me. I could read code, follow it, agree with it, and I had never once faced an empty file — and those feel identical from the inside right up until the moment they don't.

I write everything from a specification now. Slower, worse first drafts, and the only reason I can say I built this.

The full write-up covers both versions: why the correct answer scored 0.416 while two unrelated words scored 0.463, why my first container was 1.95 GB to ship 190 KB of data, and why the search goes blind the moment someone asks a follow-up question.

Link in comments.

#RAG #AI #LLM #MachineLearning #SoftwareEngineering
```

**First hour matters.** Reply to every comment — LinkedIn weights early engagement heavily and
your own replies count toward it.
